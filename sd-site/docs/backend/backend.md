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

|     Address                               | Required Fields (Field Type)                                                                                          | Optional Fields                              |Type     | Functionality                                                   |
| :--------------------------------------:  | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------: | :-----: | --------------------------------------------------------------- |
| /user/signup/                             | nickname, name, picture, updated\_at, email, email\_verified                                                          |   role **(_Roles_ Name)**, restaurant_id     | POST    |Registers SDUser to DB                                           |
| /user/reassign/                           | user_email, role **(_Roles_ Name)**                                                                                   |                                              | POST    |Updates Role of SDUser (Not RO)                                  |
| /user/reassign/                           | user_email, role **(_Roles_ Name)**, (All Fields Needed for /RO/insert/)                                              |                                              | POST    |Updates Role of SDUSer to RO and adds his restaurant page        |
| /user/data/                               | email                                                                                                                 |                                              | GET     |Returns All Fields of the SDUser                                 |
| /user/exists/                             | email                                                                                                                 |                                              | GET     |Returns if the SDUser exists in the DB                           |
| /restaurant/tag/insert/                   | food_name, restaurant, category, value                                                                                |                                              | POST    |Adds Tag to a Food Item                                          |
| /restaurant/tag/clear/                    | food_name, restaurant                                                                                                 |                                              | POST    |Clears All Tags on a Food Item                                   |
| /restaurant/tag/auto/                     | _id                                                                                                                   |                                              | POST    |Automatically tags food based on description                     |
| /restaurant/dish/create/                  | name, restaurant_id, description, picture, price, specials                                                            |                                              | POST    |Adds dish to DB                                                  |
| /restaurant/dish/get_all/                 |                                                                                                                       |                                              | GET     |retrieves all dishes                                             |           
| /restaurant/dish/get_by_restaurant/       | restaurant_id                                                                                                         |                                              | GET     |retrieves all dishes from restaurant                             |
| /restaurant/get/                          | restaurant_id                                                                                                         |                                              | GET     |Retrieves Restaurant data                                        |                                 
| /restaurant/get_all/                      |                                                                                                                       |                                              | GET     |Retrieves all Restaurants                                        |    
| /restaurant/insert/                       | name, address, phone, email, city, cuisine, pricepoint, instagram, twitter, GEO_location, external_delivery_link, bio |
| /restaurant/edit/                         | restaurant_id                                                                                                         | (All Fields Needed for /RO/insert/)          | POST    |Updates the fields of the given Restaurant with the new data     |    


All requests should be sent in a JSON format. All optional parameters can be left blank Ex: {"Role" : ""}

## Testing

Documented test cases can be found in server/{app}/test**.py where app is the corresponding app to test case.  

Specific apps, test suites, or even individual test cases can be run using the format: "python manage.py test App.Test_Suite.Test_Case" depending on how deep you want to go

