import requests
from django.db import models
from user.enum import Roles


class SDUser(models.Model):
    """ Scarborough Dining User """
    nickname = models.CharField(max_length=30, blank=True, default="")
    name = models.CharField(max_length=50, default='')
    picture = models.CharField(max_length=200, default='')
    last_updated = models.CharField(max_length=200, default='')
    email = models.EmailField(primary_key=True, default='')
    email_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=5, choices=Roles.choices(), default="BU")
    restaurant_id = models.CharField(max_length=24, blank=True, default=None)
    birthday = models.DateField(blank=True, default=None)
    address = models.CharField(max_length=24, blank=True, default='')
    phone = models.BigIntegerField(blank=True, default=None)
    GEO_location = models.CharField(max_length=200, blank=True, default='')

    @classmethod
    def signup(cls, nickname, name, picture, updated, email, verified, role, restaurant_id):
        """
        Constructs & Saves User to DB returning the newly signed up user object
        :param nickname: nickname of user
        :param name: name of user
        :param picture: URL to picture for user
        :param updated: last updated at this time
        :param email: email of user
        :param verified: status of verification of account
        :param role: role of user
        :param restaurant_id: restaurant id associated with user
        :return: new SDUser Object
        """
        if role == "":
            role = "BU"
        if restaurant_id == "":
            restaurant_id = None

        user = cls(nickname=nickname, name=name, picture=picture, last_updated=updated, email=email,
                   email_verified=verified, role=role, restaurant_id=restaurant_id)
        user.clean_fields()
        user.clean()
        user.save()
        return user

    def reassign_role(self, role):
        """
        Reassigns the Role as the User to the given Role
        :param role: the new role to be given to the user
        :return: None
        """
        if self.role != role:
            self.role = role
            self.save(update_fields=["role"])
        return None

    @classmethod
    def field_validate(self, fields):
        """
        Validates fields
        :param fields: Dictionary of fields to validate
        :return: A list of fields that were invalid. Returns None if all fields are valid
        """
        user_urls = ['picture']

        invalid = {'Invalid': []}

        for field in user_urls:
            if field in fields and fields[field] != '':
                try:
                    requests.get(fields[field])
                except (requests.ConnectionError, requests.exceptions.MissingSchema) as exception:
                    invalid['Invalid'].append(field)

        if 'phone' in fields and fields['phone'] is not None:
            if len(str(fields['phone'])) != 10:
                invalid['Invalid'].append('phone')

        if not invalid['Invalid']:
            return None
        else:
            return invalid
