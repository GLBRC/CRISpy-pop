import React, { Component } from "react";
import PropTypes from "prop-types";
import igv from "tmp_es6_igv";
// yarn add tmp_es6_igv for es6 support and import

const igvStyle = {
  paddingTop: "10px",
  paddingBottom: "10px",
  margin: "8px",
  border: "1px solid lightgray",
  maxHeight: "400px",
  overflowY: "scroll"
};

class IgvBrowser extends Component {
  componentDidMount() {
    const igvContainer = document.getElementById("igv-div");
    let fastaURL = "/S288C_reference_sequence_R64-1-1_20110203.fasta";
    let genesBed = "/yeast_genes.bed";
    let geneTrackName = "S. cerevisiae S288C Genes";
    const {
      strainName, chromStart, locusStart, locusEnd
    } = this.props;
    const locus = chromStart + ":" + locusStart + "-" + locusEnd;
    // eslint crashes if using the preferred syntax.  Apparently can't handle strings that
    // look like ranges?
    // const locus = `${chromStart}:${locusStart}-${locusEnd}`;

    if (strainName === "GLBRCY22-3") {
      fastaURL = "/GLBRCY22-3.fasta";
      genesBed = "/y22-3_genes.bed";
      geneTrackName = "S. cerevisiae GLBRCY22-3 Genes";
    } else if (strainName === "ZM4") {
      fastaURL = "/ZYMOMONAS.fasta";
      genesBed = "/ZYMOMONAS.bed";
      geneTrackName = "Z. Mobilis ZM4 Genes";
    } else if (strainName === "CUSTOM") {
      fastaURL = "/custom.fasta";
      genesBed = "";
      geneTrackName = "Custom target";
    }

    const igvOptions = {
      palette: ["#00A0B0", "#6A4A3C", "#CC333F", "#EB6841"],
      locus,
      reference: {
        id: "S288C",
        fastaURL,
        tracks: [
          {
            name: "Generated sgRNAs Forward Strand",
            url: "/generated_sgrna_coords_pos.bed",
            displayMode: "EXPANDED"
          },
          {
            name: geneTrackName,
            color: "red",
            url: genesBed,
            displayMode: "EXPANDED"
          },
          {
            name: "Generated sgRNAs Reverse Strand",
            url: "/generated_sgrna_coords_neg.bed",
            color: "purple",
            displayMode: "EXPANDED"
          },
          {
            name: "S. cerevisiae Introns",
            color: "DarkOrange",
            url: "/yeast_introns.bed",
            displayMode: "EXPANDED"
          }
        ]
      }
    };
    // dont show gene and intron tracks for custom
    if (strainName === "CUSTOM") {
      igvOptions.reference.tracks.splice(1, 1);
      igvOptions.reference.tracks.splice(2, 1);
    }
    return igv.createBrowser(igvContainer, igvOptions);
  }

  render() {
    return (
      <div id="igv-div" style={igvStyle} />
    );
  }
}

IgvBrowser.propTypes = {
  strainName: PropTypes.string.isRequired,
  chromStart: PropTypes.string.isRequired,
  locusStart: PropTypes.string.isRequired,
  locusEnd: PropTypes.string.isRequired
};

export default IgvBrowser;
