namespace :import do
  desc 'import strains. Usage: rake import:strains'
  task strains: :environment do
    CSV.foreach('lib/tasks/strain_list.tab', headers: false) do |row|
      Strain.find_or_create_by(name: row[0])
    end
  end

  desc 'import 1011 strains. Usage: rake import:thousand_strains'
  task thousand_strains: :environment do
    CSV.foreach('lib/tasks/strains_1011_list.tab', headers: false) do |row|
      Strain.create(name: row[0], strain_set: '1011genomes')
    end
    glbrc = Strain.where(strain_set: nil)
    glbrc.each do |s|
      Strain.update(s.id, strain_set: 'GLBRC')
    end
  end

  desc 'import targets. Usage: rake import:targets'
  task targets: :environment do
    CSV.foreach('lib/tasks/target_list.tab', headers: false) do |row|
      Target.find_or_create_by(name: row[0])
    end
  end

  desc 'import genes. Usage: rake import:genes'
  task genes: :environment do
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

        Gene.find_or_create_by(start_pos: row[1], end_pos: row[2],
                               chrom: row[0], name: row[3], genome: 'S288C', has_intron: hi, has_5_utr: hu)
      end
    end
    Gene.transaction do
      CSV.foreach('lib/reference/y22-3_genes.bed', col_sep: "\s") do |row|
        Gene.find_or_create_by(start_pos: row[1], end_pos: row[2],
                               chrom: row[0], name: row[3], genome: 'Y22-3')
      end
    end
  end
end

namespace :update do
  desc 'update strain names'
  task strain_names: :environment do
    s = Strain.find_by(name: 'Y22-3')
    unless s.nil?
      s.name = 'GLBRCY22-3'
      s.save!
    end
  end
end
