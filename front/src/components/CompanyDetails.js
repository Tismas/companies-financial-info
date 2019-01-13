import React, { Component } from 'react';
import { Line } from 'react-chartjs-2';

import './__styles__/company-details.css';

const chartLines = [
  { label: 'open', color: 'red' },
  { label: 'high', color: 'green' },
  { label: 'low', color: 'blue' },
  { label: 'close', color: 'orange' }
]

const Info = (props) => (
  <div className="company-data-info">
    <div className="company-data-info-label">{props.label}</div>
    <div className="company-data-info-value">{props.value}</div>
  </div>
)

export default class CompanyDetails extends Component {
  render() {
    const { companyData, quoteData } = this.props;
    const { logo, name, symbol, domain, marketOpen, marketClose } = companyData;
    if (!name) {
      return null;
    }
    const labels = Object.keys(quoteData).map(e => e.split(" ")[1].substr(0, 5));
    const chartData = {
      labels,
      datasets: chartLines.map(({label, color}, i) => ({
        label,
        fill: false,
        lineTension: 0.1,
        borderColor: color,
        data: Object.keys(quoteData).map(e => quoteData[e][`${i + 1}. ${label}`])
      }))
    }
    const volumeData = {
      labels,
      datasets: [{
        label: 'volume',
        fill: false,
        lineTension: 0.1,
        borderColor: 'black',
        data: Object.keys(quoteData).map(e => quoteData[e][`5. volume`])
      }]
    }

    return (
      <div className="company-details">
        <div className="company-data-container">
          <img src={logo} alt={name} className="company-data-image" />
          <Info label="Symbol" value={symbol} />
          <Info label="Name" value={name} />
          <Info label="Website" value={domain} />
          <Info label="Trading hours" value={`${marketOpen} - ${marketClose}`} />
        </div>
        <div className="quote-data-container">
          <Line data={chartData} />
          <Line data={volumeData} />
        </div>
      </div>
    );
  }
}