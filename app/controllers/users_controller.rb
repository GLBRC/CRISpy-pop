class UsersController < ApplicationController
  before_action :set_and_authorize_user, only: %i[show edit update destroy]
  # before_action :authorize_resource, except: [:show, :edit, :update, :destroy]
  # before_action :load_data, except: %i[index destroy]

  # render index.html
  def index
    @users = User.all
  end

  def show
    @user = User.find(params['id'])
  end

  def edit
    @roles_selected = @user.roles.map { |r| { value: r.id, label: r.name } } # for react component
    @roles = Role.all.map { |r| { value: r.id, label: r.name } }
  end

  # render new.rhtml
  def new
    @user = User.new
  end

  def create
    @user = User.new(resource_params)
  end

  def update
    if @user.update(resource_params)
      @user.save!
      flash[:notice] = 'User roles successfully updated'
      redirect_to(current_user.admin? ? users_path : @user)
    else
      render action: 'edit'
    end
  end

  def destroy
    @user.destroy
    redirect_to users_path
  end

  # protected

  # def load_data
  #   @roles = Role.all
  # end

  private

  def resource_params
    params.require(:user).permit(:display_name, :email, :username, role_ids: [])
  end

  def set_and_authorize_user
    authorize @user = User.find(params[:id])
  end
end
