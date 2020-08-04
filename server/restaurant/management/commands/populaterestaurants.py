
from restaurant.models import Restaurant
from restaurant.cuisine_dict import load_dict
from django.core.management.base import BaseCommand, CommandError
from utils.document_seed_generator import Seeder
from utils.document_seed_generator import restaurant_name_randomizer
from utils.document_seed_generator import valid_phone_number
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

        seed.add_randomizer("name",         lambda fake:restaurant_name_randomizer(fake, self.dish_dictionary), gen_dict)
        seed.add_randomizer("address",      lambda fake:fake.address(), gen_dict)
        seed.add_randomizer("phone",        lambda fake:valid_phone_number(fake), gen_dict)
        seed.add_randomizer("email",        lambda fake:fake.email(), gen_dict)
        seed.add_randomizer("city",         lambda fake:fake.city(), gen_dict)
        seed.add_randomizer("cuisine",      lambda fake:fake.random_element(self.cuisine_dictionary), gen_dict)
        seed.add_randomizer("pricepoint",   lambda fake:fake.random_element(elements = ('Low','Medium','High')), gen_dict)
        seed.add_randomizer("bio",          lambda fake:fake.paragraph(), gen_dict)
        seed.add_randomizer("GEO_location", lambda fake:fake.location_on_land(), gen_dict)

        self.seed_dict = gen_dict
        self.seeder = seed

    def add_arguments(self,parser):
        #creates a new mandatory argument
        parser.add_argument('numentries' , type=int)

    def handle(self, *args, **options):
        seed = self.seeder
        gen_dict = self.seed_dict
        invalid_randomizers = seed.clean(gen_dict)
        #generate numentries records in the database
        for _ in range(options['numentries']):
            #separate document for non-random fields in seeding process
            Document = {
                'twitter' : " ",
                'instagram' : " ",
                'external_delivery_link' : " ",
                'rating' : "0.00"
            }
            rand_Document = seed.gen_rand_dict(gen_dict)
            Document.update(rand_Document)
            Restaurant.insert(Document)
