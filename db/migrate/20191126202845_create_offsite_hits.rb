class CreateOffsiteHits < ActiveRecord::Migration[6.0]
  def change
    create_table :offsite_hits do |t|
      t.string :sgrna_sequence
      t.integer :offsite_search_id
      t.string :chrom
      t.integer :pos
      t.string :strand
      t.integer :mismatches
      t.string :name

      t.timestamps
    end
  end
end