#### Testing table legend
| Column                      | Column Description                                                                                                                                                   |
| :-------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| Test Case Name              | Name of Test Case                                                                                                                                                    |
| App                         | Django app test case is testing                                                                                                                                      |
| Test Suite                  | Test Suite for test case                                                                                                                                             |
| Evaluation Criteria         | Criteria function must pass to pass test case                                                                                                                        |                               
| (Possible Risk) Description | A description of possible risks associated with test case failure (Some cases will have matching descriptions to test different effects of the same function         |
| Magnitude                   | Measurement of how dangerous possible risks associated with test case failure                                                                                        |
| Probability                 | Measurement of how likely possible risks may occur associated with test case failure                                                                                 |
| Priority                    | Priority of importance for function to pass test case, priority is influenced by probability, magnitude and the function's priority (found in backlog) it is testing |             

|  Test Case Name              |     App    | Test Suite          |  Evaluation Criteria                                                                                                                                                                      | (Possible Risks) Description                                                                             | Magnitude | Probability | Priority |
| :--------------------------: | :--------: | :----------------:  | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:  | :------------------------------------------------------------------------------------------------------: | :-------: | :--------:  | :-----:  |                                 
|  test_signup                 | user       | SDUserTestCases     | Checks to see if The User has been inserted into the database                                                                                                                             | No new Users can be made                                                                                 |           |             |          |   
|  test_signup_invalid_role    | user       | SDUserTestCases     | Checks to see the proper Validation Error is thrown                                                                                                                                       | Anything can be used as a role                                                                           |           |             |          |   
|  test_reassign_RO_to_BU      | user       | SDUserTestCases     | Checks if the role change to BU is reflected in the database                                                                                                                              | Users won't be able to be 'demoted'                                                                      |           |             |          |     
|  test_reassign_BU_to_RO      | user       | SDUserTestCases     | Checks if the role change to RO and new restaurant id is reflected in the database                                                                                                        | New ROs won't be able to be created                                                                      |           |             |          |     
|  test_data                   | user       | SDUserTestCases     | Checks the user data returned is the matching the queried user                                                                                                                            | Display incorrect data for users                                                                         |           |             |          |     
|  test_exists_true            | user       | SDUserTestCases     | Checks if an existing user exists                                                                                                                                                         | Users will be unable to upgrade                                                                          |           |             |          |     
|  test_exists_false           | user       | SDUserTestCases     | Checks if a non-existing user exists                                                                                                                                                      | Unable to sign up users                                                                                  |           |             |          |   
|  test_add_randomizer         | utils      | UtilityTestCases    | Adds a new ["key": randomization_function()] pair into the seeder dictionary                                                                                                              | Incorrectly add new randomization functions to seeders                                                   |           |             |          |     
|  test_gen_rand_dict          | utils      | UtilityTestCases    | Generates random data based on given seeding dictionary                                                                                                                                   | Inability to randomly generate data for seeding                                                          |           |             |          |     
|  test_clean_dict             | utils      | UtilityTestCases    | Cleans invalid randomization functions (Non JSON-Encodable outputs) from a given seeding dictionary                                                                                       | Potentially broken seeding scripts with functions that produce non JSON-encodable outputs                |           |             |          |     
|  test_clear_tags             | restaurant | RestaurantTestCases | Tag ids are correctly purged from a Food document                                                                                                                                         | Tags reside in database, may result in search engine displaying non-existent/incorrect documents         |           |             |          |
|  test_clear_foods            | restaurant | RestaurantTestCases | Food ids are correctly purged from Tag document                                                                                                                                           | Tags reside in database, may result in search engine dispalting non-existent/incorrect documents         |           |             |          |
|  test_food_ids               | restaurant | RestaurantTestCases | Food ids are correctly updated from tagging an existing Tag document                                                                                                                      | Restaurant owners will be unable to tag their dishes resulting in search engines skipping their dishes   |           |             |          |
|  test_tag_ids                | restaurant | RestaurantTestCases | Tag ids are correctly updated from tagging an existing Tag document                                                                                                                       | Restaurant owners will be unable to tag their dishes resulting in search engines skipping their dishes   |           |             |          |
|  test_tag_creation           | restaurant | RestaurantTestCases | Tag document is correctly generated upon tagging with a "new" tag word                                                                                                                    | New Tag documents will not be generated, resulting in limited search engine results                      |           |             |          |
|  test_foods_already_tagged   | restaurant | RestaurantTestCases | Food ids are not duplicated upon tagging an already tagged (Food, Tag) couple                                                                                                             | Duplicate food ids take up extra space in the database and slow down querying                            |           |             |          |
|  test_tags_already_tagged    | restaurant | RestaurantTestCases | Tag ids are not duplicated upon tagging an already tagged (Food, Tag) couple                                                                                                              | Duplicate tag ids take up extra space in the database and slow down querying                             |           |             |          |
|  test_auto                   | restaurant | RestaurantTestCases | Correct Tag document correctly automatically generated based on Food's description                                                                                                        | Search engine results become slowly reliant on user input and cannot provide robust results to the user  |           |             |          |
|  test_get_all_foods          | restaurant | RestaurantTestCases | All food documents within the database are correctly retrieved                                                                                                                            | Frontend will be unable feature dishes on the homepage                                                   |           |             |          |                               
|  test_find_restaurant        | restaurant | RestaurantTestCases | Correct restaurant document is retrieved given primary key 'id'                                                                                                                           | Frontend will be unable to documents associated with that specific restaurant such as dishes and users   |           |             |          |
|  test_find_all_restaurant    | restaurant | RestaurantTestCases | All restaurant documents are retrieved from database                                                                                                                                      | Frontend will is unable to display restaurant data                                                       |           |             |          |
|  test_insert_restaurant      | restaurant | RestaurantTestCases | Given restaurant data, restaurant document is inserted into database representing said data                                                                                               | New restaurants cannot be added to the database                                                          |           |             |          |
|  test_edit_restaurant        | restaurant | RestaurantTestCases | Given new restaurant data, restaurant document is updated to represent new data                                                                                                           | Restaurant data becomes static and cannot be changed by restaurant owner                                 |           |             |          |
