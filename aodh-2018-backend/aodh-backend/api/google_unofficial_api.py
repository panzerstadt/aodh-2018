import google_streetview.api
import googlemaps
from aodh_backend.hidden.hidden import GoogleAPI


API_KEY_STREET_VIEW = GoogleAPI().api_key_street_view


def get_street_view(query='shibuya'):
    key = API_KEY_STREET_VIEW

    # Define parameters for street view api
    params = [{
        'size': '640x640',  # max 640x640 pixels
        'location': '46.414382,10.013988',
        'heading': '0',
        'fov': '90',
        'key': key
    }]

    # Create a results object
    results = google_streetview.api.results(params)
    print(results.links)

    results.preview()


    # Download images to directory 'downloads'
    results.download_links('downloads')


def street_view_2():
    gmaps = googlemaps.Client(client_id=client_id, client_secret=client_secret)

    directions_result = gmaps.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)

    print(directions_result)



if __name__ == "__main__":
    import os

    print('current work directory')
    print(os.getcwd())






