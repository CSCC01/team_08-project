from django.test import SimpleTestCase
from utils.document_seed_generator import Seeder
from utils.document_seed_generator import clean
from faker import Faker
import json

class AddTestCase(SimpleTestCase):

    def setUp(self):
        self.seeder = Seeder()
        self.faker = Faker()
        Faker.seed(0)

    #Note: when checking if a function has been added in two places, use the EXACT same instance of the
    #function, since python compares the function hashes which are unique per instance regardless if the content
    #is exactly the same
    def test_add_randomizer(self):
        '''
        dictionary correctly adds random generation functions
        '''
        gen_dict = {}
        testfunc = lambda x: x.name()
        expected = {"name": testfunc}
        self.seeder.add_randomizer("name", testfunc, gen_dict)
        self.assertEqual(gen_dict["name"], expected["name"])

    def test_gen_rand_dict(self):
        '''
        JSON dump is correctly randomly generated
        '''
        gen_dict = {"name": lambda q: q.name(), "address" : lambda x: x.address}
        expected_document = {"name": self.seeder.faker.name(), "address" : self.seeder.faker.address}
        document = self.seeder.gen_rand_dict(0,gen_dict)
        self.assertEqual(document["name"], expected_document["name"])
        self.assertEqual(document["address"], expected_document["address"])

    def test_clean_dict(self):
        '''
        dicts are properly cleaned of invalid functions
        '''
        gen_dict = {"name" : lambda faker: None}
        expected_dict = {}
        expected_keys = ["name"]
        cleaned_keys = clean(gen_dict)
        self.assertDictEqual(gen_dict, expected_dict)
        self.assertEqual(cleaned_keys, expected_keys)