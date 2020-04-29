module ResultsHelper
  def draw_alignment(topseq, botseq)
    alignment_lines = ''
    topchars = topseq.split('')
    botchars = botseq.split('')
    (0..topchars.length - 1).each do |i|
      if topchars[i] == botchars[i]
        alignment_lines += '|'
      else
        alignment_lines += ' '
      end
    end

    "        Guide RNA:     #{topseq}\n                         #{alignment_lines}\n           Target:       #{botseq}"
  end
end
