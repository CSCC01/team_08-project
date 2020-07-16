
from RO.models import Restaurant
from restaurant.cuisine_dict import load_dict
from django.core.management.base import BaseCommand, CommandError
from utils.document_seed_generator import Seeder
import json

class Command(BaseCommand):
    help = '''usage: python manage.py populaterestaurants [numentries]\nseeds the restaurant database with ""numentries"" randomly generated restaurant documents'''

    def __init__(self):
        seed = Seeder()
        gen_dict = {}
        seed.add_randomizer("name",         lambda fake:"TEST$: " + fake.name() + "'s " + 
                                                        fake.random_element(self.dish_dictionary) + "s" , gen_dict)
        seed.add_randomizer("address",      lambda fake:fake.address(), gen_dict)
        seed.add_randomizer("phone",        lambda fake:"".join(filter(str.isdigit,fake.phone_number().split('x')[0])), gen_dict)
        seed.add_randomizer("email",        lambda fake:fake.email(), gen_dict)
        seed.add_randomizer("city",         lambda fake:fake.city(), gen_dict)
        seed.add_randomizer("cuisine",      lambda fake:fake.random_element(self.cuisine_dictionary), gen_dict)
        seed.add_randomizer("pricepoint",   lambda fake:fake.random_element(elements = ('$','$$','$$$')), gen_dict)
        seed.add_randomizer("bio",          lambda fake:fake.paragraph(), gen_dict)
        seed.add_randomizer("GEO_location", lambda fake:fake.location_on_land(), gen_dict)

        self.seed_dict = gen_dict
        dish_path = 'dishes.csv'
        self.dish_dictionary = load_dict.read(dish_path)
        cuisine_path = 'cuisine.csv'
        self.cuisine_dictionary = load_dict.read(cuisine_path)
        self.seeder = seed

    def add_arguments(self,parser):
        #creates a new mandatory argument
        parser.add_argument('numentries' , type=int)

    def handle(self, *args, **options):
        seed = self.seeder

        #generate numentries records in the database
        for _ in range(options['numentries']):
            Document = {
                'twitter' : " ",
                'instagram' : " ",
                'external_delivery_link' : " ",
                'cover_photo_url' : 'https://www.nautilusplus.com/content/uploads/2016/08/Pexel_junk-food.jpeg',
                'logo_url' : 'https://d1csarkz8obe9u.cloudfront.net/posterpreviews/diner-restaurant-logo-design-template-0899ae0c7e72cded1c0abc4fe2d76ae4_screen.jpg?ts=1561476509',
                'rating' : "0.00"
            }
            rand_Document = seed.gen_rand_dict(gen_dict = self.seed_dict)
            Document.update(rand_Document)
            Restaurant.insert(Document)
