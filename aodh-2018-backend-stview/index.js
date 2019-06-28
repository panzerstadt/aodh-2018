"use strict";

const config = require("./config");
const restify = require("restify");

// init server
const server = restify.createServer({
  name: config.name,
  version: config.version
});

// add plugins
server.use(restify.plugins.jsonBodyParser({ mapParams: true }));
server.use(restify.plugins.acceptParser(server.acceptable));
server.use(restify.plugins.queryParser({ mapParams: true }));
server.use(restify.plugins.fullResponse());

// turn on server, route file
server.listen(config.port, () => {
  // can pass anything into the route file
  // this time there is a dummy variable 'client'

  let client = "hey";
  console.log(
    "%s v%s ready to accept connections on port %s in %s environment.",
    server.name,
    config.version,
    config.port,
    config.env
  );

  require("./routes/streetview-api")({ client, server });
});
