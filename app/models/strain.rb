class Strain < ApplicationRecord
  validates :name, presence: true
  scope :yeast, -> { where("name != 'ZM4'") }
  scope :zymo, -> { where("name = 'ZM4'") }
end
