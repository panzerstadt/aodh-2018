#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hidden.hidden import Twitter
import twitter
import yweather
import json
import os.path as path
import datetime

from utils.baseutils import get_filepath, print_list_of_dicts, unhashtagify
from utils.w2vutils import distance_pair_with_entities
from utils.db_utils import make_db, update_db, load_db
from utils.time_utils import str_2_datetime, datetime_2_str
from utils.cache_utils import kw_cache_wrapper

from api.google_api import detect_language_code, translate_text, get_coordinates_from_places

t_secrets = Twitter()
consumer_key = t_secrets.consumer_key
consumer_secret = t_secrets.consumer_secret
access_token_key = t_secrets.access_token_key
access_token_secret = t_secrets.access_token_secret

# sleep on rate limit=True allows the api to continue and wait till
# the rate limit is lifted, instead of failing
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret,
                  sleep_on_rate_limit=False)



# TIME FORMATTING
time_format_full_with_timezone = '%Y-%m-%d %H:%M:%S %Z'
time_format_full_no_timezone = '%Y-%m-%d %H:%M:%S'
time_format_day = '%Y-%m-%d'
time_format_hour = '%Y-%m-%d %H'

db_dir = "aodh-backend/db"
cache_filename = "cache.json"

db_dict_structure = {
    "content": {
        "label": [],
        "score": 0
    },
    "trends": {
        "exclude_hashtags": {
            "content": [],
            "timestamp": "1999-01-01 00:00:00"
        },
        "include_hashtags": {
            "content": [],
            "timestamp": "1999-01-01 00:00:00"
        }
    },
    "hashtags": {
        "content": [],
        "timestamp": "1999-01-01 00:00:00"
    }
}


cache_db_filepath = get_filepath(path.join(db_dir, cache_filename))
make_db(db_dict_structure, cache_db_filepath)


def get_tweet_content(tweet_id):
    if not isinstance(tweet_id, list):
        status = api.GetStatus(status_id=tweet_id).AsDict()
        tweet_content = status['text']
        return tweet_content
    else:
        statuses = api.GetStatuses(status_ids=tweet_id)
        tweet_contents = [status.AsDict()['text'] for status in statuses]
        return tweet_contents


def get_tweet_url(tweet_id):
    if not isinstance(tweet_id, list):
        status = api.GetStatus(status_id=tweet_id).AsDict()
        #print(json.dumps(status, indent=4, ensure_ascii=False))
        try:
            tweet_content = status['urls'][0]['expanded_url']
            return tweet_content
        except:
            return ''
    else:
        statuses = api.GetStatuses(status_ids=tweet_id)
        tweet_contents = [status.AsDict()['urls']['expanded_url'] for status in statuses]
        return tweet_contents


#@kw_cache_wrapper(cache_key='trends')
def get_top_trends_from_twitter_api(country='Japan', exclude_hashtags=True):
    """
    what is it useful for?
    participation. from twitter API docs

    How can I participate in a trend?
    Simply post a Tweet including the exact word or phrase as it appears in the trends list
    (with the hashtag, if you see one). Due to the large number of people Tweeting about these
    specific trends, you may not always be able to find your particular Tweet in search, but
    your followers will always see your Tweets.

    twitter Ads API has a keyword insights endpoint
    ref: https://developer.twitter.com/en/docs/ads/audiences/api-reference/keyword-insights.html#
    :param filter:
    :return:
    """
    # this stupid WOEID requires yweather to get (a library), because YAHOO itself has stopped supporting it
    # WOEID
    woeid_client = yweather.Client()
    woeid = woeid_client.fetch_woeid(location=country)

    if exclude_hashtags :
        trends = api.GetTrendsWoeid(woeid, exclude='hashtags')
    else:
        trends = api.GetTrendsWoeid(woeid, exclude=None)

    output = []
    for trend in trends:
        trend = trend.AsDict()
        output.append({
            "label": trend['name'],
            "time": trend['timestamp'],
            "query": trend['query'],
            "url": trend['url']
        })

    output_json = json.dumps(output, ensure_ascii=False)
    return output_json


#@kw_cache_wrapper(cache_key='hashtags')
def get_top_hashtags_from_twitter_api(country='Japan', debug=False):
    """
    an extension of get_top_trends_from_twitter()
    make an API call for top trends, then visit each URL to get grab hashtags from top 10 twitter posts
    :return:
    """
    trends = get_top_trends_from_twitter(country=country, exclude_hashtags=False)
    trends = json.loads(trends)

    queries = [t['query'] for t in trends]

    if debug:
        #[print(x) for x in trends]
        #[print(x) for x in queries]
        queries = [queries[0]]

    full_hashtags_list = []
    for query in queries:
        #print(query)
        # there is no country filter, but there is language filter at least
        if country == 'Japan':
            responses = api.GetSearch(term=query, locale='ja', return_json=True)
            try: responses = responses['statuses']
            except: print(responses)
        else:
            responses = api.GetSearch(term=query, return_json=True)
            try: responses = responses['statuses']
            except: print(responses)

        trend_hashtags_list = []
        for response in responses:
            if debug: print(json.dumps(response, indent=4, ensure_ascii=False))
            text = response['text']

            hashtags_list = response['entities']['hashtags']

            if len(hashtags_list) > 0:
                hashtags_list = [h['text'] for h in hashtags_list]
                [trend_hashtags_list.append(h) for h in hashtags_list]

        full_hashtags_list.append(trend_hashtags_list)

    flat_hashtags_list = [item for sublist in full_hashtags_list for item in sublist]

    # turn it into a set to clear duplicates, then append #
    flat_hashtags_list = list(set(flat_hashtags_list))
    flat_hashtags_list = ['#'+h for h in flat_hashtags_list]

    output = []
    for hashtag in flat_hashtags_list:
        output.append({
            "label": hashtag
        })

    output_json = json.dumps(output, ensure_ascii=False)
    return output_json


