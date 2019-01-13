import React, { Component } from 'react';
import { Grid, Row, Col } from 'react-bootstrap';
import { throttle } from 'lodash';

import Autocomplete from './components/Autocomplete';
import Loader from './components/Loader';

import './__styles__/App.css';

class App extends Component {
  state = { autocompleteData: [], cache: {}, companyData: {}, loading: false }

  updateAutocomplete = throttle(async (symbol) => {
    const response = await fetch(`http://localhost:5000/symbols?symbol=${symbol}`);
    const data = await response.json();
    this.setState({ autocompleteData: data.bestMatches });
  }, 500)

  handleSelection = async (symbolData) => {
    this.setState({ autocompleteData: [], loading: true });

    const symbol = symbolData.symbol;
    const response = await fetch(`http://localhost:5000/quote?symbol=${symbol}`);
    const data = await response.json();
    this.setState({ companyData: data, loading: false });
  }

  render() {
    const { autocompleteData, loading } = this.state;
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
        <Row>
          {loading ? <Loader /> : 'loaded'}
        </Row>
      </Grid>
    );
  }
}

export default App;
