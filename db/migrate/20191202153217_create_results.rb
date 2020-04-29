class CreateResults < ActiveRecord::Migration[6.0]
  def change
    create_table :results do |t|
      t.integer :gene_id
      t.string :sgrna_sequence
      t.decimal :perc_activity
      t.string :chrom
      t.integer :pos
      t.string :mismatch_seq
      t.string :strand
      t.integer :num_mis_matches
      t.integer :num_off_site_match
      t.integer :submission_id
      t.string :gc
      t.text :strain_coverage
      t.string :state
      t.string :name
      t.integer :pos_in_gene
      t.text :comments
      t.integer :strains_covered
      t.integer :has_human_hit

      t.timestamps
    end
  end
end
