import React from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import GridList from "@material-ui/core/GridList";
import GridListTile from "@material-ui/core/GridListTile";

const styles = theme => ({
  root: {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "space-around",
    overflow: "hidden",
    backgroundColor: theme.palette.background.paper
  },
  gridList: {
    width: "100%",
    height: "100%"
  },
  subheader: {
    width: "100%"
  }
});

function ImageGridList(props) {
  const { classes, data } = props;

  const responsiveColumns = window.innerWidth >= 420 ? 3 : 1;
  const responsiveHeight = window.innerWidth >= 420 ? 300 : 500;

  const images = data.tweets.map((tweet, i) => {
    if (tweet.photo_url) {
      return (
        <GridListTile key={i} cols={tweet.cols || 1}>
          <img src={tweet.photo_url} alt={tweet.photo_url} />
        </GridListTile>
      );
    } else {
      return null;
    }
  });

  return (
    <div className={classes.root}>
      <GridList
        cellHeight={responsiveHeight}
        className={classes.gridList}
        cols={responsiveColumns}
      >
        {images}
      </GridList>
    </div>
  );
}

ImageGridList.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(ImageGridList);
