import React, { Component } from "react";
import logo from "../../images/logo.svg";
import "../../style/css/show_data.css";

import fetchData from "../actions/index";

// do logic here

class ShowData extends Component {
  // perform fetchdata here

  render() {
    return (
      <div className="show_data">
        <img src={logo} className="App-logo" alt="logo" />
        <h1 className="App-title">Welcome to React</h1>
        <p className="App-intro">this is where the data is shown</p>
        <p>fetchData calls the API and puts it here</p>
      </div>
    );
  }
}

export default ShowData;
