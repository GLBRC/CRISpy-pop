class OffsiteSearch < ApplicationRecord
  validates :sgrna_sequence, :genome, presence: true
  has_many :offsite_hits, dependent: :destroy

  def self.cleanup(run_id)
    Dir.glob("lib/python_scripts/tmp/*-#{run_id}*.txt").each { |file| File.delete(file) }
    Dir.glob("lib/python_scripts/output/*-#{run_id}*.txt").each { |file| File.delete(file) }
  end
end
