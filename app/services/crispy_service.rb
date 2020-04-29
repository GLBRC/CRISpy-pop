class CrispyService
  def self.crispy(run_params)
    if run_params[:submission_type] == 'gene'
      gene = run_params[:gene]
      pam = run_params[:pam]
      spacer = run_params[:spacer]
      strain = run_params[:strain]
      strain_set = run_params[:strain_set]
      target = run_params[:target]
      outputfile = run_params[:outputfile]
      blast_output_file = run_params[:blast_output_file]
      submission_id = run_params[:submission_id]
      search_human_genome = run_params[:search_human_genome]
      strain_set = 'GLBRC' if strain == 'ZYMOMONAS'
      # python2.7 crispy.py -h. usage: crispy.py -g geneName -p PAM sequence -l spacer length -n strainName -t target(cds)
      if search_human_genome
        command = "python #{Rails.root.join('lib', 'python_scripts', 'crispy.py')} -g #{gene} -pr #{strain_set.upcase} -p #{pam} -l #{spacer} -n #{strain} -t #{target} -r #{submission_id} -b"
      else
        command = "python #{Rails.root.join('lib', 'python_scripts', 'crispy.py')} -g #{gene} -pr #{strain_set.upcase} -p #{pam} -l #{spacer} -n #{strain} -t #{target} -r #{submission_id}"
      end

      `#{command}` # run it

      coverage = {}
      unless strain == 'ZYMOMONAS'
        File.open("lib/python_scripts/tmp/sgRNA_list_matching_strains-#{submission_id}.txt", 'r').each do |line|
          lineparts = line.split(':')
          coverage[lineparts[0]] = lineparts[1]
        end
      end

      human_hits = []
      if search_human_genome
        CSV.foreach(blast_output_file, col_sep: "\t", headers: false) do |row|
          human_hits << row[0]
        end
      end

      CSV.foreach(outputfile, col_sep: "\t", headers: true) do |row|
        # GeneID sgRNA %Activity %GC chrom pos position_w/in_gene MisMatchseq strand numMisMatches numOffSiteMatch
        gene_id = Gene.find_by(name: gene).id
        Result.create(name: row[0], gene_id: gene_id, sgrna_sequence: row[1], perc_activity: row[2], gc: row[3], chrom: row[4],
                      pos: row[5], pos_in_gene: row[6], mismatch_seq: row[7], strand: row[8], num_mis_matches: row[9], num_off_site_match: row[10],
                      strains_covered: row[11], submission_id: submission_id, strain_coverage: coverage[row[1]].nil? ? nil : coverage[row[1]],
                      has_human_hit: human_hits.include?(row[0]))
      end
    elsif run_params[:submission_type] == 'offsite'
      outputfile = run_params[:outputfile]
      sgrna_sequence = run_params[:sgrna_sequence]
      pam_sequence = run_params[:pam]
      genome = run_params[:genome]
      offsite_search_id = run_params[:offsite_search_id]
      command = "python #{Rails.root.join('lib', 'python_scripts', 'crispy.py')} -sg #{sgrna_sequence} -p #{pam_sequence} -r #{offsite_search_id} -ref #{genome}"

      `#{command}` # run it

      CSV.foreach(outputfile, col_sep: "\t") do |row|
        coord_end = row[2].to_i + row[0].length
        hit_name = "#{row[1]}:#{row[2]}-#{coord_end}"
        OffsiteHit.create(name: hit_name, sgrna_sequence: row[0], chrom: row[1], pos: row[2], strand: row[4],
                          mismatches: row[5], offsite_search_id: offsite_search_id)
      end
    elsif run_params[:submission_type] == 'custom'
      sequence = run_params[:sequence]
      genome = run_params[:genome]
      pam_sequence = run_params[:pam]
      spacer = run_params[:spacer]
      target = run_params[:target]
      outputfile = run_params[:outputfile]
      submission_id = run_params[:submission_id]
      run_id = '000' + submission_id.to_s
      command = "python #{Rails.root.join('lib', 'python_scripts', 'crispy.py')} -seq #{sequence} -ref #{genome} -p #{pam_sequence} -l #{spacer} -t #{target} -r #{run_id}"

      `#{command}` # run it

      CSV.foreach(outputfile, col_sep: "\t", headers: true) do |row|
        if genome == 'None'
          # GeneID sgRNA %Activity %GC chrom pos position_w/in_gene strand NumReferenceMatches
          Result.create!(name: row[0], sgrna_sequence: row[1], perc_activity: row[2], gc: row[3],
                         pos_in_gene: row[6], strand: row[7], submission_id: submission_id)

        else
          offsite_matches = row[8]
          # GeneID sgRNA %Activity %GC chrom pos position_w/in_gene strand NumReferenceMatches
          r = Result.new(name: "#{row[0]}_#{row[6]}", sgrna_sequence: row[1], perc_activity: row[2], gc: row[3], chrom: row[4],
                         pos: row[5], pos_in_gene: row[6], strand: row[7], num_off_site_match: offsite_matches, submission_id: submission_id)
          r.save!
        end
      end

    end
  end
end
