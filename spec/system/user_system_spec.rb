require 'rails_helper'

RSpec.describe 'User', type: :system do
  let!(:user) { create(:user) }

  before do
    sign_in_as(user)
  end

  context 'when signed in' do
    it 'won\'t show admin menu to non-admin users' do
      visit users_path
      expect(page).not_to have_content 'Admin'
    end

    it 'will show admin menu to admin users' do
      user.make_admin
      visit users_path
      expect(page).to have_content 'Admin'
    end
  end
end
