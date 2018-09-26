import React from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import TwitterLogo from "../../../images/twitter-brands.svg";
import MehLogo from "../../../images/meh.svg";

import "../../../style/css/SimpleCard.css";

const TW_PATH = "https://twitter.com/anyuser/status/";

function map_range(value, low1, high1, low2, high2) {
  return low2 + ((high2 - low2) * (value - low1)) / (high1 - low1);
}

const styles = {
  card: {
    width: 390,
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
  },
  btn: {
    fontSize: 8
  },
  logo: {
    height: 20,
    width: 20
  }
};

function SimpleCard(props) {
  const { classes, data } = props;
  // const bull = <span className={classes.bullet}>•</span>;

  let col = `hsl(${map_range(data.sentiment, 0, 1, 0, 120)}, 65%, 70%)`;

  let tweet_url = TW_PATH + data.tweet_id;

  let bgStyle = {};
  if (data.photo_url) {
    bgStyle = {
      backgroundImage: `url("${data.photo_url}")`,
      backgroundSize: "cover",
      backgroundRepeat: "no-repeat"
    };
  } else {
    bgStyle = {
      backgroundColor: "white"
    };
  }

  return (
    <Card style={bgStyle} className={classes.card}>
      <CardContent>
        <Typography component="p" className={classes.par}>
          {data.text}
        </Typography>
        <Typography className={classes.pos} color="textSecondary">
          {data.name}
        </Typography>
      </CardContent>
      <CardActions>
        <Button disabled={true} style={{ backgroundColor: col }}>
          <img
            className="meh-logo"
            src={MehLogo}
            style={styles.logo}
            alt="sentiment"
          />
        </Button>
        <Button href={tweet_url} size="small" target="_blank">
          <img
            className="twt-logo"
            src={TwitterLogo}
            style={styles.logo}
            alt="go to twitter"
          />
        </Button>
      </CardActions>
    </Card>
  );
}

SimpleCard.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(SimpleCard);
