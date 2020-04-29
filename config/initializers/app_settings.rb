class RequiredSettingNotFound < StandardError
end
class UnknownSettingFound < StandardError
end

# Load settings.yml into APP_CONFIG constant
begin
  APP_CONFIG = YAML.load(ERB.new(File.read("#{::Rails.root}/config/settings.yml")).result)[::Rails.env].symbolize_keys
rescue StandardError
  Rails.logger.error "Error reading settings file.\nCheck config/settings.yml.sample for more information"
end

# Set CMD_PATH for external commands.
# TODO: replace CMD_PATH with ffi gem for ucsc bindings
CMD_PATH = ::Rails.root.to_s + '/lib/tasks/' unless defined? CMD_PATH

# flag for remote_user timeout method. see devise.rb  application_controller.rb
# unused - foo@dev only forces authentication for chrome, firefox, windows-safari.  No Difference: opera, mac-safari. Error: i.e.
# APP_CONFIG[:force_url] = false
# ActiveRecord::Base.include_root_in_json = false

required_keys = %i[host site_name service_desk_email site_description]
optional_keys = %i[db_dump_dir]

missing_keys = required_keys - APP_CONFIG.keys
unknown_keys = APP_CONFIG.keys - required_keys - optional_keys

raise RequiredSettingNotFound, ('Required Keys not found in settings.yml: ' + missing_keys.join(', ')) unless missing_keys.empty?

raise UnknownSettingFound, ('Unknown keys found in settings.yml not added to initializers/app_settings.rb: ' + unknown_keys.join(', ')) unless unknown_keys.empty?
