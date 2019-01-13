import React, { Component } from 'react';
import { Grid, Row, Col } from 'react-bootstrap'

import './App.css';

class App extends Component {
  render() {
    return (
      <Grid>
        <Row>
          <Col xs={10} xsoffset={1}>
            <input className="symbol-input" placeholder="Company symbol" />
          </Col>
        </Row>
      </Grid>
    );
  }
}

export default App;
