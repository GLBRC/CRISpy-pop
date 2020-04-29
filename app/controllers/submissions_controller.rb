class SubmissionsController < ApplicationController
  after_action :limit_saved_submissions, only: %i[create]
  before_action :set_resource, only: %i[show edit update destroy]
  skip_before_action :verify_authenticity_token, only: [:create]

  def new
    @submission = Submission.new
    # @offsite_search = OffsiteSearch.new
    # The default set of genes to show for yeast strains.
    @strains = { yeast: Strain.yeast.select(:name, :id), zymo: Strain.zymo.select(:name, :id) }

    # Genes to show if the strain 'GLBRCY22-3' is selected.
    @genes = { yeast: {
      s288c: Gene.where(genome: 'S288C').select(:name, :id).order(:name),
      y22_3: Gene.where(genome: 'Y22-3').select(:name, :id).order(:name)
    },
               zymo: Gene.where(genome: 'ZM4').select(:name, :id).order(:name) }
    @active_tab = params[:active].presence || 'target_gene_yeast'
    @host = APP_CONFIG[:host]
  end

  def show
    @submission = Submission.find(params[:id])
    @results = @submission.results

    if @submission.submission_type == 'custom'
      @locus_start = 1
      @locus_end = @submission.sequence.length
      @chrom_start = 'I'
      @all_strains_count = 1
    else
      @strain = Strain.find(@submission.strain_id)
      @gene = Gene.find(@submission.gene_id)
      @locus_start = @gene.start_pos - 50
      @locus_end = @gene.end_pos + 50
      @chrom_start = @gene.chrom
      @all_strains_count = Strain.where(strain_set: @submission.strain.strain_set).count
    end
    @sgrna_length = @submission.spacer_length
    @pam = @submission.pam_sequence
    @genome = @submission.genome

    if @submission.submission_type == 'custom'
      File.open('public/custom.fasta', 'w+') do |f|
        f << ">I\n"
        f << @submission.sequence.delete(" \t\r\n")
      end
      # have to make .fai index of fasta file for igv to view it
      `samtools faidx public/custom.fasta`
    end

    @chrom_types = %w[yeast zymo]

    File.open('public/generated_sgrna_coords_pos.bed', 'w+') do |f|
      @results.each do |r|
        position = r.pos_in_gene.to_i if @submission.submission_type == 'custom'
        position = r.pos.to_i if @chrom_types.include?(@submission.submission_type)
        chrom = 'I' if @submission.submission_type == 'custom'
        chrom = r.chrom if @chrom_types.include?(@submission.submission_type)
        if r.strand == '+'
          chromend = position + r.sgrna_sequence.length.to_i
          f << "#{chrom}\t#{position}\t#{chromend}\t#{r.name}\n"
        end
      end
    end
    File.open('public/generated_sgrna_coords_neg.bed', 'w+') do |f|
      @results.each do |r|
        position = r.pos_in_gene.to_i if @submission.submission_type == 'custom'
        position = r.pos.to_i if @chrom_types.include?(@submission.submission_type)
        chrom = 'I' if @submission.submission_type == 'custom'
        chrom = r.chrom if @chrom_types.include?(@submission.submission_type)
        if r.strand == '-'
          chromend = position + r.sgrna_sequence.length.to_i
          f << "#{chrom}\t#{position}\t#{chromend}\t#{r.name}\n"
        end
      end
    end
  end

  def create
    @submission = Submission.new(resource_params)
    @submission.created_by = 'Crispy User'

    if @submission.submission_type == 'custom'
      seq = @submission.sequence.gsub(/\s+/, '').upcase
      if /([^ATGC\n])/i.match?(seq)
        redirect_to '/'
        flash[:danger] = 'Target Sequence contains non-DNA characters!'
      elsif @submission.save
        outputfile = "lib/python_scripts/output/crispy-results-000#{@submission.id}.txt"
        params = {
          submission_type: 'custom',
          sequence: seq,
          genome: @submission.genome,
          pam: @submission.pam_sequence,
          spacer: @submission.spacer_length,
          target: 'gene',
          outputfile: outputfile,
          submission_id: @submission.id
        }

        Submission.cleanup('000' + @submission.id.to_s)
        CrispyService.crispy(params)
        render status: :ok, json: { message: 'success', id: @submission.id }.to_json
      else
        render status: :internal_server_error, json: { message: 'Unable to submit run', errors: @submission.errors.to_hash }.to_json
      end
    else # gene submission
      zymo_strain = Strain.find_by(name: 'ZM4')
      strain_name = nil
      @strain_set = nil
      if resource_params[:strain_id].to_i == zymo_strain.id
        strain_name = 'ZYMOMONAS'
      else
        strain = Strain.find(@submission.strain_id)
        strain_name = strain.name
        @strain_set = strain.strain_set
      end

      if @submission.save!

        outputfile = "lib/python_scripts/output/crispy-results-#{@submission.id}.txt"
        blast_output_file = "lib/python_scripts/output/crispy-results-#{@submission.id}_blast.txt"
        params = {
          submission_type: 'gene',
          gene: Gene.find(@submission.gene_id).name,
          pam: @submission.pam_sequence,
          spacer: @submission.spacer_length,
          strain: strain_name,
          strain_set: @strain_set,
          target: 'gene',
          outputfile: outputfile,
          submission_id: @submission.id,
          search_human_genome: @submission.search_human_genome,
          blast_output_file: blast_output_file
        }
        # CrispyStubService.crispy(params)
        CrispyService.crispy(params)
        Submission.cleanup(@submission.id)

        render status: :ok, json: { message: 'success', id: @submission.id }.to_json
      else
        render status: :internal_server_error, json: { message: 'Unable to submit run', errors: @submission.errors.to_hash }.to_json
      end
    end
  end

  def destroy
    @submission.destroy
    respond_to do |format|
      format.html { redirect_to submissions_url, notice: 'Submission was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private

  def limit_saved_submissions
    Submission.order('created_at DESC').offset(10).destroy_all
  end

  def set_resource
    @submission = Submission.find(params[:id])
  end

  def resource_params
    params.require(:submission)
          .permit(:submission_type, :sequence, :genome, :gene_id, :strain_id, :pam_sequence,
            :spacer_length, :target_type, :strain_set, :search_human_genome,
            :target_name, :pos_in_gene)
  end
end
