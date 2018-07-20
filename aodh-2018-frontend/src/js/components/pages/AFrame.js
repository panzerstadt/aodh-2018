import React, { Component } from "react";
import ReactHtmlParser, {
  processNodes,
  convertNodeToElement,
  htmlparser2
} from "react-html-parser";

import Button from "@material-ui/core/Button";

// import aframe_html from "../../../data/aframe-html/aframe.html";
const webpage = "https://latestcode.glitch.me";

export default class AFrame extends Component {
  render() {
    const { data } = this.props;

    return (
      <div className="page-size">
        <Button variant="contained" color="primary">
          <a href={webpage} target="_blank">
            link to aframe
          </a>
        </Button>
      </div>
    );
  }
}
