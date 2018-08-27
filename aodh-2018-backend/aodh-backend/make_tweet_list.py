#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api.twitter_api import get_posts_from_trending_hashtags, search_tweets_by_location_name, search_tweets_by_geolocation
from api.google_api import analyze_sentiment, get_geocode
from api.taiwan_shelter_api import get_closest_shelter_in_bounds

from api.resas_api import get_prefectures_list

from utils.cache_utils import kw_cache_wrapper
from utils.baseutils import remap, bullshitify, get_filepath
from utils.bounding_box_utils import get_bounding_box
from utils.time_utils import normalize_time

import json


def process_posts(posts=None, location=None, format=None, exact_location_only=True, disaster_boolean=False):
    if format == 'aodh':
        loc = location['location']
        lat = loc['lat']
        lng = loc['lng']

        bbox = get_bounding_box(latitude_in_degrees=lat, longitude_in_degrees=lng, half_side_in_km=1)

        output = []
        for v in posts:
            # debug
            print(json.dumps(v, indent=4, ensure_ascii=False))

            try:
                lat = v['coordinates']['coordinates'][1]
                lng = v['coordinates']['coordinates'][0]
                print(lat, lng)
            except:
                if exact_location_only:
                    print('exact_location_only flag is set to True. skipping this post: {}'.format(v['text']))
                    continue
                coords = v['place']['bounding_box']['coordinates'][0]
                print(coords)
                sum_lat = []
                sum_lng = []
                for c in coords:
                    sum_lat.append(c[1])
                    sum_lng.append(c[0])
                lat = sum(sum_lat) / len(sum_lat)
                lng = sum(sum_lng) / len(sum_lng)
                # averaged lat and lng from bounding box

            norm_lat = remap(lat, bbox.lat_min, bbox.lat_max, 0, 1)
            norm_lng = remap(lng, bbox.lng_min, bbox.lng_max, 0, 1)

            # grab photos
            try:
                photo = v['media'][0]['media_url']
            except:
                photo = ''

            # calculate sentiment
            # TODO: SLOW
            output_sentiment = remap(analyze_sentiment(v['text']), -1, 1, 0, 1)

            # force disaster event
            if disaster_boolean:
                output_sentiment = output_sentiment * 0.3

            # get tweet url
            tweet_id = v['id_str']

            output_single = {
                "text": v['text'],
                "sentiment": output_sentiment,
                "lat": norm_lat,
                "lng": norm_lng,
                "full_lat": lat,
                "full_lng": lng,
                "tweet_id": tweet_id,
                "name": v['user']['name'],
                "time": normalize_time(v['created_at']),
                "photo_url": photo
            }
            output.append(output_single)
        return output

    else:
        output = []
        for v in posts:
            output_single = {}
            output_single['tweet'] = v['text']
            output_single['time'] = v['created_at']
            output_single['location'] = location['location']  # todo: grab location from post if not supplied
            try:
                output_single['sentiment'] = analyze_sentiment(v['text']).score
            except AttributeError:
                output_single['sentiment'] = analyze_sentiment(v['text'])

            output.append(output_single)

            # logic for selecting geolocation
        return output



def get_tweet_list_from_trends():
    posts = get_posts_from_trending_hashtags()[:2]

    for k, v_list in posts.items():
        print('')
        print('for hashtag {}'.format(k))

        geo_check = []
        coords_check = []
        place_check = []
        user_loc_check = []
        time_check = []

        location = []
        for v in v_list['statuses']:
            geo_check.append(v['geo'])
            coords_check.append(v['coordinates'])
            place_check.append(v['place'])
            user_loc_check.append(v['user']['location'])
            time_check.append(v['created_at'])

            # logic for selecting geolocation

        print('{} geo: {}'.format(len(geo_check), geo_check))
        print('{} coords: {}'.format(len(coords_check), coords_check))
        print('{} place: {}'.format(len(place_check), place_check))
        print('{} user_loc: {}'.format(len(user_loc_check), user_loc_check))
        print('{} time: {}'.format(len(time_check), time_check))

    # location as coordinates

    # sentiment
    #sentiments = analyze_sentiment()

    # time

    pass


def get_tweet_list_from_location_name(query='', count=100):
    print("calling twitter API to get {} tweets by location name: {}".format(count, query))
    #posts = search_tweets_by_location_name(query=query)
    geocode = get_geocode(query=query)
    lat = geocode['location']['lat']
    lng = geocode['location']['lng']
    posts = search_tweets_by_geolocation(lat=lat, lng=lng, radius='1', count=count)
    print('processing posts!')
    print('posts: ', posts)
    print('geocode: ', geocode)
    t = process_posts(posts=posts, location=geocode, format="aodh")
    return t



def get_tweet_list_from_geolocation(lat=34.6937, lng=135.5022, radius='1', disaster_boolean='false', count=100, exact_location_only=True):
    print('calling twitter API to get {} tweets by location {} {}'.format(count, lat, lng))
    posts = search_tweets_by_geolocation(lat=lat, lng=lng, radius=radius, count=count)
    loc = {
        "location": {
            "lat": lat,
            "lng": lng
        }
    }
    t = process_posts(posts=posts, location=loc, format="aodh", exact_location_only=exact_location_only, disaster_boolean=disaster_boolean)
    return t


