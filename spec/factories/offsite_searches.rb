FactoryBot.define do
  factory :offsite_search do
    sgrna_sequence { 'GACTAGCTAAGCATCAG' }
    genome { 'HOG1' }
  end
end
