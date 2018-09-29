import React, { Component } from "react";
import { createFilter } from "react-search-input";

import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import Divider from "@material-ui/core/Divider";
import TextField from "@material-ui/core/TextField";
import Typography from "@material-ui/core/Typography";

import JapanIcon from "../../../images/jp.png";
import KoreaIcon from "../../../images/kr.png";
import TaiwanIcon from "../../../images/tw.png";

// import aframe_html from "../../../data/aframe-html/aframe.html";
const webpage_Kansai = "https://clean-the-code.glitch.me";
const webpage_shibuya = "https://ambiguous-vein-rshubuya.glitch.me";
const webpage_harajuku = "https://ambiguous-vein-harajuku.glitch.me";
const webpage_taipei = "https://ambiguous-vein-taiwan.glitch.me";
const webpage_tokyo = "https://ambiguous-vein-tokyo-station.glitch.me";
const webpage_seoul = "https://ambiguous-vein-seoul.glitch.me";

const aframe_urls = [
  {
    label: "Kansai International Airport",
    url: "https://clean-the-code.glitch.me",
    icon: JapanIcon
  },
  {
    label: "Shibuya",
    url: "https://ambiguous-vein-rshubuya.glitch.me",
    icon: JapanIcon
  },
  {
    label: "Taipei",
    url: "https://ambiguous-vein-taiwan.glitch.me",
    icon: TaiwanIcon
  },
  {
    label: "Tokyo",
    url: "https://ambiguous-vein-tokyo-station.glitch.me",
    icon: JapanIcon
  },
  {
    label: "Seoul",
    url: "https://ambiguous-vein-seoul.glitch.me",
    icon: KoreaIcon
  },
  {
    label: "Harajuku",
    url: "https://ambiguous-vein-harajuku.glitch.me",
    icon: JapanIcon
  }
];

const KEYS_TO_FILTER = ["label"];

export default class AFrame extends Component {
  state = {
    keyword: ""
  };

  handleUpdate(e) {
    e.preventDefault();
    this.setState({ keyword: e.target.value });
  }

  render() {
    // const { data } = this.props;

    const imgStyle = {
      height: "30px",
      width: "30px"
    };

    const linkStyle = {
      padding: 20,
      textDecoration: "none"
    };

    const filtered = aframe_urls.filter(
      createFilter(this.state.keyword, KEYS_TO_FILTER)
    );

    const url_list = filtered.map((v, i) => {
      const { label, url, icon } = v;

      return (
        <ListItem button component="a" target="_blank" href={url}>
          <ListItemIcon>
            <img src={icon} style={imgStyle} alt={label} />
          </ListItemIcon>
          <ListItemText primary={label} />
        </ListItem>
      );
    });

    return (
      <div className="page-size">
        <Typography
          component="a"
          href="/about"
          style={linkStyle}
          color="textSecondary"
        >
          <u>About this project</u>
        </Typography>
		<Typography
          component="a"
          href="/IOS"
          style={linkStyle}
          color="textSecondary"
        >
          <u>Realtime Mode - iOS App</u>
        </Typography>
        <Typography
          component="a"
          href="/QR"
          style={linkStyle}
          color="textSecondary"
        >
          <u>QR-code for sharing to your friends</u>
        </Typography>

        <TextField
          id="search"
          label="Click or search the city"
          type="search"
          helperText="e.g. Shibuya, Harajuku, Seoul..."
          margin="normal"
          fullWidth
          onChange={this.handleUpdate.bind(this)}
        />
        <List component="nav">
          {url_list}
          {/* <ListItem button component="a" target="_blank" href={webpage_shibuya}>
            <ListItemIcon>
              <img src={JapanIcon} style={imgStyle} alt="jp" />
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
              <img src={JapanIcon} style={imgStyle} alt="jp" />
            </ListItemIcon>
            <ListItemText primary="Harajuku" />
          </ListItem>
          <ListItem button component="a" target="_blank" href={webpage_tokyo}>
            <ListItemIcon>
              <img src={JapanIcon} style={imgStyle} alt="jp" />
            </ListItemIcon>
            <ListItemText primary="Tokyo" />
          </ListItem>
        </List>
        <Divider />
        <List component="nav">
          <ListItem button component="a" target="_blank" href={webpage_taipei}>
            <ListItemIcon>
              <img src={TaiwanIcon} style={imgStyleTW} alt="tw" />
            </ListItemIcon>
            <ListItemText primary="Taipei" />
          </ListItem>
        </List>
        <Divider />
        <List component="nav">
          <ListItem button component="a" target="_blank" href={webpage_seoul}>
            <ListItemIcon>
              <img src={KoreaIcon} style={imgStyle} alt="kr" />
            </ListItemIcon>
            <ListItemText primary="Seoul" />
          </ListItem> */}
        </List>
      </div>
    );
  }
}
