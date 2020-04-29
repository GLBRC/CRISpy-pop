FactoryBot.define do
  factory :thousand_strain, class: 'Strain' do
    name { %w[EXF-5046 C-6 CD7-9SV2 SA.9.2.BL3 Y6_B].sample }
    strain_set { '1011genomes' }
    description { 'great strain' }
  end
end
