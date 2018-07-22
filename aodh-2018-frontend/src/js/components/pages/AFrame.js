import React, { Component } from "react";
import ReactHtmlParser, {
  processNodes,
  convertNodeToElement,
  htmlparser2
} from "react-html-parser";

import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import Divider from "@material-ui/core/Divider";

import JapanIcon from "../../../images/jp.png";
import KoreaIcon from "../../../images/kr.png";
import TaiwanIcon from "../../../images/tw.png";

// import aframe_html from "../../../data/aframe-html/aframe.html";
const webpage_shibuya = "https://ambiguous-vein-rshubuya.glitch.me";
const webpage_harajuku = "https://ambiguous-vein-harajuku.glitch.me";
const webpage_taipei = "https://ambiguous-vein-taiwan.glitch.me";
const webpage_tokyo = "https://ambiguous-vein-tokyo-station.glitch.me";
const webpage_seoul = "https://ambiguous-vein-seoul.glitch.me";

export default class AFrame extends Component {
  render() {
    const { data } = this.props;

    const imgStyle = {
      height: "30px",
      width: "30px"
    };

    const imgStyleTW = {
      height: "20px",
      width: "20px",
      padding: "5px"
    };

    return (
      <div className="page-size">
        <List component="nav">
          <ListItem button component="a" target="_blank" href={webpage_shibuya}>
            <ListItemIcon>
              {/* <CityIcon /> */}
              <img src={JapanIcon} style={imgStyle} />
            </ListItemIcon>
            <ListItemText primary="Shibuya" />
          </ListItem>
          <ListItem
            button
            component="a"
            target="_blank"
            href={webpage_harajuku}
          >
            <ListItemIcon>
              <img src={JapanIcon} style={imgStyle} />
            </ListItemIcon>
            <ListItemText primary="Harajuku" />
          </ListItem>
          <ListItem button component="a" target="_blank" href={webpage_tokyo}>
            <ListItemIcon>
              <img src={JapanIcon} style={imgStyle} />
            </ListItemIcon>
            <ListItemText primary="Tokyo" />
          </ListItem>
        </List>
        <Divider />
        <List component="nav">
          <ListItem button component="a" target="_blank" href={webpage_taipei}>
            <ListItemIcon>
              <img src={TaiwanIcon} style={imgStyleTW} />
            </ListItemIcon>
            <ListItemText primary="Taipei" />
          </ListItem>
        </List>
        <Divider />
        <List component="nav">
          <ListItem button component="a" target="_blank" href={webpage_seoul}>
            <ListItemIcon>
              <img src={KoreaIcon} style={imgStyle} />
            </ListItemIcon>
            <ListItemText primary="Seoul" />
          </ListItem>
        </List>
      </div>
    );
  }
}
