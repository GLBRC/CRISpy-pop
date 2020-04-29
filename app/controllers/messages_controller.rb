class MessagesController < ApplicationController
  def index
    @messages = policy_scope(Ahoy::Message).page(params[:page]).per(10)
  end

  def show
    authorize @message = Ahoy::Message.find(params[:id])
  end

  def new
    @message = Message.new
  end

  def create
    @message = Message.new(resource_params)
    @message.content = "Feedback sent from <a href=\"#{@message.current_page}\">#{@message.current_page}</a><br>#{@message.content}"

    if @message.valid?
      MessageMailer.help_email(@message).deliver_now
      flash[:success] = 'Your message has been sent.'
    else
      flash[:danger] = 'An error occurred while delivering this message.'
    end

    redirect_to root_path
  end

  private

  def resource_params
    params.require(:message).permit(:name, :email, :content, :current_page)
  end
end
