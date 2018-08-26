#!/usr/bin/env python
# -*- coding: utf-8 -*-

# flask stuff
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# component
from make_tweet_list import get_tweet_list
from generate_aframe import generate_aframe
from api.here_maps_api import make_here_maps_request_url

# pretty interface
from flasgger import Swagger

# CORS for connecting with the front
allowed_domains = [
    r'*',
]

application = Flask(__name__)
Swagger(application)

CORS(application,
     origins=allowed_domains,
     resources=r'/v1/*',
     supports_credentials=True)
# only allows access to listed domains (CORS will only be applied to allowed_domains
# only allows access to v1 (CORS will only be applied to domains that start with /v1/*
# IMPORTANT: supports_credentials is allows COOKIES and CREDENTIALS to be submitted across domains


# more CORS settings here: https://flask-cors.corydolphin.com/en/latest/api.html#extension
# github example: https://github.com/corydolphin/flask-cors/blob/master/examples/app_based_example.py


def pretty_homepage(input_text):
    return render_template('main.html', content=input_text), 200


# only POST
@application.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        print(request)
        a = request.args.get('a')
    if request.method == 'POST':
        print(request)
        a = request.form['a']
    else:
        info_text = """
        welcome to the AODH-2018 team standy backend! you don't seem to have given the correct input!
        """
        return pretty_homepage(info_text)


    return "hello {}".format(a)


@application.route('/v1/aframe/', methods=['GET'])
def aframe_by_query():
    try:
        location_query = request.args.get('location')
    except:
        return 'no location specified'

    # run the aframe creation
    location_map = make_here_maps_request_url(location=location_query)
    location_tweets = {
        "results": get_tweet_list(query=location_query, count=30),
        "status": 1
    }

    return render_template("aframe.html", location=location_map, tweet_content=location_tweets)


@application.route('/v1/tweets/query/', methods=['GET'])
def return_latest_tweets_by_query():
    """
        get list of latest tweets, locations, sentiment, and time
        ---
        parameters:
          - name: location
            in: query
            type: string
            required: true
            default: osaka
        responses:
          200:
            description: returns a json list of tweets
            schema:
              id: predictionGet
              properties:
                results:
                  type: json
                  default: setosa
                status:
                  type: number
                  default: 200
    """
    if request.method == 'GET':
        query_input = request.args.get('location')
    elif request.method == 'POST':
        query_input = 'osaka'

    return jsonify(get_tweet_list(query=query_input, count=100))


@application.route('/v1/tweets/location/', methods=['GET'])
def return_latest_tweets_by_coord():
    """
        get list of latest tweets, locations, sentiment, and time
        ---
        parameters:
          - name: lat
            in: query
            type: number
            required: true
            default: 25.037757
          - name: lng
            in: query
            type: number
            required: true
            default: 121.547187
          - name: disaster
            in: query
            type: string
            required: true
            default: "false"
          - name: radius
            in : query
            type: number
            required: false
            default: 1
        responses:
          200:
            description: returns a json list of tweets
            schema:
              id: predictionGet
              properties:
                results:
                  type: json
                  default: setosa
                status:
                  type: number
                  default: 200
    """
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    disaster_switch = request.args.get('disaster')
    if disaster_switch == "true":
        disaster_switch = True
    else:
        disaster_switch = False
    rad = float(request.args.get('radius'))

    req = {
        "lat": lat,
        "lng": lng,
        "disaster": disaster_switch,
        "radius": rad
    }

    response = {
        "results": get_tweet_list(query=req),
        "status": 1
    }

    return jsonify(response)


# add ssl_context='adhoc' to application.run() to generate a self-signed certificate
application.run(host='0.0.0.0', port=5000, debug=False)
print('a flask app is initiated at {0}'.format(application.instance_path))
