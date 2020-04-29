class CreateSubmissions < ActiveRecord::Migration[6.0]
  def change
    create_table :submissions do |t|
      t.string :submission_type
      t.integer :gene_id
      t.string :pam_sequence
      t.integer :spacer_length
      t.integer :strain_id
      t.string :target_type
      t.string :created_by
      t.integer :search_human_genome
      t.text :sequence
      t.string :genome
      t.string :target_name

      t.timestamps
    end
  end
end
