import React from "react";
import PropTypes from "prop-types";
import igv from "tmp_es6_igv";
import ReactTable from "react-table-v6";
import "react-table-v6/react-table.css";
import {
  Row, Col, Button, Input
} from "reactstrap";
import IgvBrowser from "./IgvBrowser.jsx";
// yarn add tmp_es6_igv for es6 support and import

class SubmissionShow extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      allSelected: false
    };
    this.toggleSelected = this.toggleSelected.bind(this);
  }

  zoomViewer(position) {
    const startCoord = parseInt(position, 10) - 10;
    const endCoord = parseInt(position, 10) + this.props.spacerLength + 10;
    // have to use string concat to get through eslint
    const locusString = this.props.chromStart + ":" + startCoord + "-" + endCoord;
    igv.browser.search(locusString);
    window.scrollTo(0, 0);
  }

  export() {
    const selectedIds = [];
    const checked = document.querySelectorAll("input[type='checkbox']:checked");

    for (let i = 0; i < checked.length; i++) {
      selectedIds.push(checked[i].value);
    }

    fetch(`${this.props.host}/results/export?checked_ids=${selectedIds}&pam=${this.props.pam}&target_name=${this.props.targetName}`)
      .then((response) => response.json())
      .then((responseJson) => {
        const csvContent = "data:text/csv;charset=utf-8," + responseJson.data;
        const encodedUri = encodeURI(csvContent);
        window.open(encodedUri);
      }).catch((error) => {
        console.error(error);
      });
  }

  toggleSelected() {
    const checkboxes = document.querySelectorAll("input[type='checkbox']");
    for (let i = 0; i < checkboxes.length; i++) {
      if (this.state.allSelected === true) {
        checkboxes[i].checked = false;
        this.setState({ allSelected: false });
      } else {
        checkboxes[i].checked = true;
        this.setState({ allSelected: true });
      }
    }
  }

  countUnique(iterable) {
    return new Set(iterable).size;
  }

  countCoverage(covString) {
    let displayString = "";
    if (covString) {
      const strainCount = this.countUnique(covString.trim().split(","));
      displayString = `${strainCount} / ${this.props.allStrainsCount}`;
    } else {
      displayString = `1 / ${this.props.allStrainsCount}`;
    }
    return displayString;
  }

  render() {
    const {
      strainName, chromStart, locusStart, locusEnd, results
    } = this.props;

    let accessor = "";
    if (this.props.targetName === "CUSTOM") {
      accessor = "pos_in_gene";
    } else {
      accessor = "pos";
    }

    const columns = [{
      Header: "",
      accessor: "id",
      Cell: (row) => (
        <div className="text-center">
          <Input type="checkbox" name="selected" value={row.value} defaultChecked={false} />
        </div>
      ),
      minWidth: 50
    }, {
      Header: "Name",
      accessor: "name",
      minWidth: 170,
      Cell: (row) => (
        <a href={this.props.host + "/results/" + row.original.id} className="btn btn-primary" target="_blank" rel="noopener noreferrer">{row.value}</a>
      )
    }, {
      Header: "sgRNA Sequence",
      accessor: "sgrna_sequence",
      minWidth: 180,
      Cell: (row) => (
        `${row.value.slice(0, -3)}`
      )
    }, {
      Header: "PAM Site",
      accessor: "sgrna_sequence",
      Cell: (row) => (
        `${row.value.substring(row.value.length - 3, row.value.length)}`
      )
    }, {
      Header: "Go To",
      minWidth: 65,
      accessor,
      Cell: (row) => (
        <div className="text-center">
          <Button color="primary" onClick={() => { this.zoomViewer(row.value); }}>Go</Button>
        </div>
      )

    },
    {
      Header: "Activity Score",
      accessor: "perc_activity",
      minWidth: 100
    }, {
      Header: "GC%",
      accessor: "gc",
      width: 50
    }, {
      Header: "Chrom",
      accessor: "chrom",
      minWidth: 60
    }, {
      Header: "Position",
      accessor: "pos",
      width: 75
    }, {
      Header: "Position In Gene",
      accessor: "pos_in_gene",
      minWidth: 120
    }, {
      Header: "Strand",
      accessor: "strand",
      width: 75
    }, {
      Header: "Mismatches",
      accessor: "num_mis_matches",
      minWidth: 90
    }, {
      Header: "Off-site Matches",
      accessor: "num_off_site_match",
      minWidth: 120,
      Cell: (row) => (
        <div style={{
          backgroundColor: row.value > 0 ? "red" : "",
          color: row.value > 0 ? "white" : "",
          textAlign: "center"
        }}
        >
          {row.value}
        </div>
      )
    }, {
      Header: "Human Hits?",
      accessor: "has_human_hit",
      Cell: (row) => (
        row.value === 1 ? "Yes" : "No"
      )
    }, {
      Header: "Strains Covered",
      accessor: "strain_coverage",
      Cell: (row) => (
        <div>
          {this.countCoverage(row.value)}
        </div>
      )
    }

    ];

    return (
      <div>
        <Row>
          <Col md={12}>
            <IgvBrowser
              strainName={strainName}
              chromStart={chromStart}
              locusStart={locusStart}
              locusEnd={locusEnd}
            />
          </Col>
        </Row>
        <br />
        <Row>
          <Col md={4}>
            <div>
              <Button onClick={() => { this.toggleSelected(); }}>Select All</Button>
              &nbsp;&nbsp;
              <Button color="primary" onClick={() => { this.export(); }}>Export</Button>
              &nbsp;&nbsp;
              Click on column headers to sort
            </div>
          </Col>
        </Row>
        <br />
        <Row>
          <Col md={12}>
            <ReactTable
              data={results}
              columns={columns}
            />
          </Col>
        </Row>
      </div>
    );
  }
}

SubmissionShow.propTypes = {
  strainName: PropTypes.string.isRequired,
  chromStart: PropTypes.string.isRequired,
  locusStart: PropTypes.string.isRequired,
  locusEnd: PropTypes.string.isRequired,
  results: PropTypes.arrayOf(PropTypes.object).isRequired,
  spacerLength: PropTypes.number.isRequired,
  allStrainsCount: PropTypes.number.isRequired,
  pam: PropTypes.string.isRequired,
  targetName: PropTypes.string.isRequired,
  host: PropTypes.string.isRequired
};

export default SubmissionShow;
