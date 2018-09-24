import React, { Component } from "react";
import HereMap from "../units/HereMap";
import MasonryGrid from "../units/MasonryGrid";

export default class TweetsPage extends Component {
  render() {
    const { data } = this.props;

    if (!data || data.length === 0) {
      return null;
    } else {
      return (
        <div>
          <HereMap height="300px" data={data} />
          {/* <h3>Tweets and their Sentiments</h3> */}
          <MasonryGrid data={data.tweets} />
        </div>
      );
    }
  }
}
