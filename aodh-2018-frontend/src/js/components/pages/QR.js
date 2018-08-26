import React, { Component } from "react";
import qrcode from "../../../images/qr-code.png";

export default class About extends Component {

  render() {
    return (
      <div className="QR">
        <font color="#444444">
        <br />
        Share this QR-code of this site to your friends!
        <br /><br />
        <img src={qrcode} /*style={imgStyle}*/ alt="qr" />
        <br />
        <br />
        <br />
        <br />

        </font>
      </div>
    );
  }
}
