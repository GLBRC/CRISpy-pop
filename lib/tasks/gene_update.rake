namespace :update do
  desc 'update genes list. Usage: rake update:genes'
  task genes: :environment do
    puts 'Updating Genes..'
    gene_ids = Submission.all.pluck(:gene_id)

    Gene.where.not(id: gene_ids).destroy_all

    used_genes = {}
    Gene.all.each do |g|
      if used_genes.key?(g.name)
        used_genes[g.name] << g.genome
      else
        used_genes[g.name] = [g.genome]
      end
    end

    intron_utr = {}
    # read in the intron/UTR file that species which genes have extra annotation
    # different target types are conditionally available
    CSV.foreach('lib/reference/intron-fivePrimeUTR.table', col_sep: "\s") do |row|
      gene_name = row[0]
      annotation_type = row[1]

      if intron_utr.key?(gene_name)
        if annotation_type == 'intron'
          intron_utr[gene_name][:has_intron] = true
        else
          intron_utr[gene_name][:has_utr] = true
        end
      elsif annotation_type == 'intron'
        intron_utr[gene_name] = { has_intron: true, has_utr: nil }
      else
        intron_utr[gene_name] = { has_intron: nil, has_utr: true }
      end
    end

    Gene.transaction do
      CSV.foreach('lib/reference/yeast_genes.bed', col_sep: "\s") do |row|
        hi = intron_utr.key?(row[3]) ? intron_utr[row[3]][:has_intron] : nil
        hu = intron_utr.key?(row[3]) ? intron_utr[row[3]][:has_utr] : nil

        if used_genes[row[3]].nil?
          Gene.find_or_create_by(start_pos: row[1], end_pos: row[2],
                                 chrom: row[0], name: row[3], genome: 'S288C', has_intron: hi, has_5_utr: hu)
        elsif used_genes[row[3]].include?('S288C')
          puts 'Gene record in use'
        else
          Gene.find_or_create_by(start_pos: row[1], end_pos: row[2],
                                 chrom: row[0], name: row[3], genome: 'S288C', has_intron: hi, has_5_utr: hu)
        end
      end
    end
    Gene.transaction do
      CSV.foreach('lib/reference/y22-3_genes.bed', col_sep: "\s") do |row|
        if used_genes[row[3]].nil?
          Gene.find_or_create_by(start_pos: row[1], end_pos: row[2],
                                 chrom: row[0], name: row[3], genome: 'Y22-3')
        elsif used_genes[row[3]].include?('Y22-3')
          puts 'Gene record in use'
        else
          Gene.find_or_create_by(start_pos: row[1], end_pos: row[2],
                                 chrom: row[0], name: row[3], genome: 'Y22-3')
        end
      end
    end
    puts 'Done Updating genes'
  end
end
