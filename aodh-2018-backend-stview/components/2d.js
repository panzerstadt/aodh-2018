/*globals google*/
// when ready, use this
// browserify demo/2d.js -o demo/static/bundle.js | cd demo/static | serve

/*
  Creates an image grid where each click loads
  a new StreetView panorama.
 */

var equirect = require("../");
var panorama = require("google-panorama-by-location");
var awesome = require("awesome-streetview");
var events = require("dom-events");
var shuffle = require("array-shuffle");

var zoom = 3;
var locations = shuffle(awesome.locations);
var idx = 0;

var canvas = document.createElement("canvas");
var text = document.createElement("p");
run();

function run() {
  // var location_local;
  // if (navigator.geolocation) {
  //   navigator.geolocation.getCurrentPosition(function(position) {
  //     location_local = [position.coords.latitude, position.coords.longitude];
  //     console.log(typeof location_local);
  //   });
  // }

  var location = locations[idx++];
  //location = [48.865937, 2.312376];

  panorama(
    location,
    {
      source: google.maps.StreetViewSource.DEFAULT,
      preference: google.maps.StreetViewPreference.NEAREST
    },
    function(err, result) {
      document.body.appendChild(canvas);
      if (err) {
        console.log(err);
        var obj = document.getElementById("error");
        obj.innerText = "no street view nearby found.";
      } else {
        canvas.className = "gallery-item";
        equirect(result.id, {
          tiles: result.tiles,
          canvas: canvas,
          zoom: zoom
        })
          .on("complete", function(image, info) {
            console.log("Ready", info);
            console.log(location);
          })
          .on("progress", function(ev) {
            //console.log(ev.count / ev.total);
          });
      }

      events.once(window, "click", function() {
        run();
      });
    }
  );
}
