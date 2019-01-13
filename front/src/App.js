import React, { Component } from 'react';
import { Grid, Row, Col } from 'react-bootstrap';
import { throttle } from 'lodash';

import Autocomplete from './components/Autocomplete'

import './__styles__/App.css';

class App extends Component {
  state = { autocompleteData: [], cache: {} }

  updateAutocomplete = throttle(async (symbol) => {
    const response = await fetch(`http://localhost:5000/symbols?symbol=${symbol}`)
    const data = await response.json();
    this.setState({ autocompleteData: data.bestMatches })
  }, 500)

  handleSelection = (symbolData) => {
    console.log(symbolData);
    this.setState({ autocompleteData: [] });
  }

  render() {
    const { autocompleteData } = this.state;
    return (
      <Grid>
        <Row>
          <Col xs={10} xsoffset={1}>
            <Autocomplete
              autocompleteData={autocompleteData}
              updateAutocomplete={this.updateAutocomplete}
              handleSelection={this.handleSelection}
            />
          </Col>
        </Row>
      </Grid>
    );
  }
}

export default App;
