import React, { Component } from "react";
import Typography from "@material-ui/core/Typography";
import qrcode from "../../../images/qr-code.png";

const qrStyle = {
  root: {
    height: "100%",
    width: "100%",
    justifyContent: "center"
  },
  text: {
    display: "flex",
    padding: 30,
    justifyContent: "center"
  },
  qr: {
    paddingTop: 100
  }
};

export default class About extends Component {
  render() {
    return (
      <div className="QR" style={qrStyle.root}>
        <Typography component="div" style={qrStyle.text} color="textSecondary">
          Share this QR-code of this site to your friends!
        </Typography>

        <img style={qrStyle.qr} src={qrcode} /*style={imgStyle}*/ alt="qr" />
      </div>
    );
  }
}
