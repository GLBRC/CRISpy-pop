class CreateGenes < ActiveRecord::Migration[6.0]
  def change
    create_table :genes do |t|
      t.string :name
      t.text :description
      t.string :genome
      t.integer :start_pos
      t.integer :end_pos
      t.string :chrom
      t.integer :has_intron
      t.integer :has_5_utr

      t.timestamps
    end
  end
end
