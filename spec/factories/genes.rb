FactoryBot.define do
  s288c_genes = []
  CSV.foreach('lib/reference/yeast_genes.bed', col_sep: "\s") do |row|
    gene_name = row[3]
    s288c_genes << gene_name
  end

  factory :gene do
    name { s288c_genes.sample }
    description { 'S. cerevisiae' }
    genome { 'S288C' }
    start_pos { 52_000 }
    end_pos { 54_000 }
    chrom { 'X' }
  end
end
