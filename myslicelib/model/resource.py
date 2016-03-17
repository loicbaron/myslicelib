from myslicelib.model import Entities, Entity

class Resources(Entities):
    pass

class Resource(Entity):
    _class = "Resource"
    _type = "resource" # link, channel ???
    _collection = "Resources"

#
#
# from repoze.lru import lru_cache
# @lru_cache(100)
# def get_location(city):
#     location = None
#     try:
#         #from geopy.geocoders import Nominatim
#         #geolocator = Nominatim()
#         #from geopy.geocoders import GeoNames
#         #geolocator = GeoNames()
#         from geopy.geocoders import GoogleV3
#         geolocator = GoogleV3()
#
#         location = geolocator.geocode(city)
#     except Exception as e:
#         print(e)
#     return location
#
# @lru_cache(100)
# def get_country(location):
#     try:
#         from geopy.geocoders import GoogleV3
#         geolocator = GoogleV3()
#
#         address = geolocator.reverse(location)
#         return address[0].address.split(', ')[-1]
#     except Exception as e:
#         print(e)
#     return location
#

