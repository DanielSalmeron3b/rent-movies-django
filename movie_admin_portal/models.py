from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User

# Create your models here.

class Area(models.Model):
    # pincode = models.CharField(validators = [MinLengthValidator(6), MaxLengthValidator(6)],max_length = 6,unique=True)
    city = models.CharField(max_length = 20)

    def __str__(self):
        return self.city


class MovieAdmin(models.Model):
    movie_admin = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
        )
    phone_number = models.CharField(
        validators = [
            MinLengthValidator(10), 
            MaxLengthValidator(13)
            ], 
            max_length = 13
            )
    area = models.OneToOneField(
        Area, 
        on_delete=models.PROTECT
        )
    wallet = models.IntegerField(default = 0)



class Movies(models.Model):
    movie_name = models.CharField(max_length = 20)
    genre = models.CharField(max_length = 10)
    added_by = models.ForeignKey(
        MovieAdmin, 
        on_delete = models.PROTECT
        )
    area = models.ForeignKey(
        Area, 
        on_delete=models.SET_NULL, 
        null = True
        )
    duration = models.CharField(max_length = 10)
    is_available = models.BooleanField(default = True)
    description = models.CharField(max_length = 100)