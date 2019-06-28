module.exports = {
  name: "streetview-rest-api",
  version: "0.0.1",
  env: process.env.NODE_ENV || "development",
  port: process.env.PORT || 3000,
  db: {
    uri:
      "mongodb+srv://tliqun-dev:tb8zToeXK7gRffZg@tliqun-dev-db-nxfz3.gcp.mongodb.net/test?retryWrites=true"
    //uri: 'MONGODB CONNECITON STRING'
    // username and password is NOT MongoDB access pw, but new users in cluster
  }
};
