Rails.application.routes.draw do
  root to: 'submissions#new'

  get '/index', to: 'pages#index'
  get '/about', to: 'pages#about'
  get '/help' => 'pages#help', as: 'help'
  get '/glbrc_strains' => 'pages#glbrc_strains', as: 'glbrc_strains'
  get '/thousand_genome_strains' => 'pages#thousand_genome_strains', as: 'thousand_genome_strains'
  post '/results/export', to: 'results#export', as: 'checked_result'

  resources :messages, only: %i[new create]
  resources :users, only: %i[index show edit update]
  resources :submissions do
    post :stub_create, on: :member
  end
  resources :genes do
    get :get, on: :collection
  end
  resources :results do
    get :export, on: :collection
  end
  resources :strains, only: %i[index]
  resources :offsite_searches

  get '/status', to: 'api/v1/status#status'
  namespace :api do
    namespace :v1 do
      get '/status', to: 'status#status'
    end
  end
end
