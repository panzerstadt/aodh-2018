import React, { Component } from "react";
import { Link } from "react-router-dom";

import logo from "../../images/logo.svg";
import Button from "@material-ui/core/Button";

class Header extends Component {
  render() {
    return (
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1 className="App-title">team Standy 2018</h1>
        <Button variant="outlined" color="primary">
          <Link to="/tweets"> Tweets </Link>
        </Button>
        <Button variant="outlined" color="primary">
          <Link to="/images"> Images </Link>
        </Button>
      </header>
    );
  }
}

export default Header;
