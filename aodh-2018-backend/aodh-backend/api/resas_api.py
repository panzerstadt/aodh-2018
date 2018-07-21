from hidden.hidden import Resas
from api.google_api import translate_text
from utils.cache_utils import kw_cache_wrapper
import requests
try:
    import ujson as json
except:
    import json

resas = Resas()
API_KEY = resas.api_key


def city_code(city_name):
    if type(city_name) == str:
        # keyword matching to get prefCode
        pass
    elif type(city_name) == int:
        return city_name

    # todo convert en and ja names to city code
    city_code = 11362
    return city_code


def pref_code(prefecture_name):
    if type(prefecture_name) == str:
        # keyword matching to get prefCode
        pass
    elif type(prefecture_name) == int:
        return prefecture_name

    # todo convert en and ja names to pref code
    pref_code = 11
    return pref_code


def resas_api_call(url_endpoint="/api/v1/industries/broad", query_dict=None):
    resas_headers = {"x-api-key": API_KEY}
    url = "https://opendata.resas-portal.go.jp" + url_endpoint
    response = requests.get(url=url, headers=resas_headers, params=query_dict)
    r = response.json()
    return r


@kw_cache_wrapper(cache_key='broad_industries', cache_name='resas-cache.json')
def get_industries(translate=True, debug=False):
    url_endpoint = "/api/v1/industries/broad"
    r = resas_api_call(url_endpoint=url_endpoint)

    if debug:
        view = json.dumps(r, indent=4, ensure_ascii=False)
        print(view)

    output = r['result']

    if translate:
        translated_output = []
        for x in output:
            translated_output.append({
                "sicCode": x['sicCode'],
                "sicName_en": translate_text(x['sicName'], target='en'),
                "sicName": x['sicName']
            })
        return translated_output

    return output


def get_population(prefecture='saitama', city='saitama-shi', year=2012):
    url_endpoint = "/api/v1/population/composition/perYear"


    if type(city) == str:
        # keyword matching to get cityCode
        pass

    # todo: match cities to city code
    queries = {
        "prefCode": pref_code(prefecture),
        "cityCode": city_code(city)
    }

    r = resas_api_call(url_endpoint=url_endpoint, query_dict=queries)
    return r


def get_population_mesh():
    url_endpoint = "api/v1/population/mesh/chart "
    # todo: find out how to use this data

    # https://translate.googleusercontent.com/translate_c?depth=1&hl=en&ie=UTF8&prev=_t&rurl=translate.google.co.jp&sl=auto&sp=nmt4&tl=en&u=https://opendata.resas-portal.go.jp/docs/api/v1/population/mesh/chart.html&xid=17259,15700019,15700124,15700149,15700168,15700173,15700186,15700190,15700201&usg=ALkJrhgWymF7aRKzu_VIC8T1hM5d5ZUyKw


def get_tourist_attractions(prefecture='saitama', city='saitama-shi'):
    url_endpoint = "/api/v1/tourism/attractions"

    queries = {
        "prefCode": pref_code(prefecture),
        "cityCode": city_code(city)
    }

    r = resas_api_call(url_endpoint=url_endpoint, query_dict=queries)
    return r


@kw_cache_wrapper(cache_key='prefectures', cache_name='resas-cache.json')
def get_prefectures_list():
    url_endpoint = "/api/v1/prefectures"
    r = resas_api_call(url_endpoint=url_endpoint)

    output = r['result']

    return output


if __name__ == '__main__':
    r = get_prefectures_list()
    print(r)
    # t = get_tourist_attractions()
    # print(json.dumps(t, indent=4, ensure_ascii=False))
