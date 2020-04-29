class ApplicationMailer < ActionMailer::Base
  default from: 'noreply@glbrc.org'
  default to: APP_CONFIG[:service_desk_email]
  layout 'mailer'
end
