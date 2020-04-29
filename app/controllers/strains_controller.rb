class StrainsController < ApplicationController
  def index
    @glbrc_strains = Strain.where(strain_set: 'GLBRC')
    @thousand_genome_strains = Strain.where(strain_set: '1011genomes')
  end

  private

  def set_and_authorize_resource
    authorize @strain = Strain.find(params[:id])
  end

  def resource_params
    params.require(:strain).permit(:name, :description)
  end
end
