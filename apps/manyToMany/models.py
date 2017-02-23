from __future__ import unicode_literals

from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        errors = []
        regexemail = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) < 1:
            print "empty email"
            errors.append("empty email")
        if len(postData['username'])<1:
            errors.append("empty username")
        if not regexemail.match(postData['email']):
            errors.append("this is not an email")
            # if we filter for the current username and come back with something, then we know it already exists
        if len(self.filter(username=postData['username'])) > 0:
            errors.append("username taken, suckkkkaaaa")
        if len(self.filter(email = postData['email'])) > 0:
            errors.append("this email already exists in our database")
        if len(errors) == 0:
            newuser = self.create(username=postData['username'], email=postData['email'])
            return (True, newuser)
        return (False, errors)# should return a tuple.....

class PetManager(models.Manager):
    def petValidate(self, postData):
        errors = []
        if len(postData['pet']) < 1 or len(postData['habitat']) < 1:
            errors.append("Fields must not be empty")
            return (False, errors)
        else:
            newpet = self.create(habitat=postData['habitat'], name=postData['pet'])
            return (True, newpet)



class Pet(models.Model):
    habitat = models.CharField(max_length = 30)
    name = models.CharField(max_length = 30)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PetManager()

class User(models.Model):
    username = models.CharField(max_length = 30)
    pets = models.ManyToManyField(Pet, related_name="userpet")
    email = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
