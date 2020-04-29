class ResultsController < ApplicationController
  def show
    @result = Result.find(params[:id])
    @submission = Submission.find(@result.submission_id)
    @strain = Strain.find(@submission.strain_id)
    @covered = nil

    @covered = if @result.strain_coverage.nil?
                 [@strain.name]
               else
                 @result.strain_coverage.squish.split(',').uniq
               end
    @not_covered = Strain.where.not(name: @covered).pluck(:name)

    if @not_covered.length > @covered.length
      (@not_covered.length - @covered.length).times do
        @covered << nil
      end
    end
    @list = @covered.zip(@not_covered)
  end

  def edit
    # set state of result to indicate it has been used in the lab
    @result = Result.find(params[:id])
    @result.state = 'Used'
    @result.save
    redirect_to :back
  end

  def update
    @result = Result.find(params[:id])
    @result.comments = params[:result][:comments]
    @result.save!
    redirect_to :back
  end

  def export
    return if params[:checked_ids].blank?

    @results = Result.find(params[:checked_ids].split(',').map(&:to_i))
    pam = params[:pam]
    target_name = params[:target_name]
    data = Result.export(@results, pam, target_name)
    if @results
      render status: :ok, json: { data: data }.to_json
    else
      render status: :not_found, json: { message: 'data not found' }
    end
  end

  private

  def set_and_authorize_resource
    authorize @result = Result.find(params[:id])
  end

  def resource_params
    params.require(:result).permit(:gene_id, :sgrna_sequence, :perc_activity,
      :chrom, :pos, :mismatch_seq, :strand,
      :num_mis_matches, :num_off_site_match,
      :submission_id, :gc, :strain_coverage, :comments)
  end
end
