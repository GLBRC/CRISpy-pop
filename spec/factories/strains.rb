FactoryBot.define do
  thousand_strains = []
  CSV.foreach('lib/tasks/strains_1011_list.tab', col_sep: "\t") do |row|
    strain_name = row[0]
    thousand_strains << strain_name
  end

  strains = []
  CSV.foreach('lib/tasks/strain_list.tab', col_sep: "\t") do |row|
    strain_name = row[0]
    strains << strain_name unless thousand_strains.include?(strain_name)
  end

  factory :strain do
    name { strains.sample }
    strain_set { 'GLBRC' }
    description { 'Regular Strain' }
  end
end
