class API::V1::StatusController < ApplicationController
  def status
    head 200, content_type: 'text/html'
  end
end
