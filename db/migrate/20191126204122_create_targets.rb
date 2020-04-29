class CreateTargets < ActiveRecord::Migration[6.0]
  def change
    create_table :targets do |t|
      t.string :name
      t.text :comments

      t.timestamps
    end
  end
end