def get_top_hashtags_from_twitter(country='Japan', debug=False, cache_duration_mins=15):
    cache_db = load_db(database_path=cache_db_filepath, debug=False)
    hashtags_cache = cache_db['hashtags']

    # compare db and now
    db_timestamp = str_2_datetime(hashtags_cache['timestamp'], input_format=time_format_full_no_timezone)
    rq_timestamp = datetime.datetime.now()

    time_diff = rq_timestamp - db_timestamp
    print('time diff: ', time_diff)
    if time_diff.seconds < cache_duration_mins * 60:
        # DB
        output_json = json.dumps(hashtags_cache['content'], ensure_ascii=False)
        return output_json
    else:
        output_json = get_top_hashtags_from_twitter_api(country=country, debug=debug)
        # update
        output_dict = json.loads(output_json)
        cache_db['hashtags']['content'] = output_dict
        cache_db['hashtags']['timestamp'] = datetime_2_str(rq_timestamp, output_format=time_format_full_no_timezone)

        update_db(cache_db, database_path=cache_db_filepath, debug=debug)
        return output_json


def get_top_trends_from_twitter(country='Japan', exclude_hashtags=True, debug=False, cache_duration_mins=15):
    cache_db = load_db(database_path=cache_db_filepath, debug=False)
    trends_db = cache_db['trends']
    if exclude_hashtags:
        trends_cache = trends_db['exclude_hashtags']
    else:
        trends_cache = trends_db['include_hashtags']

    # compare db and now
    db_timestamp = str_2_datetime(trends_cache['timestamp'], input_format=time_format_full_no_timezone)
    rq_timestamp = datetime.datetime.now()

    time_diff = rq_timestamp - db_timestamp
    if time_diff.seconds < cache_duration_mins*60:
        output_json = json.dumps(trends_cache['content'], ensure_ascii=False)
        return output_json
    else:
        output_json = get_top_trends_from_twitter_api(country=country, exclude_hashtags=exclude_hashtags)
        # update
        output_dict = json.loads(output_json)
        if exclude_hashtags:
            cache_db['trends']['exclude_hashtags']['content'] = output_dict
            cache_db['trends']['exclude_hashtags']['timestamp'] = datetime_2_str(rq_timestamp, output_format=time_format_full_no_timezone)
        else:
            cache_db['trends']['include_hashtags']['content'] = output_dict
            cache_db['trends']['include_hashtags']['timestamp'] = datetime_2_str(rq_timestamp, output_format=time_format_full_no_timezone)

        update_db(cache_db, database_path=cache_db_filepath, debug=debug)
        return output_json


#@kw_cache_wrapper(cache_key='posts')
def get_posts_from_hashtags_list(hashtags_list_in):
    cache_db = load_db(database_path=cache_db_filepath, debug=False)
    hashtags_db = cache_db['hashtags']

    post_dict = {}
    for hashtag in hashtags_list_in:
        print('searching hashtag: {}'.format(hashtag))
        response = api.GetSearch(term=hashtag + '-filter:retweets', include_entities=True, return_json=True)
        post_dict[hashtag] = response

    return post_dict


# calculate distance pairs
def calculate_pairwise_distance(keyword='大坂', list_of_entities=['日本', '錦糸町最高', '秋葉原の喫茶店', '地震'], method='average', debug=False):
    from utils.tokenizer_utils import tokenize_and_normalize_sentences
    # translate everything into target language (japanese)
    # this is designed to support future languages (word2vec currently only for japanese
    # todo: train english word2vec
    if debug: print('keyword: {}'.format(keyword))

    target_language_code = detect_language_code(keyword)

    output_score = []
    for entity in list_of_entities:
        if debug: print('hashtag: {}'.format(entity))

        # remove hashtags
        entity = unhashtagify(entity)

        # tokenize
        tokens = tokenize_and_normalize_sentences(entity, language=detect_language_code(entity))
        if debug: print('original tokens: {}'.format(tokens))

        # translate into target language to be able to properly perform word2vec
        tokens = [translate_text(e, target=target_language_code) for e in tokens]
        if debug: print('translated tokens: {}'.format(tokens))

        # for each token, calculate w2v
        token_similarities = distance_pair_with_entities((keyword, tokens))
        # filter out 9999 (NaNs)
        token_similarities = [x for x in token_similarities if x != 9999]
        # but leave one
        if len(token_similarities) == 0:
            token_similarities = [9999]

        if debug: print('w2v similarity: {}'.format(token_similarities))

        # then return average / closest
        if method == 'average':
            score = sum(token_similarities) / len(token_similarities)
        elif method == 'closest':
            score = min(token_similarities)
        else:
            score = min(token_similarities)

        if debug:
            print('score ({}): {}'.format(method, score))
            print('-'*100)

        output_score.append(score)
    return output_score


