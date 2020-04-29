Rails.application.configure do
  config.lograge.enabled = true
  config.lograge.ignore_actions = ['API::V1::StatusController#status']
  config.lograge.custom_options = lambda do |event|
    unwanted_keys = %w[format action controller _method]
    params = event.payload[:params].reject { |key, _| unwanted_keys.include? key }

    # capture some specific timing values you are interested in
    {
      params: params,
      event_time: Time.now.iso8601,
      exception: event.payload[:exception], # ["ExceptionClass", "the message"]
      exception_object: event.payload[:exception_object] # the exception instance
    }
  end
end
