"use strict";

//const StreetView = require("../components/streetview2d");
const StreetView = require("../components/streetview2d");

module.exports = function(ctx) {
  // extract context from passed in object
  const client = ctx.client;
  const server = ctx.server;

  // how to make routes
  // server is the client, allow for get/post/put/delete

  // request for street view
  server.get("/streetview/:lat:lng", (req, res, next) => {
    let lat = req.query.lat;
    let lng = req.query.lng;

    // run the streetview code here
    result = StreetView({ lat: lat, lng: lng });

    // then return an image
    res.send(200, result);

    // dunno what next() does
    next();
  });

  // // create
  // // next seems like a callback
  // server.post("/streetview", (req, res, next) => {
  //   // extract data from body and add timestamps
  //   const data = Object.assign({}, req.body, {
  //     created: new Date(),
  //     updated: new Date()
  //   });

  //   // insert one object into the todos collections
  //   collection
  //     .insertOne(data)
  //     .then(doc => res.send(200, doc.ops[0]))
  //     .catch(err => res.send(500, err));

  //   next();
  // });

  // // update
  // server.put("/streetview/:id", (req, res, next) => {
  //   // extract data from body and add timestamps
  //   const data = Object.assign({}, req.body, {
  //     updated: new Date()
  //   });

  //   // build out findOneAndUpdate variables to organize things
  //   let query = { _id: ObjectID(req.params.id) };
  //   let body = { $set: data };
  //   let opts = {
  //     returnNewDocument: true,
  //     upsert: true
  //   };

  //   // find and update document based on passed id (via route)
  //   collection
  //     .findOneAndUpdate(query, body, opts)
  //     .then(doc => res.send(200, doc))
  //     .catch(err => res.send(500, err));

  //   next();
  // });

  // // delete
  // server.del("/streetview/:id", (req, res, next) => {
  //   // remove one document based on passed in id
  //   collection
  //     .findOneAndDelete({ _id: ObjectID(req.params.id) })
  //     .then(doc => res.send(204))
  //     .catch(err => res.send(500, err));

  //   next();
  // });
};
