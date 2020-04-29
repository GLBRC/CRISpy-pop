class OffsiteSearchesController < ApplicationController
  skip_before_action :verify_authenticity_token, only: [:create]

  def show
    # byebug
    @offsite_search = OffsiteSearch.find(params[:id])
    @offsite_hits = @offsite_search.offsite_hits
    if @offsite_hits.first.nil?
      @chrom_start = 'I'
      @locus_start = 50
      @locus_end = 70
    else
      @chrom_start = @offsite_hits.first.chrom
      @locus_start = @offsite_hits.first.pos - 50
      @locus_end = @offsite_hits.first.pos + 50
      @sgrna_length = @offsite_hits.first.sgrna_sequence.length

      File.open('public/offsite_hits_pos.bed', 'w+') do |f|
        @offsite_hits.each do |osh|
          if osh.strand == '+'
            chromend = osh.pos.to_i + osh.sgrna_sequence.length.to_i
            f << "#{osh.chrom}\t#{osh.pos}\t#{chromend}\t#{osh.name}\n"
          end
        end
      end
      File.open('public/offsite_hits_neg.bed', 'w+') do |f|
        @offsite_hits.each do |osh|
          next unless osh.strand == '-'

          start_pos = osh.pos.to_i + @offsite_search.pam_sequence.length
          chromend = start_pos + osh.sgrna_sequence.length.to_i
          f << "#{osh.chrom}\t#{start_pos}\t#{chromend}\t#{osh.name}\n"
        end
      end
    end
  end

  def create
    @offsite_search = OffsiteSearch.new(resource_params)
    if /[^ATGCNRTV]/i.match?(@offsite_search.sgrna_sequence)
      redirect_to '/'
      flash[:danger] = 'sgRNA Sequence contains non-DNA characters!'
    elsif @offsite_search.save
      @outputfile = "lib/python_scripts/tmp/sg-#{@offsite_search.id}-offinder.txt"
      params = {
        submission_type: 'offsite',
        outputfile: @outputfile,
        sgrna_sequence: @offsite_search.sgrna_sequence,
        pam: @offsite_search.pam_sequence,
        genome: @offsite_search.genome,
        offsite_search_id: @offsite_search.id
      }
      CrispyService.crispy(params)
      OffsiteSearch.cleanup(@offsite_search.id.to_s)
      render status: :ok, json: { message: 'success', id: @offsite_search.id }.to_json
    else
      render status: :internal_server_error, json: { message: 'Unable to submit run', errors: @offsite_search.errors.to_hash }.to_json
    end
  end

  private

  def set_and_authorize_resource
    authorize @offsite_search = OffsiteSearch.find(params[:id])
  end

  def resource_params
    params.require(:offsite_search).permit(:sgrna_sequence, :genome, :pam_sequence)
  end
end
