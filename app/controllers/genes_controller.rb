class GenesController < ApplicationController
  before_action :set_and_authorize_resource, only: %i[show edit update destroy]
  # before_action :authorize_resource, except: %i[show edit update destroy]

  def index
    @genes = Gene.order(:name)
    @genes = @genes.where('name like ?', "%#{params[:term]}%") if params[:term]
  end

  def show
    @gene = Gene.find(params[:id])
  end

  def get
    @gene = Gene.find(params[:gene_id])

    # has_intron,, has_5_utr
    # Target.id, Target.name
    names = ['gene']
    names << 'intron' if @gene.has_intron?
    names << 'five_prime_UTR_intron' if @gene.has_5_utr?

    @targets = Target.where(name: names)
    @targets = @targets.map { |t| { id: t.id, name: t.name } }

    respond_to do |format|
      format.json { render json: @targets }
    end
  end

  def set_and_authorize_resource
    authorize @gene = Gene.find(params[:id])
  end

  def resource_params
    params.require(:gene).permit(:gene_id, :chrom, :has_intron, :has_5_utr, :start_pos, :end_pos, :genome)
  end
end
