# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)

puts '***RUNNING RAKE TASKS***'

print 'Importing Genes...'
Rake::Task['import:genes'].invoke
puts 'done'

print 'Updating genes..'
Rake::Task['update:genes'].invoke
puts 'done'

print 'Importing Strains...'
Rake::Task['import:strains'].invoke
puts 'done'

print 'Updating Strains...'
Rake::Task['update:strain_names'].invoke
puts 'done'

print 'Importing Targets...'
Rake::Task['import:targets'].invoke
puts 'done'

print 'Importing zymomonas genes'
Rake::Task['import:zymo_genes'].invoke
puts 'done'

print 'Importing zymomonas strains'
Rake::Task['import:zymo_strains'].invoke
puts 'done'

print 'Importing thousand strains'
Rake::Task['import:thousand_strains'].invoke
puts 'done'
