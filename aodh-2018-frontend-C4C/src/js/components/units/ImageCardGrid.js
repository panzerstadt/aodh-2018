import React from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import GridList from "@material-ui/core/GridList";
import GridListTile from "@material-ui/core/GridListTile";
import SimpleCard from "./SimpleCard";
// import tileData from './tileData';

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
    height: 450
  },
  subheader: {
    width: "100%"
  }
});

function CardGridList(props) {
  const { classes, data } = props;
  const cols = window.innerWidth >= 420 ? 3 : 1;

  return (
    <div className={classes.root}>
      <GridList cellHeight={200} className={classes.gridList} cols={cols}>
        {data.map((tile, i) => (
          <GridListTile key={i} cols={tile.cols || 1}>
            <SimpleCard data={tile} />
            {/* <img src={tile.img} alt={tile.title} /> */}
          </GridListTile>
        ))}
      </GridList>
    </div>
  );
}

CardGridList.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(CardGridList);