# calculates the similarity of trending topics globally and in japan to the supplied keyword
def calculate_trend_similarity(keyword='大坂', country='Japan'):
    # set country of interest
    country_of_interest = country

    # this stupid WOEID requires yweather to get (a library), because YAHOO itself has stopped supporting it
    # WOEID
    woeid_client = yweather.Client()
    woeid = woeid_client.fetch_woeid(location=country_of_interest)

    # 1. call twitter to return trends
    # get trends global. each trend is a dictionary
    current_trends_global = api.GetTrendsCurrent()
    current_trends_global = [c.AsDict() for c in current_trends_global]

    # get trends by WOEID
    current_trends_country = api.GetTrendsWoeid(woeid=woeid)
    current_trends_country = [c.AsDict() for c in current_trends_country]

    print_list_of_dicts(current_trends_country)
    print_list_of_dicts(current_trends_global)

    # optional: get additional hashtags
    # global_hashtags_from_trends_list = get_hashtags_from_query_list(current_trends_global)
    # country_hashtags_from_trends_list = get_hashtags_from_query_list(current_trends_country)

    # turn them both into lists
    current_trends_global_list = [x['name'] for x in current_trends_global]
    current_trends_country_list = [x['name'] for x in current_trends_country]

    # calculate pairwise distance here
    global_relevance = calculate_pairwise_distance(keyword=keyword, list_of_entities=current_trends_global_list, debug=True)
    country_relevance = calculate_pairwise_distance(keyword=keyword, list_of_entities=current_trends_country_list, debug=True)

    output = {
        "global": global_relevance,
        "country": country_relevance
    }

    return output


def search_tweets_by_geolocation(lat=51.474144, lng=-0.035401, radius='0.5', count=10):
    # https://github.com/ideoforms/python-twitter-examples/blob/master/twitter-search-geo.py
    response = api.GetSearch(geocode="{},{},{}km".format(lat, lng, radius), count=count)

    output = []
    for r in response:
        output.append(r.AsDict())

    return output


def search_tweets_by_location_name(query='Toronto', count=10):
    response = api.GetSearch(term=query, count=count, include_entities=True)

    output = []
    for r in response:
        output.append(r.AsDict())

    return output


def get_posts_from_trending_hashtags(country='Japan'):
    t = json.loads(get_top_hashtags_from_twitter(country=country))
    # print(json.dumps(t, indent=4, ensure_ascii=False))

    hashtags_list = [h['label'] for h in t][:10]

    posts = get_posts_from_hashtags_list(hashtags_list)

    return posts


def process_geolocation_for_posts(posts):
    output_dict = []

    for k, v_list in posts.items():
        print('')
        print('for hashtag {}'.format(k))

        post_dict = []

        for v in v_list['statuses']:
            # check for geo
            out = {}
            out['content'] = v['text']
            out['data'] = get_tweet_url(v['id_str'])
            if v['geo'] is not None:
                out['location'] = v['geo']
            elif v['coordinates'] is not None:
                out['location'] = v['coordinates']
            elif v['place'] is not None:
                out['location'] = v['place']
            elif v['user']['location'] is not None and len(v['user']['location']) > 0:
                get_coords = get_coordinates_from_places(v['user']['location'])
                out['location'] = get_coords
            else:
                out['location'] = 'UNKNOWN'

            post_dict.append(out)

        output_dict.append(post_dict)

    return output_dict


# 3. filter for disaster keywords or for sudden spikes in interest
# todo

# 4. when triggered, get top posts and return images and photos


# 5. get friends from twitter, and check their latest replies (how long since the disaster before they replied?)

# todo; perhaps word filter?


if __name__ == '__main__':
    def check():
        posts = get_posts_from_trending_hashtags()
        for k, v_list in posts.items():
            print('')
            print('for hashtag {}'.format(k))

            geo_check = []
            coords_check = []
            place_check = []
            user_loc_check = []

            for v in v_list['statuses']:

                geo_check.append(v['geo'])
                coords_check.append(v['coordinates'])
                place_check.append(v['place'])
                user_loc_check.append(v['user']['location'])

            print('{} geo: {}'.format(len(geo_check), geo_check))
            print('{} coords: {}'.format(len(coords_check), coords_check))
            print('{} place: {}'.format(len(place_check), place_check))
            print('{} user_loc: {}'.format(len(user_loc_check), user_loc_check))
    #check()