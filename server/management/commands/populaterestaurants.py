from django_seed import Seed
from RO.models import Restaurant
from restaurant.cuisine_dict import load_dict

seeder = Seed.seeder()

seeder.add_entity(Restaurant, 50, {
    'name' : lambda x: seeder.faker.name(),
    'address' : lambda x: seeder.faker.address(),
    'phone' : lambda x: seeder.faker.phone_number(),
    'email' : lambda x: seeder.faker.email(),
    'city' : lambda x: seeder.faker.city(),
    'cuisine' : lambda x: ,
    'pricepoint' : lambda x: seeder.faker.()
})

inserted_pks = seeder.execute()