def __calculate__weighted__lat__long(lat, lng, radius, openfile):

    def get_highest_sentiment_location(tweets_in):
        lats = [x['lat'] for x in tweets_in]
        lngs = [x['lng'] for x in tweets_in]
        sentiments = [x['sentiment'] for x in tweets_in]

        sentiment_func = lambda y : y[2]

        sorted_locations = sorted(zip(lats, lngs, sentiments), key=sentiment_func, reverse=True)
        top_sentiment = sorted_locations[0]
        print(sorted_locations)
        print(sorted(sentiments))


        output = {
            "lat": top_sentiment[0],
            "lng": top_sentiment[1]
        }

        print('highest sentiment in list: {} : {}'.format(top_sentiment[2], output))

        return output


    sentiment = []
    weightedlat = []
    weightedlng = []
    tweets = json.loads(openfile)
    for i in tweets:
        if(i['sentiment'] >= 0.5):
            sentiment.append(i['sentiment'])
            weightedlat.append((i['lat']) * (i['sentiment']))
            weightedlng.append((i['lng']) * (i['sentiment']))

    if len(sentiment) == 0:
        # return highest sentiment lat and lng
        # todo: will be updated to be more robust
        s = get_highest_sentiment_location(tweets)
        weighted_lat = s['lat']
        weighted_lng = s['lng']

        return {"lat": weighted_lat, "lng": weighted_lng}


    weightedlatnew = sum(weightedlat) / sum(sentiment)
    weightedlngnew = sum(weightedlng) / sum(sentiment)

    bbox = get_bounding_box(latitude_in_degrees=lat, longitude_in_degrees=lng, half_side_in_km=radius)

    full_lat = remap(weightedlatnew, 0, 1, bbox.lat_min, bbox.lat_max)
    full_lng = remap(weightedlngnew, 0, 1, bbox.lng_min, bbox.lng_max)

    output = {
        "lat": weightedlatnew,
        "lng": weightedlngnew,
        "full_lat": full_lat,
        "full_lng": full_lng
    }

    return output


def __isDisaster(openfile):
    sentimentsForDisaster = []
    configForDisaster = json.loads(openfile)

    #Determine if sentiments avaerage is less than 0.5
    for i in configForDisaster:
        sentimentsForDisaster.append(i['sentiment'])

    try:
        chk = sum(sentimentsForDisaster) / len(sentimentsForDisaster)
    except ZeroDivisionError:
        return 'false'

    print('all sentiments: {}'.format(sentimentsForDisaster))
    print('average sentiment of all tweets: {}'.format(chk))

    if chk < 0.3:
        return "true"
    else:
        return "false"


def calculate_destination(lat, lng, radius, json_output):
    disaster_boolean = __isDisaster(json_output)
    if disaster_boolean:
        # return nearest shelter if shelter is within the bounds
        # return shelter if shelter function returns a place
        shelter = get_closest_shelter_in_bounds(lat, lng, radius)
        if shelter:
            return shelter
        else:
            return __calculate__weighted__lat__long(lat, lng, radius, json_output)
    else:
        # return weighted location
        return __calculate__weighted__lat__long(lat, lng, radius, json_output)


def get_tweet_list(query='', exact_location_only=True, count=100):
    if type(query) == dict:
        lat = query['lat']
        lng = query['lng']
        disaster = query['disaster']

        print('lat and lng', lat, lng)
        try:
            radius = query['radius']
            output = get_tweet_list_from_geolocation(lat=lat, lng=lng, radius=radius, count=count,
                                                     disaster_boolean=disaster,
                                                     exact_location_only=exact_location_only)
        except:
            radius = 1
            output = get_tweet_list_from_geolocation(lat=lat, lng=lng, count=count,
                                                     disaster_boolean=disaster,
                                                     exact_location_only=exact_location_only)
    else:
        """
        used for aframe generation
        """
        radius = 1
        disaster = 0
        geocode = get_geocode(query=query)
        lat = geocode['location']['lat']
        lng = geocode['location']['lng']
        output = get_tweet_list_from_geolocation(lat=lat, lng=lng, count=count,
                                                 disaster_boolean=disaster,
                                                 exact_location_only=exact_location_only)

    output = bullshitify(output_dict=output)
    json_output = json.dumps(output, indent=4, ensure_ascii=False)

    output = {
        "tweets": output,
        "destination": calculate_destination(lat, lng, radius, json_output=json_output),
        "disaster": __isDisaster(json_output)
    }

    return output


if __name__ == '__main__':
    # prefecture = get_prefectures_list()[0]['prefName']
    # print(prefecture)

    test_loc = {
        "lat": 25.037757,
        "lng": 121.547187,
        "disaster": True,
        "radius": 1
    }

    t = get_tweet_list(query=test_loc)
    print(json.dumps(t, indent=4, ensure_ascii=False))
