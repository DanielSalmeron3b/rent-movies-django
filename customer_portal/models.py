from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from movie_admin_portal.models import *

from movie_admin_portal.models import MovieAdmin

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(
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
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT
        )


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    movie_admin = models.ForeignKey(MovieAdmin, on_delete=models.PROTECT)
    rent = models.CharField(max_length=8)
    movie = models.ForeignKey(Movies, on_delete=models.PROTECT)
    days = models.CharField(max_length = 3)
    is_complete = models.BooleanField(default = False)