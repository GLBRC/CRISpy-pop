class Submission < ApplicationRecord
  has_many :results, dependent: :destroy, class_name: 'Result'
  belongs_to :gene, optional: true
  belongs_to :strain, optional: true
  validates :pam_sequence, :spacer_length, presence: true

  def self.cleanup(run_id)
    Dir.glob("lib/python_scripts/tmp/*-#{run_id}*.txt").each { |file| File.delete(file) }
    Dir.glob("lib/python_scripts/output/*-#{run_id}*.txt").each { |file| File.delete(file) }
    Dir.glob("lib/python_scripts/output/*-#{run_id}*.fa").each { |file| File.delete(file) }
  end
end
