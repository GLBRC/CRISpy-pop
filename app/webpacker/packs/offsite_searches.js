import $ from "jquery";
import igv from "tmp_es6_igv";

var div = $("#browser")[0];
let fastaURL = "/S288C_reference_sequence_R64-1-1_20110203.fasta";
let genesBed = "/yeast_genes.bed";
let geneTrackName = "S. cerevisiae S288C Genes";

if (genome == 'Y22-3') {
  fastaURL = "/GLBRCY22-3.fasta";
  genesBed = "/y22-3_genes.bed";
  geneTrackName = "S. cerevisiae GLBRCY22-3 Genes";
}
else if (genome == 'Saccharomyces_paradoxus') {
  fastaURL = "/Saccharomyces_paradoxus_converted.fasta";
  genesBed = "/blank.bed";
  geneTrackName = "S. paradoxus genes";
}
else if (genome == 'kluuveromyces_lactis') {
  fastaURL = "/kluuveromyces_lactis.fasta";
  genesBed = "/blank.bed";
  geneTrackName = "K. lactis genes";
}
else if (genome == 'ZYMOMONAS') {
  fastaURL = "/ZYMOMONAS.fasta";
  genesBed = "/ZYMOMONAS.bed";
  geneTrackName = "Z. mobilis genes";
}
const locus =  chromStart + ":" + locusStart + "-" + locusEnd;
const options = {
        palette: ["#00A0B0", "#6A4A3C", "#CC333F", "#EB6841"],

        locus: locus,

        reference: {
            id: "S288C",
            fastaURL: fastaURL
        },

        trackDefaults: {
            bam: {
                coverageThreshold: 0.2,
                coverageQualityWeight: true
            }
        },

        tracks: [
            {
                name: "Offsite Hits Forward Strand",
                url: "/offsite_hits_pos.bed",
                displayMode: "EXPANDED"
            },
            {
                name: "Offsite Hits Reverse Strand",
                url: "/offsite_hits_neg.bed",
                color: "purple",
                displayMode: "EXPANDED"
            },
            {
                name: geneTrackName,
                color: "red",
                url: genesBed,
                displayMode: "EXPANDED"
            },
            {
                name: "S. cerevisiae Introns",
                color: "DarkOrange",
                url: "/yeast_introns.bed",
                displayMode: "EXPANDED"
            }
        ]
    };
igv.createBrowser(div, options);

$( ".zoomButton" ).click(function() {
  zoomViewer($(this).attr('pos'), $(this).attr('chrom'));
});

function zoomViewer(position, chrom) {
  const startCoord = parseInt(position) - 10;
  const len = parseInt(sgrnaLength);
  const endCoord = parseInt(position) + len + 10;
  const locusString = chrom + ":" + startCoord + "-" + endCoord;
  igv.browser.search(locusString);
  $("html, body").animate({ scrollTop: 0 }, "medium");
}
