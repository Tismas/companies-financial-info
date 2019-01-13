import React from 'react';

import './__styles__/loader.css';

export default (props) => {
    return (
        <div className="lds-grid">
            {
                new Array(9)
                    .fill(0)
                    .map((e, i) => <div key={i} />)
            }
        </div>
    );
}