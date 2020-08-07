# geolocation library
import googlemaps
import json

with open('geo/api_secret.json') as f:
    api_key = json.load(f)['key']

client = googlemaps.Client(api_key)


def geocode(address):
    """
    :params-address: address to be geocoded
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
