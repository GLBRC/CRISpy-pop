FactoryBot.define do
  factory :user, aliases: %i[creator submitter preparer] do
    # Requiring unique first and last names was causing errors in
    # CI test runs, so remove that constraint, and just make sure
    # username is unique.
    # sequence :display_name do |n|
    #   "Display ##{n}"
    # end
    # sequence :username do |n|
    #   "user_#{n}"
    # end
    display_name { "Diplay Name #{Time.now.to_f}" }
    username { "User_Name_#{Time.now.to_f}" }
    provider { 'GLBRC' }
    uid { SecureRandom.uuid }
    # If username is unique, then email is guaranteed to be unique.
    email { "#{username}@glbrc.org" }

    password { Devise.friendly_token[0, 20] }
    factory :admin_user do
      after(:create) do |user|
        user.roles << Role.find_or_create_by(name: 'Admin')
      end
    end
  end
end
