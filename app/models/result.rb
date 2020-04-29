class Result < ApplicationRecord
  belongs_to :submission
  belongs_to :gene, optional: true
  validates :name, :sgrna_sequence, presence: true

  def self.export(results, pam, target_name, options = { headers: true })
    CSV.generate(options) do |csv|
      csv << ['Name', 'sgRNA Sequence', 'Reverse Complement', 'PAM Site', 'Percent Activity',
              'GC%', 'Chromosome', 'Position', 'Position in Gene', 'Strand', 'Num Mismatches', 'Off-Site Matches', 'Has Human hits?']
      results.each do |r|
        revcom = r.sgrna_sequence[0...-pam.length].reverse.tr('ATCG', 'TAGC')
        if target_name == 'gene'
          tname = r.name
        else
          tname = "#{target_name}:#{r.name}"
        end

        csv << [tname, r.sgrna_sequence[0...-pam.length], revcom, r.sgrna_sequence.last(pam.length),
                r.perc_activity, r.gc, r.chrom, r.pos, r.pos_in_gene, r.strand, r.num_mis_matches,
                r.num_off_site_match, r.has_human_hit? ? 'Yes' : 'No']
      end
    end
  end
end
