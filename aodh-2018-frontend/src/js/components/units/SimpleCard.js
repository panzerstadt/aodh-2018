import React, { Component } from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import TwitterLogo from "../../../images/twitter-brands.svg";

const TW_PATH = "https://twitter.com/anyuser/status/";

function map_range(value, low1, high1, low2, high2) {
  return low2 + ((high2 - low2) * (value - low1)) / (high1 - low1);
}

const styles = {
  card: {
    minWidth: 275,
    margin: 10
  },
  bullet: {
    display: "inline-block",
    margin: "0 2px",
    transform: "scale(0.8)"
  },
  title: {
    marginBottom: 16,
    fontSize: 14
  },
  pos: {
    marginTop: 12
  },
  par: {
    marginTop: 20
  }
};

function SimpleCard(props) {
  const { classes } = props;
  const bull = <span className={classes.bullet}>•</span>;

  let col = `hsl(${map_range(props.data.sentiment, 0, 1, 0, 120)}, 65%, 70%)`;

  let tweet_url = TW_PATH + props.data.tweet_id;
  let btnStyle = {
    fontSize: 8
  };
  let twtStyle = {
    height: 20,
    width: 20
  };

  return (
    <div>
      <Card className={classes.card}>
        <CardContent>
          <Typography component="p" className={classes.par}>
            {props.data.text}
          </Typography>
          <Typography className={classes.pos} color="textSecondary">
            {props.data.name}
          </Typography>
        </CardContent>
        <CardActions>
          <Button
            href={tweet_url}
            size="small"
            target="_blank"
            style={{ backgroundColor: col }}
          >
            sentiment
          </Button>
          <Button style={btnStyle}>
            <img src={TwitterLogo} style={twtStyle} alt="go to twitter" />
          </Button>
        </CardActions>
      </Card>
    </div>
  );
}

SimpleCard.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(SimpleCard);
