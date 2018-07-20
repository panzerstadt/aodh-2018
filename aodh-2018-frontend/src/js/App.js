import React, { Component } from "react";
import Main from "./components/Main";
import Header from "./components/Header";
import Footer from "./components/Footer";
import "../style/css/App.css";

class App extends Component {
  render() {
    return (
      <div className="App mdl-main">
        <Header />
        <Main />
        <Footer />
      </div>
    );
  }
}

export default App;
