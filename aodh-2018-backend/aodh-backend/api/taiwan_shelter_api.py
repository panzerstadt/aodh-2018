from requests_xml import XMLSession
from utils.bounding_box_utils import get_bounding_box
import json


def get_shelter_xml():
    session = XMLSession()
    taiwan_shelter_url = "http://portal.emic.gov.tw/pub/DSP/OpenData/EEA/Shelter.xml"
    r = session.get(taiwan_shelter_url)

    shelter_info_xml_list = r.xml.xpath('//shelterInfo')

    # [print(s) for s in shelter_info_xml_list]

    def check_indoors(xml_in):
        if xml_in.attrs['isIndoor'] == '是':
            return 'true'
        else:
            return 'false'

    output = []
    for s in shelter_info_xml_list:
        output.append({
            "name": s.attrs['name'],
            "shelterCode": s.attrs['shelterCode'],
            "address": s.attrs['address'],
            "capacity": s.attrs['peopleno'],
            "lat": s.attrs['lat'],
            "lng": s.attrs['lon'],
            "indoors": check_indoors(s)
        })

    return output


def get_closest_shelter_in_bounds(lat, lng, radius):
    shelters = get_shelter_xml()

    bbox = get_bounding_box(latitude_in_degrees=lat, longitude_in_degrees=lng, half_side_in_km=radius)

    def bounds_check(shelter_dict):
        lat = shelter_dict['lat']
        lng = shelter_dict['lng']

        if bbox.lat_min <= float(lat) <= bbox.lat_max:
            chk_lat = True
        else:
            chk_lat = False

        if bbox.lng_min <= float(lng) <= bbox.lng_max:
            chk_lng = True
        else:
            chk_lng = False

        return all((chk_lat, chk_lng))

    shelters_inside_bounds = list(filter(bounds_check, shelters))

    if len(shelters_inside_bounds) > 1:
        print('multiple shelters found. returning the closest one')

        def bound
    print(shelters_inside_bounds)


if __name__ == '__main__':
    r = get_closest_shelter_in_bounds(lat=25.034365, lng=121.566133, radius=1)

    print(r)