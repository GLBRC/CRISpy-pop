FactoryBot.define do
  factory :submission do
    association :gene
    association :strain
    pam_sequence { 'NGG' }
    spacer_length { 20 }
    target_type { 'gene' }
    created_by { 'Admin' }
  end
end
