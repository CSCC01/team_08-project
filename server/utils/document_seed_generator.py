from faker import Faker
from faker.providers import internet, address, date_time, geo, person, phone_number
from datetime import datetime
from logging import Logger
import json


'''
Facilitates conveniently generating random JSON documents for DB seeding using the faker library
add several randomly generated key:value pairs to a seeder object and then use it anywhere
'''
class Seeder():
    def __init__(self):
        fake = Faker()
        #add several providers for convenience
        fake.add_provider(internet)
        fake.add_provider(address)
        fake.add_provider(date_time)
        fake.add_provider(geo)
        fake.add_provider(person)
        fake.add_provider(phone_number)
        self.faker = fake
    

    def add_randomizer(self, keyname = None, randomizerfunc = lambda x: None, gen_dict = {}):
        '''
        adds a randomly generated datatype to the JSON document being generated by Seeder  
        in the format "keyname" : lambda x: faker.randomizerfunc(faker) 
        if there is already a generation function in the dictionary, it will be overwritten
        Parameters: 
            keyname(string):                                        the name of the JSON key
            randomizerfunc:(function(faker) -> Object(JSONEncoder))      the function responsible for randomly generating 
                                                                        this key's value which must be JSON encodable
                                                                        NOTE: the randomizerfunc must take a faker as an argument
                                                                        to inject this dependency
            gen_dict({string: function(faker)}): the dictionary of functions for random generation
        Returns:
            None
        '''
        gen_dict[keyname] = randomizerfunc

    def gen_rand_dict(self, seed = datetime.now(), gen_dict = {}) -> 'Document':
        '''
        randomly generates one dictionary record with the current JSON in this object's gendict
        Parameters: 
            seed(Primitive): data used to seed the Random.random instance of the faker
                NOTE: do not change this for any purpose other than testing, set to 0 for tests so that the outputs are identical
            gen_dict({string: function(faker)}): the dictionary of functions for random generation
        Returns: 
            JSONDoc(dict): a dictionary of the format key:value generated
        '''
        Faker.seed(seed) 
        Document = {}
        #The key value tuples are in the form- "property" : randomizationfunc(faker)
        #loop through all of the generation functions and generate 
        for Keyval in gen_dict.items():
            Document[Keyval[0]] = Keyval[1](self.faker)
        return Document

    def clean(self, gen_dict = {}) -> 'Cleaned Keys':
        '''
        removes the invalid random generation functions from the current generation dictionary
        Params: 
            gen_dict({string: function(faker)}): the dictionary of functions for random generation
        Return: 
            None
        '''
        cleaned_keys = []
        for Keyval in gen_dict.items():
            try:
                json.dumps(Keyval[1](self.faker))
            except:
                print(f"[ {Keyval[0]} ]: invalid random generation function, cleaning...")
                cleaned_keys.append(Keyval[0])
        for Key in cleaned_keys:
            gen_dict.pop(Key, None)
        return cleaned_keys