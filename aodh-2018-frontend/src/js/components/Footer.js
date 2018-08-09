import React, { Component } from "react";
import { Link } from "react-router-dom";

import PropTypes from "prop-types";
import SpeakerNotesIcon from "@material-ui/icons/SpeakerNotes";
import ChangeHistoryIcon from "@material-ui/icons/ChangeHistory";
import FavoriteIcon from "@material-ui/icons/Favorite";
import LocationOnIcon from "@material-ui/icons/LocationOn";
import { withStyles } from "@material-ui/core/styles";
import BottomNavigation from "@material-ui/core/BottomNavigation";
import BottomNavigationAction from "@material-ui/core/BottomNavigationAction";

const styles = {
  root: {
    position: "fixed",
    bottom: 0,
    width: "100%",
    boxShadow: "0px 3px 15px #C6C6C6",
    zIndex: 999
  }
};

class LabelBottomNavigation extends Component {
  state = {
    value: "recents"
  };

  handleChange = (event, value) => {
    this.setState({ value });
  };

  render() {
    const { classes } = this.props;
    const { value } = this.state;

    return (
      <BottomNavigation
        value={value}
        onChange={this.handleChange}
        className={classes.root}
      >
        <BottomNavigationAction
          label="Tweets"
          value="recents"
          component={Link}
          to="/tweets"
          icon={<SpeakerNotesIcon />}
        />

        <BottomNavigationAction
          label="Images"
          value="favorites"
          component={Link}
          to="/images"
          icon={<FavoriteIcon />}
        />
        <BottomNavigationAction
          label="Map"
          value="nearby"
          component={Link}
          to="/map"
          icon={<LocationOnIcon />}
        />
        <BottomNavigationAction
          label="AR"
          value="folder"
          component={Link}
          to="/ar"
          icon={<ChangeHistoryIcon />}
        />
      </BottomNavigation>
    );
  }
}

LabelBottomNavigation.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(LabelBottomNavigation);
