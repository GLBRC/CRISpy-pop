class Gene < ApplicationRecord
  validates :name, :start_pos, :end_pos, :chrom, presence: true
end
