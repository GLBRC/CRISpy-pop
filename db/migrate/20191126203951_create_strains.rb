class CreateStrains < ActiveRecord::Migration[6.0]
  def change
    create_table :strains do |t|
      t.string :name
      t.text :description
      t.string :vcf_file
      t.string :strain_set

      t.timestamps
    end
  end
end
