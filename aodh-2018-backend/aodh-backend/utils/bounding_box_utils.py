import math

class BoundingBox(object):
    def __init__(self, *args, **kwargs):
        self.lat_min = None
        self.lng_min = None
        self.lat_max = None
        self.lng_max = None


def get_bounding_box(latitude_in_degrees, longitude_in_degrees, half_side_in_km):
    #assert half_side_in_miles > 0
    latitude_in_degrees = float(latitude_in_degrees)
    longitude_in_degrees = float(longitude_in_degrees)
    assert latitude_in_degrees >= -90.0 and latitude_in_degrees  <= 90.0
    assert longitude_in_degrees >= -180.0 and longitude_in_degrees <= 180.0

    #half_side_in_km = half_side_in_miles * 1.609344
    lat = math.radians(latitude_in_degrees)
    lon = math.radians(longitude_in_degrees)

    radius  = 6371
    # Radius of the parallel at given latitude
    parallel_radius = radius*math.cos(lat)

    lat_min = lat - half_side_in_km/radius
    lat_max = lat + half_side_in_km/radius
    lng_min = lon - half_side_in_km/parallel_radius
    lng_max = lon + half_side_in_km/parallel_radius
    rad2deg = math.degrees

    box = BoundingBox()
    box.lat_min = rad2deg(lat_min)
    box.lng_min = rad2deg(lng_min)
    box.lat_max = rad2deg(lat_max)
    box.lng_max = rad2deg(lng_max)

    return (box)