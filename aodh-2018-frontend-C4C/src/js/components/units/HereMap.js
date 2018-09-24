import React, { Component } from "react";
import { geolocated } from "react-geolocated";
import { Map, TileLayer, Marker } from "react-leaflet";

// IPC is the map provider for japan

class HereMapsComponent extends Component {
  constructor() {
    super();
    this.state = {
      location: {}
    };
  }

  render() {
    const mapStyle = {
      height: this.props.height,
      width: "100%",
      boxShadow: "0px 1px 5px #B9BABF",
      zIndex: 2
    };

    if (!this.props.isGeolocationAvailable) {
      return <div>Your browser does not support Geolocation</div>;
    } else if (!this.props.isGeolocationEnabled) {
      return <div>Geolocation is not enabled</div>;
    } else {
      console.log("got stuff");
      console.log(this.props);
      if (this.props.coords) {
        let user_pos = [
          this.props.coords.latitude,
          this.props.coords.longitude
        ];

        const { destination, query, tweets } = this.props.data;

        const target_marker = (
          <Marker position={[destination.full_lat, destination.full_lng]} />
        );

        const query_marker = <Marker position={query} />;

        const user_marker = <Marker position={user_pos} />;

        const tweet_markers = tweets.map((t, i) => {
          return <Marker key={i} position={[t.full_lat, t.full_lng]} />;
        });

        return (
          <Map center={user_pos} zoom={16} style={mapStyle}>
            <TileLayer
              url="https://{s}.{base}.maps.cit.api.here.com/maptile/2.1/{type}/{mapID}/hybrid.day/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}"
              attribution="Map &copy; 1987-2014 <a href=&quot;http://developer.here.com&quot;>HERE</a>"
              subdomains="1234"
              mapID="newest"
              app_id="Wm5IPc9gwFJxYnZndsao"
              app_code="RBuslL7WAJiltWLKo8fulA"
              base="aerial"
              maxZoom="20"
              type="maptile"
              language="eng"
              format="png8"
              size="256"
            />
            {target_marker}
            {query_marker}
            {user_marker}
            {tweet_markers}
          </Map>
        );
      } else {
        return <div>Getting the location data&hellip; </div>;
      }
    }
  }
}

export default geolocated({
  positionOptions: {
    enableHighAccuracy: false
  },
  userDecisionTimeout: 5000
})(HereMapsComponent);
