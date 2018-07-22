import React, { Component } from "react";
import { Link } from "react-router-dom";

import logo from "../../images/logo.svg";
import Button from "@material-ui/core/Button";

class Header extends Component {
  render() {
    return (
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <h1 className="App-title">Sentiments in AR</h1>
      </header>
    );
  }
}

export default Header;
