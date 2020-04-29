import React, { useState, useEffect } from "react";
import Select, { createFilter } from "react-select";
import PropTypes from "prop-types";
import {
  TabContent, TabPane, Nav, NavItem, NavLink, Button, CardBody, Row, Col, Form, FormGroup, Input, Label
} from "reactstrap";
import classnames from "classnames";

const CrispySubmissionForm = (props) => {
  const [activeTab, setActiveTab] = useState("1");
  const [isLoading, setIsLoading] = useState(false);
  const hv = {
    strain_id: null, gene_id: null, pam_sequence: "NGG", target_type: "gene", spacer_length: "20", search_human_genome: "0"
  };
  const [yeastFormOptions, setYeastFormOptions] = useState(hv);

  // There's only one strain; so this could be hardcoded.
  const useStrainId = props.strains.zymo[0].id;
  const zymoGeneDefault = props.genes.zymo[0].id;
  const zv = {
    strain_id: useStrainId, gene_id: zymoGeneDefault, pam_sequence: "NGG", spacer_length: "20", search_human_genome: "0"
  };
  const [zymoFormOptions, setZymoFormOptions] = useState(zv);

  const ov = { sgrna_sequence: "", pam_sequence: "NGG", genome: "S288C" };
  const [offsiteFormOptions, setOffsiteFormOptions] = useState(ov);

  const [customFormOptions, setCustomFormOptions] = useState({
    target_name: "", sequence: "", pam_sequence: "NGG", spacer_length: "20", genome: "S288C"
  });
  // For the "Target Custom Sequence" tab.

  const toggle = (tab) => {
    if (activeTab !== tab) setActiveTab(tab);
  };

  // Starts out without a yeast strain selected.
  const [yeastGenesForSelect, setYeastGenesForSelect] = useState(null);
  const [geneInputLength, setGeneInputLength] = useState(0);

  const setFormValues = (controlId, fieldToSet, valueToSet) => {
    if (controlId.startsWith("yeast")) {
      const formOptions = yeastFormOptions;
      formOptions[fieldToSet] = valueToSet;
      setYeastFormOptions(formOptions);
    } else if (controlId.startsWith("zymo")) {
      const formOptions = zymoFormOptions;
      formOptions[fieldToSet] = valueToSet;
      setZymoFormOptions(formOptions);
    } else if (controlId.startsWith("offsite")) {
      const formOptions = offsiteFormOptions;
      formOptions[fieldToSet] = valueToSet;
      setOffsiteFormOptions(formOptions);
    } else if (controlId.startsWith("custom")) {
      const formOptions = customFormOptions;
      formOptions[fieldToSet] = valueToSet;
      setCustomFormOptions(formOptions);
    }
  };

  const handleGeneSelection = (event, whichForm) => {
    setFormValues(whichForm, "gene_id", event.value);
  };

  const handlePAMSequenceSelection = (event) => {
    setFormValues(event.target.id, "pam_sequence", event.target.value);
  };

  const handleSetSpacerLength = (event) => {
    setFormValues(event.target.id, "spacer_length", event.target.value);
  };

  const handleToggleHumanGenome = (event) => {
    const searchHumanGenome = (event.target.checked) ? "1" : "0";
    setFormValues(event.target.id, "search_human_genome", searchHumanGenome);
  };

  const handleSgRNASeq = (event) => {
    setFormValues(event.target.id, "sgrna_sequence", event.target.value);
  };

  const handleGenomeSelection = (event) => {
    setFormValues(event.target.id, "genome", event.target.value);
  };

  const handleSetTargetName = (event) => {
    setFormValues(event.target.id, "target_name", event.target.value);
  };

  const handleSetSequence = (event) => {
    setFormValues(event.target.id, "sequence", event.target.value);
  };

  let yeastGeneOptions = []; // empty unless a strain is selected.
  if ((yeastFormOptions.strain_id !== "0") && (yeastGenesForSelect)) {
    yeastGeneOptions = yeastGenesForSelect.map((item) => (
      { value: item.id, label: item.name }
    ));
  }

  const zymoStrainOptions = props.strains.zymo.map((item) => (
    { label: item.name, value: item.id }
  ));

  const zymoGeneOptions = props.genes.zymo.map((item) => (
    { label: item.name, value: item.id }
  ));

  const pamSeqOptions = ["NGG", "NNGRRT", "TTTV", "NNNNGATT", "NNAGAAW"].map((item) => {
    return <option key={`pamSeq${item}`} value={item}>{ item }</option>;
  });

  const yeastStrainOptions = props.strains.yeast.map((item) => (
    { label: item.name, value: item.id }
  ));

  const targetTypeOptions = (<option key="targetTypeGene" value="gene"> Gene </option>);

  const [formData, setFormData] = useState(false);

  //
  // Events
  //
  const toggleLoading = (whichForm) => {
    if (isLoading === false) {
      setIsLoading(true);
      document.getElementById("spinner").style.visibility = "visible";
    }
    let formOptions;
    if (whichForm === "yeast") {
      formOptions = yeastFormOptions;
    } else if (whichForm === "zymo") {
      formOptions = zymoFormOptions;
    } else if (whichForm === "offsite") {
      formOptions = offsiteFormOptions;
    } else if (whichForm === "custom") {
      formOptions = customFormOptions;
    }
    setFormData(Object.assign(formOptions, { submission_type: whichForm }));
  };

  const handleStrainSelection = (event, whichForm) => {
    if (whichForm === "yeast") {
      const selectedStrainName = event.label;
      const genesAvailable = (selectedStrainName === "GLBRCY22-3") ? props.genes.yeast.y22_3 : props.genes.yeast.s288c;
      setYeastGenesForSelect(genesAvailable);
    }
    setFormValues(whichForm, "strain_id", event.value);
  };

  //
  // Effects
  //
  useEffect(() => {
    if (!formData) {
      return;
    }
    let url;
    const st = formData.submission_type;
    let requestBody = formData;
    if (formData.submission_type === "offsite") {
      url = `${props.host}/offsite_searches`;
      delete requestBody.submission_type;
      requestBody = { offsite_search: requestBody };
    } else {
      url = `${props.host}/submissions`;
      requestBody = { submission: requestBody };
    }
    console.log(url);
    fetch(url, {
      method: "post",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requestBody)
    })
      .then((res) => res.json())
      .then((response) => {
        if (response.message === "success") {
          if (st === "offsite") {
            window.location.href = `${props.host}/offsite_searches/${response.id}`;
          } else {
            window.location.href = `${props.host}/submissions/${response.id}`;
          }
        }
      })
      .catch((error) => console.log(error));
  }, [formData]);

  return (
    <div>
      <Nav tabs>
        <NavItem>
          <NavLink
            className={classnames({ active: activeTab === "1" })}
            onClick={() => { toggle("1"); }}
          >
            Target A Gene - S. cerevisiae
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink
            className={classnames({ active: activeTab === "2" })}
            onClick={() => { toggle("2"); }}
          >
            Target A Gene - Z. mobilis
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink
            className={classnames({ active: activeTab === "3" })}
            onClick={() => { toggle("3"); }}
          >
            Offsite Target Search
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink
            className={classnames({ active: activeTab === "4" })}
            onClick={() => { toggle("4"); }}
          >
            Target Custom Sequence
          </NavLink>
        </NavItem>
      </Nav>
      <TabContent activeTab={activeTab}>
        <TabPane tabId="1">
          <Form>
            <Row>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>Strain</b></Label>
                  <Select
                    filterOption={createFilter({ ignoreAccents: false })}
                    id="yeastStrain"
                    onChange={(e) => handleStrainSelection(e, "yeast")}
                    options={yeastStrainOptions}
                  />
                </FormGroup>
              </Col>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>Gene</b></Label>
                  { ((geneInputLength < 2) && (yeastFormOptions.strain_id !== "0"))
                  && <span className="geneLengthNotice">Please enter 2 or more characters</span>}
                  <Select
                    filterOption={createFilter({ ignoreAccents: false })}
                    value={yeastFormOptions.gene}
                    menuIsOpen={geneInputLength > 1}
                    onChange={(e) => handleGeneSelection(e, "yeast")}
                    onInputChange={(e) => setGeneInputLength(e.length)}
                    isDisabled={yeastFormOptions.strain_id === "0"}
                    id="yeastGene"
                    options={yeastGeneOptions}
                  />
                </FormGroup>
              </Col>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>PAM Sequence</b></Label>
                  <Input type="select" name="select" id="yeastPAMSequence" onChange={handlePAMSequenceSelection}>
                    { pamSeqOptions }
                  </Input>
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>Target Type</b></Label>
                  <Input type="select" name="select" id="yeastTargetType">
                    { targetTypeOptions }
                  </Input>
                </FormGroup>
              </Col>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>Spacer Length</b></Label>
                  <Input
                    type="number"
                    name="number"
                    id="yeastSpacerLength"
                    defaultValue="20"
                    min="14"
                    max="100"
                    step="1"
                    onChange={handleSetSpacerLength}
                  />
                </FormGroup>
              </Col>
              <Col sm="3" className="text-left">
                <FormGroup check>
                  <div className="hg-checkbox">
                    <Label check>
                      <Input type="checkbox" id="yeastSearchHumanGenome" onChange={handleToggleHumanGenome} value="1" />
                      {" "}
                      <b>Search human genome</b>
                    </Label>
                  </div>
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col>
                <Button onClick={() => { toggleLoading("yeast"); }}>Find Target Sites</Button>
              </Col>
            </Row>
          </Form>
        </TabPane>
        <TabPane tabId="2">
          <Form>
            <Row>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>Strain</b></Label>
                  <Select
                    id="zymoStrain"
                    filterOption={createFilter({ ignoreAccents: false })}
                    options={zymoStrainOptions}
                  />
                </FormGroup>
              </Col>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>Gene</b></Label>
                  { geneInputLength < 2 && zymoFormOptions.strain_id !== "0"
                  && <span className="geneLengthNotice">Please 2 or more characters</span>}
                  <Select
                    id="zymoGene"
                    filterOption={createFilter({ ignoreAccents: false })}
                    menuIsOpen={geneInputLength > 1}
                    onChange={(e) => handleGeneSelection(e, "zymo")}
                    onInputChange={(e) => setGeneInputLength(e.length)}
                    isDisabled={zymoFormOptions.strain_id === "0"}
                    options={zymoGeneOptions}
                  />
                </FormGroup>
              </Col>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>PAM Sequence</b></Label>
                  <Input type="select" name="select" id="zymoPAMSequence" onChange={handlePAMSequenceSelection}>
                    { pamSeqOptions }
                  </Input>
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>Spacer Length</b></Label>
                  <Input
                    type="number"
                    name="number"
                    id="zymoSpacerLength"
                    defaultValue="20"
                    min="14"
                    max="100"
                    onChange={handleSetSpacerLength}
                  />
                </FormGroup>
              </Col>
              <Col sm="3" className="text-left">
                <FormGroup check>
                  <div className="hg-checkbox">
                    <Label check>
                      <Input type="checkbox" id="zymoSearchHumanGenome" onChange={handleToggleHumanGenome} />
                      {" "}
                      <b>Search human genome</b>
                    </Label>
                  </div>
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col>
                <Button onClick={() => { toggleLoading("zymo"); }}>Find Target Sites</Button>
              </Col>
            </Row>
          </Form>
        </TabPane>
        <TabPane tabId="3">
          <Form>
            <Row>
              <CardBody>
                <div className="text-left">
                  <p>Input sgRNA sequence to search for offsite hits.</p>
                  <p>Include the PAM sequence in the input field and select the appropriate pattern from the dropdown.</p>
                  <p>
                    E.g. AAAAAGCAATGGAGGAACGG
                    <span className="text-danger">TGG</span>
                  </p>
                </div>
              </CardBody>
            </Row>
            <Row>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>sgRNA Sequence</b></Label>
                  <Input type="text" name="sgrna_sequence" id="offsiteSgRNASeq" onChange={handleSgRNASeq} />
                </FormGroup>
              </Col>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>PAM Sequence</b></Label>
                  <Input type="select" name="select" id="offsitePamSeqSelect" onChange={handlePAMSequenceSelection}>
                    { pamSeqOptions }
                  </Input>
                </FormGroup>
              </Col>
              <Col sm="3" className="text-left">
                <FormGroup>
                  <Label><b>Genome</b></Label>
                  <Input type="select" name="select" id="offsiteGenomeSelect" onChange={handleGenomeSelection}>
                    <option>S288C</option>
                    <option>Y22-3</option>
                    <option>Saccharomyces_paradoxus</option>
                    <option>Saccharomyces_eubayanus</option>
                    <option>kluuveromyces_lactis</option>
                    <option>ZM4</option>
                  </Input>
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col>
                <Button onClick={() => { toggleLoading("offsite"); }}>Search for Offsite Binding Sites</Button>
              </Col>
            </Row>
          </Form>
        </TabPane>
        <TabPane tabId="4">
          <Form>
            <Row>
              <Col sm="6" className="text-left">
                <FormGroup>
                  <Label><b>Target Name</b></Label>
                  <Input type="text" placeholder="custom_target" name="targetname" id="customTargetName" onChange={handleSetTargetName} />
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col sm="6" className="text-left">
                <FormGroup>
                  <Label><b>Sequence</b></Label>
                  <Input type="textarea" name="sequenceTxt" rows="9" id="customSequence" onChange={handleSetSequence} />
                </FormGroup>
              </Col>
              <Col sm="4" className="text-left">
                <Row>
                  <Col>
                    <FormGroup>
                      <Label><b>PAM Sequence</b></Label>
                      <Input type="select" name="select" id="customPamSeqSelect" onChange={handlePAMSequenceSelection}>
                        { pamSeqOptions }
                      </Input>
                    </FormGroup>
                  </Col>
                </Row>
                <Row>
                  <Col className="text-left">
                    <FormGroup>
                      <Label><b>Spacer Length</b></Label>
                      <Input
                        type="number"
                        name="number"
                        id="customSpacerLength"
                        defaultValue="20"
                        min="14"
                        max="100"
                        onChange={handleSetSpacerLength}
                      />
                    </FormGroup>
                  </Col>
                </Row>
                <Row>
                  <Col className="text-left">
                    <FormGroup>
                      <Label><b>Genome</b></Label>
                      <Input type="select" name="select" id="customGenomeSelect" onChange={handleGenomeSelection}>
                        <option>None</option>
                        <option>S288C</option>
                        <option>Y22-3</option>
                        <option>Saccharomyces_paradoxus</option>
                        <option>kluuveromyces_lactis</option>
                      </Input>
                    </FormGroup>
                  </Col>
                </Row>
              </Col>
            </Row>
            <br />
            <br />
            <Row>
              <Col>
                <Button onClick={() => { toggleLoading("custom"); }}>Find Target Sites</Button>
              </Col>
            </Row>
          </Form>
        </TabPane>
      </TabContent>
    </div>
  );
};

CrispySubmissionForm.propTypes = {
  genes: PropTypes.object.isRequired,
  host: PropTypes.string.isRequired,
  strains: PropTypes.object.isRequired
};

export default CrispySubmissionForm;
