# geolocation library
import googlemaps

api_key = 'AIzaSyDB8xhviNef3URV-bXtjJ47e94iLz_E8ik'
client = googlemaps.Client(api_key)


def geocode(address):
    """
    return longitude and latitude of an address
    raises Value error for no results or multiple results
    """
    results = client.geocode(address)
    if len(results) == 0:
        raise ValueError('No results')
    elif len(results) == 1:
        return results[0]['geometry']['location']
    else:
        raise ValueError('Ambiguous query')



