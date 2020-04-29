Rails.application.configure do
  config.generators do |g|
    g.orm             :active_record
    g.template_engine :erb
    g.test_framework  false
    g.assets          false
    g.helper          false
    g.jbuilder        false
    g.scaffold_stylesheet false
  end
end
