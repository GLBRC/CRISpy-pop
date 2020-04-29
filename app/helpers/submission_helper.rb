module SubmissionHelper
  def count_coverage(cov_string, strain)
    if cov_string.present?
      strain_count = cov_string.squish.split(',').uniq.count
      all_strains_count = Strain.where(strain_set: strain.strain_set).count
      "#{strain_count} / #{all_strains_count}"
    else
      "1 / #{all_strains_count}"
    end
  end

  def coverage_num(cov_string)
    cov_string.squish.split(',').uniq.count
  end
end
