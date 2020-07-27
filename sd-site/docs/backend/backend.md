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
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50, default='')
    restaurant_id = models.CharField(max_length=24, editable=False)
    description = models.CharField(max_length=200, blank=True, default='')
    picture = models.CharField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    tags = models.ListField(default=[], blank=True)
    specials = models.CharField(max_length=51, blank=True)
```

###### Manual Tag for Food Item

```python
    _id = models.ObjectIdField()
    category = models.CharField(max_length=4, choices=Categories.choices())
    value = models.CharField(max_length=50)
    foods = models.ListField(default=[], blank=True)
```

###### Restaurant

```python
    _id = models.ObjectIdField()
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=40)
    cuisine = models.CharField(max_length=30)
    pricepoint = models.CharField(max_length=5, choices=Prices.choices()) 
    twitter = models.CharField(max_length=200, blank=True)
    instagram = models.CharField(max_length=200, blank=True)
    bio = models.TextField(null=True)
    GEO_location = models.CharField(max_length=200)
    external_delivery_link = models.CharField(max_length=200)
    cover_photo_url = models.CharField(max_length=200,
                                       default='https://www.nautilusplus.com/content/uploads/2016/08/Pexel_junk-food.jpeg')
    logo_url = models.CharField(max_length=200,
                                default='https://d1csarkz8obe9u.cloudfront.net/posterpreviews/diner-restaurant-logo-design-template-0899ae0c7e72cded1c0abc4fe2d76ae4_screen.jpg?ts=1561476509')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    owner_name = models.CharField(max_length = 50, blank = True)
    owner_story = models.CharField(max_length = 3000, blank = True)
    owner_picture_url = models.CharField(max_length = 200, blank=True)
```

###### Prices (Enum)

    Low = "$"
    Medium = "$$"
    High = "$$$"

###### Categories (Enum)

    PR = "Promotion"
    FR = "Food Restriction"
    CU = "Cuisine"
    DI = "Dish"

#### Timeline

###### TimelinePost
```python
    _id = models.ObjectIdField()
    restaurant_id = models.CharField(max_length=24)
    user_id = models.CharField(max_length=24)
    likes = models.ListField(default=[], blank=True)
    content = models.TextField(max_length=4096)
    Timestamp = models.DateTimeField(auto_now=True)
    comments = models.ListField(default=[], blank=True)
```

##### TimelineComment
```python
    _id = models.ObjectIdField()
    post_id = models.CharField(max_length=24)
    user_id = models.CharField(max_length=24)
    likes = models.ListField(default=[], blank=True)
    content = models.TextField(max_length=256)
    Timestamp = models.DateTimeField(auto_now=True)
