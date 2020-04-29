class CrispyStubService
  def self.crispy(run_params)
    if run_params[:submission_type] == 'gene'
      gene_id = run_params[:gene_id]
      # pam = run_params[:pam]
      # spacer = run_params[:spacer]
      # strain = run_params[:strain]
      # strain_set = run_params[:strain_set]
      # target = run_params[:target]
      # outputfile = run_params[:outputfile]
      # blast_output_file = run_params[:blast_output_file]
      submission_id = run_params[:submission_id]
      # search_human_genome = run_params[:search_human_genome]
      # strain_set = 'GLBRC' if strain == 'ZYMOMONAS'

      gene_id = Gene.find_by(id: gene_id)

      10.times do
        FactoryBot.create(:result, gene_id: gene_id, submission_id: submission_id)
      end
      # Result.create(name: row[0], gene_id: gene_id, sgrna_sequence: row[1],
      #              perc_activity: row[2], gc: row[3], chrom: row[4],
      #              pos: row[5], pos_in_gene: row[6], mismatch_seq: row[7],
      #              strand: row[8], num_mis_matches: row[9], num_off_site_match: row[10],
      #              strains_covered: row[11], submission_id: submission_id,
      #              strain_coverage: coverage[row[1]].nil? ? nil : coverage[row[1]],
      #              has_human_hit: human_hits.include?(row[0]))

    elsif run_params[:submission_type] == 'offsite'
      # outputfile = run_params[:outputfile]
      # sgrna_sequence = run_params[:sgrna_sequence]
      # pam_sequence = run_params[:pam]
      # genome = run_params[:genome]
      # offsite_search_id = run_params[:offsite_search_id]

    elsif run_params[:submission_type] == 'custom_target'
      # sequence = run_params[:sequence]
      # genome = run_params[:genome]
      # pam_sequence = run_params[:pam]
      # spacer = run_params[:spacer]
      # target = run_params[:target]
      # outputfile = run_params[:outputfile]
      submission_id = run_params[:submission_id]
      # run_id = '000' + submission_id.to_s

      10.times do
        FactoryBot.create(:result, submission_id: submission_id)
      end
    end
  end
end
