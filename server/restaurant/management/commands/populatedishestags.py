from restaurant.models import Food, ManualTag
from RO.models import Restaurant
from restaurant.cuisine_dict import load_dict
from django.core.management.base import BaseCommand, CommandError
from utils.document_seed_generator import Seeder
import json

class Command(BaseCommand):
    help = '''usage: python manage.py populaterestaurants [numentries]\nseeds the restaurant database with ""numentries"" randomly generated restaurant documents'''

    def __init__(self):
        #initialize the seeder dictionary with all necessary randomization functions
        seed = Seeder()
        gen_dict = {}

        #load the dishes and cuisines dictionaries as they are used for selecting random food and cuisine words during seeding
        dish_path = 'dishes.csv'
        self.dish_dictionary = load_dict.read(dish_path)
        cuisine_path = 'cuisine.csv'
        self.cuisine_dictionary = load_dict.read(cuisine_path)
        #retrieve list of all existing restaurants so that the inserted foods are randomly
        #associated with a restaurant
        self.restaurant_ids = []
        Restaurants = Restaurant.get_all()
        for restaurant in Restaurants['Restaurants']:
            self.restaurant_ids.append(restaurant['_id'])

        seed.add_randomizer("name",             lambda fake: fake.random_element(self.dish_dictionary), gen_dict)
        seed.add_randomizer("restaurant_id",    lambda fake: fake.random_element(self.restaurant_ids), gen_dict)
        seed.add_randomizer("description",      lambda fake: fake.random_element(self.dish_dictionary), gen_dict)
        #randomly generates a price from 1.00 - 99.99
        seed.add_randomizer("price",            lambda fake: fake.numerify(text = "!%.##"), gen_dict)
        #randomly generates a percentage string from 0% off - 99% off
        seed.add_randomizer("specials",         lambda fake: fake.numerify(text = "!#") + "% off", gen_dict)

        self.seed_dict = gen_dict
        self.seeder = seed

    def add_arguments(self,parser):
        #creates a new mandatory argument
        parser.add_argument('numentries' , type=int)

    def handle(self, *args, **options):
        seed = self.seeder
        gen_dict = self.seed_dict
        invalid_randomizers = seed.clean(gen_dict)
        #need to store the inserted restaurant/name pairs for auto-tagging
        #stored in the format (name, restaurant_id)
        dishes = []
        #generate numentries records in the database
        for _ in range(options['numentries']):
            #separate document for non-random fields in seeding process
            Document = {
                'picture' : " "
            }
            rand_Document = seed.gen_rand_dict(gen_dict)
            Document.update(rand_Document)
            Food.add_dish(Document)
            ManualTag.auto_tag_food(Food.objects.get(restaurant_id = Document['restaurant_id'], name = Document['name'])._id)

