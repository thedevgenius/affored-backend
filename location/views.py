from django.shortcuts import render
from django.views.generic import TemplateView
import pygeohash as pgh
import geohash2
from geopy.geocoders import Nominatim

# Create your views here.
def get_geohashes_within_radius(center_lat, center_lon, radius_meters=1000, precision=7):
    """
    Generate geohashes in a square bounding box of radius_meters around the center point.
    """
    geohash_set = set()
    lat_step = 0.0015  # ~150m for precision 7
    lon_step = 0.0015
    lat_range = int(radius_meters / 150)
    lon_range = int(radius_meters / 150)

    for i in range(-lat_range, lat_range + 1):
        for j in range(-lon_range, lon_range + 1):
            new_lat = center_lat + i * lat_step
            new_lon = center_lon + j * lon_step
            geoh = geohash2.encode(new_lat, new_lon, precision=precision)
            geohash_set.add(geoh)

    return list(geohash_set)

def geohash_to_address(geoh, geolocator):
    lat, lon = geohash2.decode(geoh)
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, language='en')
        return location.address if location else "Address not found"
    except:
        return "Error fetching address"

def print_addresses_from_pincode(pincode):
    geolocator = Nominatim(user_agent="geoapi")

    # Step 1: Get lat/lon of PIN code
    location = geolocator.geocode(pincode)
    if not location:
        print("Could not find coordinates for this PIN code.")
        return

    center_lat, center_lon = location.latitude, location.longitude

    # Step 2: Generate geohash codes around the PIN
    geohashes = get_geohashes_within_radius(center_lat, center_lon, radius_meters=1000)

    # Step 3: Reverse geocode each geohash
    for geoh in geohashes:
        address = geohash_to_address(geoh, geolocator)
        print(f"{geoh}: {address}")


class LocationListView(TemplateView):
    template_name = 'location/location_list.html'