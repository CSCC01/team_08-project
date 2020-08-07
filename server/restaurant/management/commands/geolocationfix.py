
from restaurant.models import Restaurant
from restaurant.cuisine_dict import load_dict
from django.core.management.base import BaseCommand, CommandError
import json
import random
import traceback
from faker import Faker
from datetime import datetime

class Command(BaseCommand):
    help = '''usage: python manage.py populaterestaurants [numentries]\nseeds the restaurant database with ""numentries"" randomly generated restaurant documents'''

    def __init__(self):
        self.faker = Faker()
        Faker.seed(datetime.now())

    def add_arguments(self,parser):
        pass

    def handle(self, *args, **options):
        all_restaurants = Restaurant.get_all()['Restaurants']


        
        for restaurant in all_restaurants:
            try:
                geo_location = eval(restaurant['GEO_location'])
                price = restaurant['pricepoint']
                print("geo" + str(geo_location))
                if type(geo_location) == dict:
                    continue
                if not type(geo_location) == tuple:
                    print(f"one of the entries is not a tuple: {geo_location}")
                    geo_location = eval(self.faker.location_on_land())
                if not price.lower() in {'low','medium','high'}:
                    print(f"invalid pricepoint {price}")
                    if not price in {'$',"$$","$$$"}:
                        raise Exception
                    else:
                        price = {'$': 'Low', "$$": 'Medium', "$$$": "High"}[price]
            except NameError:
                traceback.print_exc()
                geo_location = self.faker.location_on_land()
            except Exception:
                print("execution halted")
                break

                

            new_location = {
                "lat": str(geo_location[0]),
                "long": str(geo_location[1]),
                "city": str(geo_location[2]),
                "state": str(geo_location[3]),
                "country": str(geo_location[4])
            }
            restaurant['GEO_location'] = new_location
            restaurant['pricepoint'] = price.title()
            new_rest = Restaurant(**restaurant)
            new_rest.clean_fields()
            new_rest.clean()
            new_rest.save()
        
