from django.urls import re_path, path
from movie_admin_portal.views import *
# from django.conf.urls import url

urlpatterns = [
    re_path(r'^index/$',index),
    re_path(r'^login/$',login),
    re_path(r'^auth/$',auth_view),
    re_path(r'^logout/$',logout_view),
    re_path(r'^register/$',register),
    re_path(r'^registration/$',registration),
    re_path(r'^add_movie/$',add_movie),
    re_path(r'^manage_movies/$',manage_movies),
    re_path(r'^order_list/$',order_list),
    re_path(r'^complete/$',complete),
    re_path(r'^history/$',history),
    re_path(r'^delete/$',delete),

    # REST API
    path('movies_api/', MovieView.as_view()),
    path('movies_api/<int:id>', MovieView.as_view()),
]