class CreateOffsiteSearches < ActiveRecord::Migration[6.0]
  def change
    create_table :offsite_searches do |t|
      t.string :sgrna_sequence
      t.string :genome
      t.string :pam_sequence

      t.timestamps
    end
  end
end
