import React, { Component } from "react";
import HereMap from "../units/HereMap";
import SimpleCard from "../units/SimpleCard";

function map_range(value, low1, high1, low2, high2) {
  return low2 + ((high2 - low2) * (value - low1)) / (high1 - low1);
}

export default class TweetsPage extends Component {
  render() {
    const { data } = this.props;

    if (!data || data.length === 0) return null;

    const tweets_card = data.tweets.map((tweets, i) => {
      let col = `hsl(${map_range(tweets.sentiment, 0, 1, 0, 120)}, 65%, 95%)`;

      return (
        <div key={i} className="">
          <SimpleCard data={tweets} />
        </div>
      );
    });

    return (
      <div>
        <HereMap height="300px" />
        {/* <h3>Tweets and their Sentiments</h3> */}
        {tweets_card}
      </div>
    );
  }
}
