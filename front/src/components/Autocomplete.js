import React, { Component, Fragment } from 'react';

import './__styles__/autocomplete.css';

class App extends Component {
  state = { symbol: '' }

  componentDidMount() {
    window.addEventListener('keydown', this.keyDownHandler);
  }
  componentWillUnmount() {
    window.removeEventListener('keydown', this.keyDownHandler);
  }

  keyDownHandler = (e) => {
    if (e.code === 'Escape') {
      this.props.hideAutocompleteList();
    }
  }

  handleChange = (e) => {
    const symbol = e.target.value;
    this.props.updateAutocomplete(symbol);
    this.setState({ symbol });
  }

  handleSelection = (autocompleteEntry) => {
    this.setState({ symbol: autocompleteEntry.name });
    this.props.handleSelection(autocompleteEntry);
  }

  render() {
    const { symbol } = this.state;
    const { autocompleteData } = this.props;
    return (
      <Fragment>
        {autocompleteData.length > 0 && <div className="autocomplete-overlay" onClick={this.props.hideAutocompleteList} />}
        <div className="autocomplete-container">
          <input value={symbol} onChange={this.handleChange} className="autocomplete-input" placeholder="Company symbol" />
          {autocompleteData.length > 0 &&
            <div className="autocomplete-entries">
              {autocompleteData.map((e, i) => (
                <div key={e.name + e.symbol + i} className="autocomplete-entry" onClick={this.handleSelection.bind(this, e)}>
                  <div> {e.name} </div>
                  <div> {e.symbol} </div>
                </div>
              ))}
            </div>
          }
        </div>
      </Fragment>
    );
  }
}

export default App;