```


## URLs

|               Address               | Required Fields (Field Type)                                                                                                                                                       | Optional Fields                                                                    | Type | Functionality                                                |
| :---------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :--: | ------------------------------------------------------------ |
|            /user/signup/            | nickname, name, picture, updated_at, email, email_verified                                                                                                                         | role (_Roles_ Name), restaurant_id                                                 | POST | Registers SDUser to DB                                       |
|           /user/role_reassign/      | user\_email, role (_Roles_ Name)                                                                                                                                                   |                                                                                    | POST | Updates Role of SDUser (Not RO)                              |
|           /user/role_reassign/      | user\_email, role (_Roles_ Name), (All Fields Needed for /restaurant/insert/)                                                                                                      |                                                                                    | POST | Updates Role of SDUSer to RO and adds his restaurant page    |
|             /user/data/             | email                                                                                                                                                                              |                                                                                    | GET  | Returns All Fields of the SDUser                             |
|            /user/exists/            | email                                                                                                                                                                              |                                                                                    | GET  | Returns if the SDUser exists in the DB                       |
|            /user/edit/              | email                                                                                                                                                                              | **nickname, name, picture, updated_at**                                            | POST | Updates the fields of the given User with the new data       |
|       /restaurant/tag/insert/       | food\_name, restaurant\_id, category (_Categories_ Name), value                                                                                                                    |                                                                                    | POST | Adds Tag to a Food Item                                      |
|       /restaurant/tag/clear/        | food_name, restaurant_id                                                                                                                                                           |                                                                                    | POST | Clears All Tags on a Food Item                               |
|        /restaurant/tag/auto/        | \_id                                                                                                                                                                               |                                                                                    | POST | Automatically tags food based on description                 |
|      /restaurant/dish/insert/       | name, restaurant_id, description, picture, price, specials                                                                                                                         |                                                                                    | POST | Adds a dish to DB                                            |
|      /restaurant/dish/get_all/      |                                                                                                                                                                                    |                                                                                    | GET  | Retrieves all dishes                                         |
|      /restaurant/dish/edit/         | \_id                                                                                                                                                                               | **name, description, picture, price, specials**                                    | POST | Updates the fields of the given Food with the new data       |
|      /restaurant/dish/delete/       | food_name, restaurant_id                                                                                                                                                           |                                                                                    | POST | Deletes dish from db                                         |
| /restaurant/dish/get_by_restaurant/ | restaurant_id                                                                                                                                                                      |                                                                                    | GET  | Retrieves all dishes from restaurant                         |
|          /restaurant/get/           | \_id                                                                                                                                                                               |                                                                                    | GET  | Retrieves Restaurant data                                    |
|        /restaurant/get_all/         |                                                                                                                                                                                    |                                                                                    | GET  | Retrieves all Restaurants                                    |
|         /restaurant/insert/         | name, address, phone, email (unique), city, cuisine, pricepoint (_Price_ Name), instagram, twitter, GEO_location, external_delivery_link, bio, cover_photo_url, logo_url, rating   | owner_name, owner_story, owner_picture_url                                         | POST | Registers a Restaurant to DB                                 |
|          /restaurant/edit/          | restaurant_id                                                                                                                                                                      | **(All Fields Needed for /restaurant/insert/ except for rating and GEO_location)** | POST | Updates the fields of the given Restaurant with the new data |
|        /timeline/post/upload/       | restaurant_id, user_id, content                                                                                                                                                    |                                                                                    | POST | Add post to timeline table                                   |
|        /timeline/post/delete/       | post_id                                                                                                                                                                            |                                                                                    | POST | deletes a post and all linked comments from the timeline table |
|        /timeline/post/get_all/      |                                                                                                                                                                                    |                                                                                    | GET  | Retrieves all posts                                          |
|      /timeline/comment/upload/      | post_id, user_id, content                                                                                                                                                          |                                                                                    | POST | Add comment to database and to post                          |
|      /timeline/comment/delete/      | \_id                                                                                                                                                                               |                                                                                    | POST | Deletes a comment from the database                          |
|      /timeline/comment/get/         | _id                                                                                                                                                                                |                                                                                    | GET  | Retrieves comment data                                       |

All requests should be sent in a JSON format. Optional parameters can be left blank Ex: {"Role" : ""}. Bolded Fields can be omitted entirely.

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

    #randomly generates a restaurant name in format "{name}'s {dish}s"
    def restaurant_name_randomizer(faker, dish_dict):

    #randomly generates a phone number accounting for faker's default format
    def valid_phone_number(faker)

## Testing

Documented test cases can be found in server/{app}/test**.py where app is the corresponding app to test case.  

Specific apps, test suites, or even individual test cases can be run using the format: "python manage.py test App.Test_File.Test_Suite.Test_Case" depending on how deep you want to go. (Test_File is usually=tests)

#### Testing table legend
| Column                      | Column Description                                                                                                                                                   |
| Test Case Name              | Name of Test Case                                                                                                                                                    |
| App                         | Django app test case is testing                                                                                                                                      |
| Test Suite                  | Test Suite for test case                                                                                                                                             |
| Evaluation Criteria         | Criteria function must pass to pass test case                                                                                                                        |                               
| (Possible Risk) Description | A description of possible risks associated with test case failure                                                                                                    |
| Magnitude                   | Measurement of how dangerous possible risks associated with test case failure                                                                                        |
| Probability                 | Measurement of how likely possible risks may occur associated with test case failure                                                                                 |
| Priority                    | Priority of importance for function to pass test case, priority is influenced by probability, magnitude and the function's priority (found in backlog) it is testing |             

#### Master Testing Table

|  Test Case Name                       |     App    | Test Suite          |  Evaluation Criteria                                                                                                                                                                      | (Possible Risks) Description                                                                             | Magnitude | Probability | Priority |
| :-----------------------------------: | :--------: | :----------------:  | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:  | :------------------------------------------------------------------------------------------------------: | :-------: | :--------:  | :-----:  |                                 
|  test_signup                          | user       | SDUserTestCases     | Checks to see if The User has been inserted into the database                                                                                                                             | No new Users can be made                                                                                 |    High   |     High    |   High   |   
|  test_signup_invalid_role             | user       | SDUserTestCases     | Checks to see the proper Validation Error is thrown                                                                                                                                       | Anything can be used as a role                                                                           |    High   |     Low     |  Medium  |   
|  test_reassign_RO_to_BU               | user       | SDUserTestCases     | Checks if the role change to BU is reflected in the database                                                                                                                              | Users won't be able to be 'demoted'                                                                      |    Low    |     Low     |   Low    |     
|  test_reassign_BU_to_RO_User          | user       | SDUserTestCases     | Checks if the role change to RO and new restaurant id is reflected in the database (user side)                                                                                            | New ROs won't be able to be created                                                                      |    High   |     Low     |  Medium  |     
|  test_reassign_BU_to_RO_Restaurant    | user       | SDUserTestCases     | Checks if the role change to RO and new restaurant id is reflected in the database (restaurant side)                                                                                      | New Restaurants won't be able to be created                                                              |    High   |     Low     |  Medium  |
|  test_data                            | user       | SDUserTestCases     | Checks the user data returned is the matching the queried user                                                                                                                            | Display incorrect data for users                                                                         |    High   |     High    |   High   |     
|  test_exists_true                     | user       | SDUserTestCases     | Checks if an existing user exists                                                                                                                                                         | Users will be unable to upgrade                                                                          |    High   |     High    |   High   |     
|  test_exists_false                    | user       | SDUserTestCases     | Checks if a non-existing user exists                                                                                                                                                      | Unable to sign up users                                                                                  |    High   |     High    |   High   |   
|  test_edit_user                       | user       | SDUserTestCases     | Given new user data, user document is updated to represent new data                                                                                                                       | Users will be unable to customize their profile                                                          |    Low    |     Low     |   Low    |   
|  test_add_randomizer                  | utils      | UtilityTestCases    | Adds a new ["key": randomization_function()] pair into the seeder dictionary                                                                                                              | Incorrectly add new randomization functions to seeders                                                   |    Low    |     Low     |   Low    |     
|  test_gen_rand_dict                   | utils      | UtilityTestCases    | Generates random data based on given seeding dictionary                                                                                                                                   | Inability to randomly generate data for seeding                                                          |    Low    |     Low     |   Low    |     
|  test_clean_dict                      | utils      | UtilityTestCases    | Cleans invalid randomization functions (Non JSON-Encodable outputs) from a given seeding dictionary                                                                                       | Potentially broken seeding scripts with functions that produce non JSON-encodable outputs                |    Low    |     Low     |   Low    |     
|  test_clear_tags                      | restaurant | TagClearCases       | Tag ids are correctly purged from a Food document                                                                                                                                         | Tags remain in database which may result in referencing non-existent tag documents                       |   Medium  |    Medium   |  Medium  |
|  test_clear_foods                     | restaurant | TagClearCases       | Food ids are correctly purged from Tag document                                                                                                                                           | Foods remain tagged which may result in search engine displaying non-existent/incorrect documents        |   Medium  |    Medium   |  Medium  |
|  test_food_ids                        | restaurant | AddTagCases         | Tag ids are correctly updated from tagging an existing Tag document                                                                                                                       | Food will not be associated with subsequent tag which may cause incorrect search engine results          |   Medium  |     Low     |  Medium  |
|  test_tag_ids                         | restaurant | AddTagCases         | Tag ids are correctly updated from tagging an existing Tag document                                                                                                                       | Restaurant owners will be unable to tag their dishes resulting in search engines skipping their dishes   |   Medium  |     High    |  Medium  |
|  test_tag_creation                    | restaurant | AddTagCases         | Tag document is correctly generated upon tagging with a "new" tag word                                                                                                                    | New Tag documents will not be generated, resulting in limited search engine results                      |   Medium  |     Low     |  Medium  |
|  test_foods_already_tagged            | restaurant | AddTagCases         | Food ids are not duplicated upon tagging an already tagged (Food, Tag) couple                                                                                                             | Duplicate food ids take up extra space in the database and slow down querying                            |    Low    |     Low     |   Low    |
|  test_tags_already_tagged             | restaurant | AddTagCases         | Tag ids are not duplicated upon tagging an already tagged (Food, Tag) couple                                                                                                              | Duplicate tag ids take up extra space in the database and slow down querying                             |    Low    |     Low     |   Low    |
|  test_auto                            | restaurant | AutoTagCases        | Correct Tag document correctly automatically generated based on Food's description                                                                                                        | Search engine results become slowly reliant on user input and cannot provide robust results to the user  |   Medium  |     High    |  Medium  |
|  test_get_all_foods                   | restaurant | FoodTestCases       | All food documents within the database are correctly retrieved                                                                                                                            | Frontend will be unable feature dishes on the homepage                                                   |   Medium  |     High    |  Medium  |                               
|  test_get_by_restaurant               | restaurant | FoodTestCases       | All food documents for a restaurant within the database are correctly retrieved                                                                                                           | Frontend will be unable show each restaurant's page/menu                                                 |     High  |     High    |  High    |                               
|  test_delete_food                     | restaurant | FoodTestCases       | The Food object is correctly wiped from the database                                                                                                                                      | Restaurant Pages will have previously deleted dishes                                                     |   Medium  |     Medium  |  Medium  |
|  test_edit_dish                       | restaurant | FoodTestCases       | Given new food data, food document is updated to represent new data                                                                                                                       | Restaurant Owners will be unable to edit the information of their dishes                                 |   Medium  |     Medium  |  Medium  |                               
|  test_find_restaurant                 | restaurant | RestaurantTestCases | Correct restaurant document is retrieved given primary key 'id'                                                                                                                           | Frontend will be unable to documents associated with that specific restaurant such as dishes and users   |    High   |     High    |   High   |
|  test_find_all_restaurant             | restaurant | RestaurantTestCases | All restaurant documents are retrieved from database                                                                                                                                      | Frontend will is unable to display restaurant data                                                       |    High   |     High    |   High   |
|  test_insert_restaurant               | restaurant | RestaurantTestCases | Given restaurant data, restaurant document is inserted into database representing said data                                                                                               | New restaurants cannot be added to the database                                                          |    High   |     High    |   High   |
|  test_edit_restaurant                 | restaurant | RestaurantTestCases | Given new restaurant data, restaurant document is updated to represent new data                                                                                                           | Restaurant data becomes static and cannot be changed by restaurant owner                                 |   Medium  |    Medium   |  Medium  |
|  test_upload                          | timeline   | PostSuite           | Given post data, Post document is generated in the database                                                                                                                               | No Post can be created                                                                                   |   Medium  |     High    |  Medium  |
|  test_delete                          | timeline   | PostSuite           | Given post id, post and its related comments are deleted from the database                                                                                                                        | No Post can be deleted                                                                             |   Medium  |     Medium    |  Medium  |
|  test_get_all_post                    | timeline   | PostSuite           | All post documents within the database are correctly retrieved                                                                                                                            | Story tab will not be populated properly                                                                 |   Medium  |     High    |  High    |
|  test_upload_comment                  | timeline   | CommentSuite        | Given Comment data, Comment document is generated in the database                                                                                                                         | No Comments can be created                                                                               |   Medium  |     High    |  Medium  |
|  test_upload_post                     | timeline   | CommentSuite        | Given Comment data, Comment document id is added to original post's comments                                                                                                              | No Comments can be viewed                                                                                |   Medium  |     High    |  Medium  |
|  test_comment_delete_comment          | timeline   | CommentSuite        | Given the id of the comment, comment is deleted on the comment side                                                                                                                       | No Comments can be deleted                                                                               |   Low     |     Medium  |  Medium  |
|  test_comment_delete_post             | timeline   | CommentSuite        | Given the id of the comment, comment is deleted on the post side                                                                                                                          | Posts will include deleted comments                                                                      |   Low     |     Medium  |  Medium  |
|  test_get_comment                     | timeline   | CommentSuite        | Correct comment document is retrieved given primary key 'id'                                                                                                                              | Comments can not be viewed                                                                               |   Medium  |     Medium  |  Medium  |
|  test_upload                          | cloud_storage | CloudStorageTestCases | File is uploaded to cloud, and correct path pointing to file is returned                                                                                                             | Images media cannot be changed                                                                           |   High    |     High    |   High   |
|  test_delete                          | cloud_storage | CloudStorageTestCases | File is removed from the cloud                                                                                                                                                       | Images remain clogging the storage                                                                       |   Medium  |    Medium   |  Medium  |
|  test_delete_default                  | cloud_storage | CloudStorageTestCases | Files in default-buckets are not deleted                                                                                                                                             | Default images are deleted, affecting many users unwantingly                                             |   High    |     High    |   High   |
## API and Microservices

### Cloud-storage

Available constants 

| Constant          | Description                     |
| :---------------: | :-----------------------------: |
| TEST_BUCKET       | Path to testing bucket          |
| PRODUCTION_BUCKET | Path to deploy/production bucket|
| IMAGE             | content type for images
#### Functions

#### `upload(file, bucket_path)`
Upload file (binary data) into bucket path of our google cloud and return link to uploaded file

#### `delete(file_path)`
Check if pointed file from the file_path is a default object and if not, delete file from its bucket

#### Example

```python
from cloud_storage import cloud_controller

def test(file):
    """
    file is binary data, django forms can do this for you
    or you can use pillows
    """
    # upload file to test bucket
    path = cloud_controller.upload(file, cloud_controller.TEST_BUCKET)
    
    # optional parameter content_type, by setting it image this allows you to
    # view image in the google console instead of downloading
    #  path = cloud_controller.upload(file, cloud_controller.TEST_BUCKET, 
            #  content_type=cloud_controller.IMAGE)
    
    # delete file
    cloud_controller.delete(path)
```