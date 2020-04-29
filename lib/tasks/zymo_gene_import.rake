namespace :import do
  desc 'import zymomonas genes. Usage: rake import:zymo_genes'
  task zymo_genes: :environment do
    # read in the z mobilis genes
    Gene.transaction do
      CSV.foreach('lib/reference/ZYMOMONAS.bed', col_sep: "\s") do |row|
        genome = row[0]
        gene_name = row[4]
        ## need to rerun this to get the chrom I out of there
        Gene.find_or_create_by(start_pos: row[1], end_pos: row[2], chrom: 'ZM4', name: gene_name,
                               genome: genome, has_intron: false, has_5_utr: false)
      end
    end
  end

  desc 'import zymomonas strains. Usage: rake import:zymo_strains'
  task zymo_strains: :environment do
    Strain.find_or_create_by(name: 'ZM4', description: 'Z. mobilis strain ZM4')
  end
end
