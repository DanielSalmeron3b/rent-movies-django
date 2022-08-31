from django.urls import re_path
# from django.conf.urls import url
from home.views import *
from movie_admin_portal import *
from customer_portal import *

urlpatterns = [
    re_path(r'^$',home_page),
]