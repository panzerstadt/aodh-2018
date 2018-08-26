from urllib import request


def get_zoom_level(location="shibuya"):
    print("checking location for", location)
    # because there are too many cities to vet through the list of navigable countries, we whitelist high zoom areas
    # https://developer.here.com/documentation/map-tile/topics/intermediate-countries.html
    zoom_dict = {
        "taipei": 14,
        "havana": 15,
        "jakarta": 13,
    }

    try:
        out = zoom_dict[location]
    except:
        out = 12

    return out


def make_here_maps_request_url(location="shibuya"):

    z = get_zoom_level(location)

    url = "https://image.maps.cit.api.here.com/mia/1.6/mapview?"
    url += "app_id=2qmJNSdVqQMA1A5r3znU&app_code=gZ4gfY_9k3Pgx2iV9CJifg&t=14&ppi=75&q=100"
    url += "&ci={}&vt=0&w=2048&h=2048&z={}".format(location, z)

    return url



if __name__ == '__main__':

    r = request.urlopen(make_here_maps_request_url("tokyo"))
    print(r)