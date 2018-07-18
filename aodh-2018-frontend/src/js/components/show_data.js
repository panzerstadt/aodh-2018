import React, { Component } from 'react';
import logo from '../../images/logo.svg';
import '../../style/css/show_data.css';

// do logic here


class ShowData extends Component {
  render() {
    return (
      <div className="show_data">
        <img src={logo} className="App-logo" alt="logo" />
        <h1 className="App-title">Welcome to React</h1>
        <p className="App-intro">
          this is the data page
        </p>
      </div>
    );
  }
}

export default ShowData;
