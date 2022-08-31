from django.urls import re_path
from customer_portal.views import *
# from django.conf.urls import url


urlpatterns = [
    re_path(r'^index/$',index),
    re_path(r'^login/$',login),
    re_path(r'^auth/$',auth_view),
    re_path(r'^logout/$',logout_view),
    re_path(r'^register/$',register),
    re_path(r'^registration/$',registration),
    re_path(r'^search/$',search),
    re_path(r'^search_results/$',search_results),
    re_path(r'^rent/$',rent_movie),
    re_path(r'^confirmed/',confirm),
    re_path(r'^manage/',manage),
    re_path(r'^update/',update_order),
    re_path(r'^delete/',delete_order),
]
