from django.db import models
from user.enum import Roles


# Scarborough Dining User
class SDUser(models.Model):
    nickname = models.CharField(max_length=30, blank=True, default="")
    name = models.CharField(max_length=50, default='')
    picture = models.CharField(max_length=200, default='')
    last_updated = models.CharField(max_length=200, default='')
    email = models.EmailField(primary_key=True, default='')
    email_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=5, choices=Roles.choices(), default="BU")
    restaurant_id = models.CharField(max_length=24, blank=True, default=None)

    # Constructs & Saves User to DB returning the newly signed up user object
    @classmethod
    def signup(cls, nickname, name, picture, updated, email, verified, role, restaurant_id):
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

    # Reassigns the Role as the User to the given Role
    def reassign_role(self, role):
        if self.role != role:
            self.role = role
            self.save(update_fields=["role"])
        return None
