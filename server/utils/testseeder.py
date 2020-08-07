from django.test import SimpleTestCase
from utils.document_seed_generator import Seeder
from faker import Faker
import json

class SeederTestCases(SimpleTestCase):

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
        take the same function and manually insert it into the dictionary in the same way
        that the add_randomizer function is supposed to
        '''
        gen_dict = {}
        testfunc = lambda x: x.name()
        expected = {"name": testfunc}
        self.seeder.add_randomizer("name", testfunc, gen_dict)
        self.assertEqual(gen_dict["name"], expected["name"])


    def test_gen_rand_dict(self):
        '''
        JSON dump is correctly randomly generated
        This test works by comparing the random output at the same seed value, so the output will be identical
        '''
        gen_dict = {"name": lambda q: q.name(), "address" : lambda x: x.address}
        expected_document = {"name": self.seeder.faker.name(), "address" : self.seeder.faker.address}
        Faker.seed(0)
        document = self.seeder.gen_rand_dict(gen_dict)
        self.assertEqual(document["name"], expected_document["name"])
        self.assertEqual(document["address"], expected_document["address"])

    def test_clean_dict(self):
        '''
        dicts are properly cleaned of invalid functions
        The lambda function cannot be encoded to json by python's json library so it is cleaned, while the name is valid 
        '''
        testfuncinvalid = lambda faker : lambda faker : None
        testfuncvalid = lambda faker : faker.name()

        gen_dict = {"function" : testfuncinvalid, "name": testfuncvalid}
        expected_dict = {"name": testfuncvalid}
        expected_keys = ["function"]
        cleaned_keys = self.seeder.clean(gen_dict)
        self.assertDictEqual(gen_dict, expected_dict)
        self.assertEqual(cleaned_keys, expected_keys)