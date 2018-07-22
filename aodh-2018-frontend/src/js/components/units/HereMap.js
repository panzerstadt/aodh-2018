import React, { Component } from "react";
import { geolocated } from "react-geolocated";
import { Map, TileLayer } from "react-leaflet";
import { L } from "leaflet";

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
      width: "100%"
    };

    if (!this.props.isGeolocationAvailable) {
      return <div>Your browser does not support Geolocation</div>;
    } else if (!this.props.isGeolocationEnabled) {
      return <div>Geolocation is not enabled</div>;
    } else {
      if (this.props.coords) {
        return (
          <Map
            center={[this.props.coords.latitude, this.props.coords.longitude]}
            zoom={16}
            style={mapStyle}
          >
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
