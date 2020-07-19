---
id: backend
title: Backend
---

This section will go over all the backends components of the Scarborough Dining Project.

## Models & Enums

#### Auth2

###### Scarborough Dining User

```python
     nickname = models.CharField(max_length=30, blank=True, default="")
     name = models.CharField(max_length=50, default='')
     picture = models.CharField(max_length=200, default='')
     last_updated = models.CharField(max_length=200, default='')
     email = models.EmailField(primary_key=True, default='')
     email_verified = models.BooleanField(default=False)
     role = models.CharField(max_length=5, choices=Roles.choices(), default="BU")
     restaurant_id = models.CharField(max_length=24, blank=True, default=None)
```

###### Roles (Enum)

    RO = "Restaurant Owner"
    BU = "Basic User"

#### Restaurant

###### Food Item

```python
class Food(models.Model):
    name = models.CharField(max_length=50)
    restaurant = models.CharField(max_length=50)  # To be changed when restaurant is implemented
    description = models.CharField(max_length=200, blank=True, default='')
    picture = models.CharField(max_length=200, blank=True, default='')
    category = models.CharField(max_length=50, blank=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
```

###### Manual Tag for Food Item

```python
class ManualTag(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=[("promo", "promo"), ("allergy", "allergy")])
    value = models.CharField(max_length=50)
```

###### Restaurant

```python
class Restaurant(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=40)
    cuisine = models.CharField(max_length=30)
    pricepoint = models.CharField(max_length=30)  # add choices, make enum
    twitter = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    bio = models.TextField(null=True)
    GEO_location = models.CharField(max_length=100)
    external_delivery_link = models.CharField(max_length=1000)
```

## URLs

|               Address               | Required Fields (Field Type)                                                                                          | Optional Fields                        | Type | Functionality                                                |
| :---------------------------------: | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------- | :--: | ------------------------------------------------------------ |
|            /user/signup/            | nickname, name, picture, updated_at, email, email_verified                                                            | role **(_Roles_ Name)**, restaurant_id | POST | Registers SDUser to DB                                       |
|           /user/reassign/           | user*email, role \*\*(\_Roles* Name)\*\*                                                                              |                                        | POST | Updates Role of SDUser (Not RO)                              |
|           /user/reassign/           | user*email, role \*\*(\_Roles* Name)\*\*, (All Fields Needed for /RO/insert/)                                         |                                        | POST | Updates Role of SDUSer to RO and adds his restaurant page    |
|             /user/data/             | email                                                                                                                 |                                        | GET  | Returns All Fields of the SDUser                             |
|            /user/exists/            | email                                                                                                                 |                                        | GET  | Returns if the SDUser exists in the DB                       |
|       /restaurant/tag/insert/       | food_name, restaurant, category, value                                                                                |                                        | POST | Adds Tag to a Food Item                                      |
|       /restaurant/tag/clear/        | food_name, restaurant                                                                                                 |                                        | POST | Clears All Tags on a Food Item                               |
|        /restaurant/tag/auto/        | \_id                                                                                                                  |                                        | POST | Automatically tags food based on description                 |
|      /restaurant/dish/create/       | name, restaurant_id, description, picture, price, specials                                                            |                                        | POST | Adds dish to DB                                              |
|      /restaurant/dish/get_all/      |                                                                                                                       |                                        | GET  | retrieves all dishes                                         |
| /restaurant/dish/get_by_restaurant/ | restaurant_id                                                                                                         |                                        | GET  | retrieves all dishes from restaurant                         |
|          /restaurant/get/           | \_id                                                                                                                  |                                        | GET  | Retrieves Restaurant data                                    |
|        /restaurant/get_all/         |                                                                                                                       |                                        | GET  | Retrieves all Restaurants                                    |
|         /restaurant/insert/         | name, address, phone, email, city, cuisine, pricepoint, instagram, twitter, GEO_location, external_delivery_link, bio |
|          /restaurant/edit/          | restaurant_id                                                                                                         | (All Fields Needed for /RO/insert/)    | POST | Updates the fields of the given Restaurant with the new data |

All requests should be sent in a JSON format. All optional parameters can be left blank Ex: {"Role" : ""}

    path('tag/insert/', views.insert_tag_page, name='insert_tag_page'),
    path('tag/clear/', views.clear_tags_page, name='clear_tags_page'),
    path('tag/auto/', views.auto_tag_page, name='auto_tag_page'),
    path('dish/insert/', views.insert_dish_page, name='insert_dish_page'),
    path('dish/get_all/', views.all_dishes_page, name='all_dishes_page'),
    path('dish/get_by_restaurant/', views.get_dish_by_restaurant_page, name='get_dish_by_restaurant_page'),
    path('get/', views.get_restaurant_page, name='get_restaurant_page'),
    path('insert/', views.insert_restaurant_page, name='insert_restaurant_page'),
    path('get_all/', views.get_all_restaurants_page, name='get_all_restaurants_page'),
    path('edit/', views.edit_restaurant_page, name='edit_restaurant_page')

## Utilities

### Seeding framework: document_seed_generator.py

#### Seeder Class: member methods

```python
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
    def gen_rand_dict(self, gen_dict = {}) -> 'Document':
        '''
        randomly generates one dictionary record with the current JSON in this object's gendict
        Parameters:
            seed(Primitive): data used to seed the Random.random instance of the faker
                NOTE: do not change this for any purpose other than testing, set to 0 for tests so that the outputs are identical
            gen_dict({string: function(faker)}): the dictionary of functions for random generation
        Returns:
            JSONDoc(dict): a dictionary of the format key:value generated
        '''
    def clean(self, gen_dict = {}) -> 'Cleaned Keys':
        '''
        removes the invalid random generation functions from the current generation dictionary
        Params:
            gen_dict({string: function(faker)}): the dictionary of functions for random generation
        Return:
            None
        '''
```

#### Utility functions:

```python
    #randomly generates a restaurant name in format "{name}'s {dish}s"
    def restaurant_name_randomizer(faker, dish_dict):

    #randomly generates a phone number accounting for faker's default format
    def valid_phone_number(faker)
```
