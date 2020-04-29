source 'https://rubygems.org'
git_source(:github) { |repo| "https://github.com/#{repo}.git" }

ruby '2.6.4'

gem 'activerecord-session_store'
gem 'bootsnap', '>= 1.4.2', require: false
gem 'bootstrap-kaminari-views'
gem 'bootstrap_form'
gem 'devise'
gem 'haml-rails'
gem 'httparty'
gem 'jbuilder', '~> 2.7'
gem 'lograge'
gem 'net-ldap'
gem 'pandoc-ruby'
gem 'puma', '~> 3.11'
gem 'pundit'
gem 'rails', '~> 6.0.0'
gem 'react-rails'
gem 'request_store'
gem 'skylight'
gem 'sqlite3', '~> 1.4'
gem 'turbolinks', '~> 5'
gem 'tzinfo-data', platforms: %i[mingw mswin x64_mingw jruby]
gem 'webpacker', '~> 4.0'
gem 'webtoken'

group :production do
  gem 'passenger'
end

group :development, :test, :oracle_test do
  gem 'brakeman'
  gem 'bundler-audit'
  gem 'byebug', platforms: %i[mri mingw x64_mingw]
  gem 'factory_bot_rails'
  gem 'faker'
  gem 'launchy'
  gem 'letter_opener'
  gem 'parallel_tests'
  gem 'pry-rails'
  gem 'rspec-rails', '~> 3.8'
  gem 'rubocop', '~> 0.81.0', require: false
  gem 'rubocop-performance', require: false
  gem 'rubocop-rails', require: false
  gem 'rubocop-rspec', require: false
end

group :development do
  gem 'listen', '>= 3.0.5', '< 3.2'
  gem 'spring'
  gem 'spring-watcher-listen', '~> 2.0.0'
  gem 'web-console', '>= 3.3.0'
end

group :test, :oracle_test do
  gem 'capybara', '>= 2.15'
  gem 'database_cleaner'
  gem 'selenium-webdriver'
  gem 'webdrivers'
end
