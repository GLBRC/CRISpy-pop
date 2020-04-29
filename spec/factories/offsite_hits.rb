FactoryBot.define do
  factory :offsite_hit do
    sgrna_sequence { 'AGGCATGCATCAGCACCAGT' }
    association :offsite_search
    chrom { 'I' }
    pos { 1 }
    strand { 'Forward' }
    mismatches { 1 }
  end
end
