# first time only
heroku container:login
heroku create

(then get that app)

# update
heroku container:push web --app aodh-2018-backend
heroku container:release web --app aodh-2018-backend
heroku config:set --app protected-eyrie-85272 GOOGLE_APPLICATION_CREDENTIALS="hidden/config.json"

# to note
heroku doesn't support EXPOSE

# heroku needs your GOOGLE_APPLICATION_CREDENTIALS
heroku config:set --app aodh-2018-backend GOOGLE_APPLICATION_CREDENTIALS="hidden/config.json"