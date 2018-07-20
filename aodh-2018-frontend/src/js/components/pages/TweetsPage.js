import React, { Component } from "react";

export default class TweetsPage extends Component {
  render() {
    const { data } = this.props;

    if (!data || data.length === 0) return null;

    const tweets_card = data.tweets.map(tweets => {
      return (
        <div className="">
          <h3>{tweets.text}</h3>
          <p>{tweets.sentiment}</p>
        </div>
      );
    });

    return (
      <div>
        <p>this is the tweets page data</p>
        {tweets_card}
      </div>
    );
  }
}
