import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";
import moment from "moment";
import "../../style/css/main.css";

// import Button from "@material-ui/core/Button";

import TweetsPage from "./pages/TweetsPage";
import TweetsGrid from "./pages/TweetsGrid";
import SentimentMap from "./pages/SentimentMap";
import AFrame from "./pages/AFrame";
import About from "./pages/About";
import AboutEn from "./pages/AboutEn";
import QR from "./pages/QR";

// import dummyTaipei from "../../data/dummy/dummy_taipei";
import dummyShibuya from "../../data/dummy/dummy_shibuya";
// import dummyHiroshima from "../../data/dummy/dummy_hiroshima";
// import dummyKochi from "../../data/dummy/dummy_kochi";

let dummyData = dummyShibuya;
let debug = true;

// do logic here
class Main extends Component {
  constructor() {
    super();
    this.state = {
      data: []
    };
  }
  // perform fetchdata here

  componentDidMount() {
    const lat = 25.033;
    const lng = 121.5654;

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        let pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        console.log(
          `position taken from browser: lat=${pos.lat}, lng=${pos.lng}`
        );
      });
    }

    const params = {
      lat: lat,
      lng: lng,
      disaster: "false",
      radius: "1"
    };

    if (debug === false) {
      const url = new URL("http://35.189.128.32/v1/tweets/location");
      Object.keys(params).forEach(key =>
        url.searchParams.append(key, params[key])
      );

      console.log("fetchData:", url);

      fetch(url, {
        credentials: "include"
      })
        .then(response => {
          // !?!?!?! dunno the next step only works if i add
          // this step here
          return response.json();
        })
        .then(response => {
          let results = Object.assign({}, response.results, {
            query: params,
            timestamp: moment()
          });
          console.log(results);

          this.setState({ data: results });
          console.log("this should have set the data into the component");
          console.log(this.state.data);
        });
    } else {
      let dummyResults = Object.assign({}, dummyData.results, {
        query: params,
        timestamp: moment()
      });
      this.setState({ data: dummyResults });
    }
  }

  render() {
    // turn the state into decent things users can see

    // make pages here
    const tweetsPageComponent = () => {
      return <TweetsPage data={this.state.data} />;
    };

    const tweetsGridComponent = () => {
      return <TweetsGrid data={this.state.data} />;
    };

    const sentimentMapCompoent = () => {
      return <SentimentMap data={this.state.data} />;
    };

    const aFrameComponent = () => {
      return <AFrame data={this.state.data} />;
    };

    const aboutComponent = () => {
      return <About data={this.state.data} />;
    };

    const aboutEnComponent = () => {
      return <AboutEn data={this.state.data} />;
    };

    const QRComponent = () => {
      return <QR data={this.state.data} />;
    };

    return (
      <div className="main">
        <Switch>
          <Route exact path="/tweets" component={tweetsPageComponent} />
          <Route exact path="/images" component={tweetsGridComponent} />
          <Route exact path="/map" component={sentimentMapCompoent} />
          <Route exact path="/ar" component={aFrameComponent} />
          <Route exact path="/about" component={aboutComponent} />
          <Route exact path="/aboutEn" component={aboutEnComponent} />
          <Route exact path="/qr" component={QRComponent} />
        </Switch>
      </div>
    );
  }
}

export default Main;
