require 'rails_helper'

module Systems
  module SessionHelpers
    # NOTE:  After using sign_in, regular_sign_in, or custodian_sign_in,
    #        subsequent sign_ins must be done using sign_in_as, since it's
    #        the only method that signs out the previous user first.
    def self.included(base)
      base.before { @user = nil }
      base.after { sign_out @user if @user }
    end

    def admin_sign_in
      @user = create(:admin_user)
      sign_in @user
      @user
    end

    def regular_sign_in
      @user = create(:user)
      sign_in @user
      @user
    end

    def login(user)
      visit '/users/sign_in'
      fill_in 'Username', with: user.username
      fill_in 'Password', with: user.password
      click_button 'Sign in'
      expect(page).to have_current_path(root_path)
    end

    def sign_in_as(user)
      sign_out(@user) if @user
      @user = user
      sign_in @user
      @user
    end

    # # Sign out currently signed-in user through the UI
    # def sign_out
    #   find('.dropdown-toggle').click
    #   find('#log_out_link', visible: false).click
    #   @user = nil
    # end
  end
end

# Including Requests::SessionHelpers allows tests to use
# sign_in(user) instead of going through the UI sign-in
# process above, BUT the sign-in must be done before each
# test (i.e. it doesn't persist if done in before(:all),
# for some reason).
module Requests
  module SessionHelpers
    include Warden::Test::Helpers

    def self.included(base)
      base.before { Warden.test_mode! }
      base.after { Warden.test_reset! }
    end

    def sign_in(resource)
      login_as(resource, scope: warden_scope(resource))
    end

    def sign_out(resource)
      logout(warden_scope(resource))
    end

    private

    def warden_scope(resource)
      resource.class.name.underscore.to_sym
    end
  end
end
