#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api.twitter_api import get_posts_from_trending_hashtags, search_tweets_by_location_name, search_tweets_by_geolocation
from api.google_api import analyze_sentiment, get_geocode

from api.resas_api import get_prefectures_list

from utils.cache_utils import kw_cache_wrapper
from utils.baseutils import remap, bullshitify
from utils.bounding_box_utils import get_bounding_box
from utils.time_utils import normalize_time


import json


def process_posts(posts=None, location=None, format=None, exact_location_only=True):
    if format == 'aodh':
        loc = location['location']
        lat = loc['lat']
        lng = loc['lng']

        bbox = get_bounding_box(latitude_in_degrees=lat, longitude_in_degrees=lng, half_side_in_km=1)

        output = []
        for v in posts:
            # debug
            # print(json.dumps(v, indent=4, ensure_ascii=False))

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

            output_single = {
                "text": v['text'],
                "sentiment": remap(analyze_sentiment(v['text']).score, -1, 1, 0, 1),
                "lat": norm_lat,
                "lng": norm_lng,
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
            output_single['sentiment'] = analyze_sentiment(v['text']).score

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


def get_tweet_list_from_location_name(query=''):
    posts = search_tweets_by_location_name(query=query)
    geocode = get_geocode(query=query)
    t = process_posts(posts=posts, location=geocode)
    return t


def get_tweet_list_from_geolocation(lat=34.6937, lng=135.5022, radius='1', count=100, exact_location_only=True):
    posts = search_tweets_by_geolocation(lat=lat, lng=lng, radius=radius, count=count)
    loc = {
        "location": {
            "lat": lat,
            "lng": lng
        }
    }
    t = process_posts(posts=posts, location=loc, format="aodh", exact_location_only=exact_location_only)
    return t


def get_tweet_list(query='', exact_location_only=True):
    if type(query) == dict:
        lat = query['lat']
        lng = query['lng']
        output = get_tweet_list_from_geolocation(lat=lat, lng=lng, count=100, exact_location_only=exact_location_only)
    else:
        output = get_tweet_list_from_location_name(query=query)

    output = bullshitify(output_dict=output)
    json_output = json.dumps(output)

    output = {
        "tweets": output,
        "direction": 'ROHIT please place the output from the calculations here, use json_output'
    }

    return output


if __name__ == '__main__':
    # prefecture = get_prefectures_list()[0]['prefName']
    # print(prefecture)

    test_loc = {
        "lat": 25.037757,
        "lng": 121.547187
    }

    t = get_tweet_list(query=test_loc)
    [print(json.dumps(x, indent=4, ensure_ascii=False)) for x in t]
    