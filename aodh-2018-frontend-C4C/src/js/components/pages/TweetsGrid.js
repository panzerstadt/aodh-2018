import React, { Component } from "react";
import ImageGrid from "../units/ImageGrid";

export default class TweetsPage extends Component {
  render() {
    const { data } = this.props;

    if (!data || data.length === 0) return null;

    return <ImageGrid data={data} />;
  }
}
