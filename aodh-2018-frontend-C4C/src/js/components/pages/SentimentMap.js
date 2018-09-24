import React, { Component } from "react";
import HereMap from "../units/HereMap";

export default class SentimentMap extends Component {
  render() {
    const { data } = this.props;

    const mapStyle = {
      zIndex: -999
    };

    if (!data || data.length === 0) return null;

    // const tweets_pic = data.tweets.map(tweets => {
    //   if (!tweets.photo_url || tweets.photo_url === "") {
    //     console.log("no images, skipping this tweet");
    //     return null;
    //   } else {
    //     return (
    //       <div className="">
    //         <img src={tweets.photo_url} alt="" />
    //       </div>
    //     );
    //   }
    // });

    // console.log(tweets_pic);

    return (
      <HereMap height={window.innerHeight - 130} style={mapStyle} data={data} />
    );
  }
}
