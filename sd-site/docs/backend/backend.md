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

|     Address                  | Required Fields (Field Type)                                                                                          | Optional Fields                              |Type     | Functionality                                                   |
| :--------------------------: | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------  | :-----: | --------------------------------------------------------------- |
| /auth/signup/                | nickname, name, picture, updated\_at, email, email\_verified                                                          |   role **(_Roles_ Name)**, restaurant_id     | POST    |Registers SDUser to DB                                           |
| /auth/reassign/              | user_email, role **(_Roles_ Name)**                                                                                        |                                              | POST    |Updates Role of SDUser (Not RO)                                  |
| /auth/reassign/              | user_email, role **(_Roles_ Name)**, (Along With All Fields Needed for /RO/insert/)                                        |                                              | POST    |Updates Role of SDUSer to RO and adds his restaurant page        |
| /auth/data/                  | email                                                                                                                 |                                              | GET     |Returns All Fields of the SDUser                                 |
| /auth/exists/                | email                                                                                                                 |                                              | GET     |Returns if the SDUser exists in the DB                           |
| /tag/add/                    | food_name, restaurant, category, value                                                                                |                                              | POST    |Adds Tag to a Food Item                                          |
| /tag/clear/                  | food_name, restaurant                                                                                                 |                                              | POST    |Clears All Tags on a Food Item                                   |
| /tag/auto_tag/               | _id                                                                                                                   |                                              | POST    |Automatically tags food based on description                     |
| /tag/create/                 | name, restaurant_id, description, picture, price, specials                                                            |                                              | POST    |Adds dish to DB                                                  |
| /tag/get_all/                |                                                                                                                       |                                              | GET     |retrieves all dishes                                             |           
| /tag/get_food_by_restaurant/ | restaurant_id                                                                                                         |                                              | GET     |retrieves all dishes from restaurant                             |
| /RO/get/                     | restaurant_id                                                                                                         |                                              | GET     |Retrieves Restaurant data                                        |                                 
| /RO/getAll/                  |                                                                                                                       |                                              | GET     |Retrieves all Restaurants                                        |    
| /RO/insert/                  | name, address, phone, email, city, cuisine, pricepoint, instagram, twitter, GEO_location, external_delivery_link, bio |


All requests should be sent in a JSON format. All optional parameters can be left blank Ex: {"Role" : """}

