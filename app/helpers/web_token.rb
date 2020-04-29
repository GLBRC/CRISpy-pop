module WebToken
  def self.web_token
    RequestStore.store[:token]
  end

  def self.web_token=(token)
    RequestStore.store[:token] = token
  end
end
