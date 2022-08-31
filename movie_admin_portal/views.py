from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View # For the REST API
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from movie_admin_portal.models import *
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import json

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'movie_admin/login.html')
    else:
        return render(request, 'movie_admin/home_page.html')


def login(request):
    return render(request, 'movie_admin/login.html')


def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'movie_admin/home_page.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            username=username,
            password=password
        )
    
    try:
        movie_admin = MovieAdmin.objects.get(movie_admin= user)
    except:
        movie_admin = None

    if movie_admin is not None:
        auth.login(request, user)
        return render(request, 'movie_admin/home_page.html')
    else:
        return render(request, 'movie_admin/login_failed.html')


def logout_view(request):
    auth.logout(request)
    return render(request, 'movie_admin/login.html')


def register(request):
    return render(request, 'movie_admin/register.html')


def registration(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    phone_number = request.POST.get('phone_number')
    name = request.POST.get('name')
    email = request.POST.get('email')
    city = request.POST.get('city')
    city = city.lower()
    # pincode = request.POST['pincode']

    try:
        user = User.objects.create_user(
            username = username,
            password = password,
            email=email,
        )
        user.name = name
        user.save()
    except:
        return render(request, 'movie_admin/registration_error.html')

    try:
        area = Area.objects.get(
            city = city,
            # pincode = pincode
        )
    except:
        area = None

    if area is not None:
        movie_admin = MovieAdmin(
            movie_admin = user, 
            phone_number = phone_number,
            area=area
        )
    else:
        area = Area(
            city = city,
            # pincode = pincode
        )
        area.save()
        area = Area.objects.get(
            city = city,
            # pincode = pincode
        )
        movie_admin = MovieAdmin(
            movie_admin = user,
            phone_number = phone_number,
            area=area
        )
    movie_admin.save()

    return render(request, 'movie_admin/registered.html')


@login_required
def add_movie(request):
    movie_name = request.POST.get('movie_name')
    genre = request.POST.get('genre')
    added_by = MovieAdmin.objects.get(movie_admin = request.user)
    city = request.POST.get('city')
    city = city.lower()
    # pincode = request.POST['pincode']
    description = request.POST.get('description')
    duration = request.POST.get('duration')

    try:
        area = Area.objects.get(city = city)
    except:
        area = None

    if area is not None:
        movie = Movies(
            movie_name=movie_name,
            genre=genre,
            added_by=added_by,
            area=area,
            description=description,
            duration=duration,
            )
    else:
        area = Area(city=city)
        area.save()
        area = Area.objects.get(city = city)
        movie = Movies(
            movie_name=movie_name,
            genre=genre,
            added_by=added_by,
            area=area,
            description=description,
            duration=duration,
            )
    movie.save()
    return render(request, 'movie_admin/movie_added.html')


@login_required
def manage_movies(request):
    username = request.user
    user = User.objects.get(username=username)
    movie_admin = MovieAdmin.objects.get(movie_admin = user)
    movie_list = []
    movies = Movies.objects.filter(added_by=movie_admin)

    for movie in movies:
        movie_list.append(movie)
    return render(request, 'movie_admin/manage.html', {'movie_list': movie_list})


@login_required
def order_list(request):
    username = request.user
    user = User.objects.get(username=username)
    movie_admin = MovieAdmin.objects.get(movie_admin = user)
    orders = Orders.objects.filter(movie_admin = movie_admin)
    order_list = []

    for order in orders:
        if order.is_complete == False:
            order_list.append(order)
    return render(request, 'movie_admin/order_list.html', {'order_list': order_list})


@login_required
def complete(request):
    order_id = request.POST.get('id')
    order = Orders.objects.get(id = order_id)
    movie = order.movie
    order.is_complete = True
    order.save()
    movie.is_available = True
    movie.save()
    return HttpResponseRedirect('/movie_admin_portal/order_list/')


@login_required
def history(request):
    user = User.objects.get(username = request.user)
    movie_admin = MovieAdmin.objects.get(movie_admin = user)
    orders = Orders.objects.filter(movie_admin = movie_admin)
    order_list = []
    for order in orders:
        order_list.append(order)
    return render(request, 'movie_admin/history.html', {'wallet':movie_admin.wallet, 'order_list':order_list})


@login_required
def delete(request):
    movie_id = request.POST.get('id')
    movie = Movies.objects.get(id = movie_id)
    movie.delete()
    return HttpResponseRedirect('/movie_admin_portal/manage_movies/')


# ------------------ REST API ------------------

class MovieView(View):

    # Eliminating csfr to make POST requests
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, id=0):
        if (id > 0):
            movies = list(Movies.objects.filter(id=id).values())
            if len(movies) > 0:
                movie = movies[0]
                data = {
                    'message': "Success",
                    'movie': movie,
                }
            else:
                data = {'message': "Movie not found",}
            return JsonResponse(data)
        else:
            movies = list(Movies.objects.values())
            if len(movies) > 0:
                data = {
                    'message': "Success",
                    'movies': movies,
                }
            else:
                data = {'message': "Movies not found",}
            return JsonResponse(data)


    def post(self, request):
        data = {'message': "Success",}
        return JsonResponse(data)


    def patch(self, request, id):
        json_data = json.loads(request.body)
        movies = list(Movies.objects.filter(id=id).values())
        if len(movies) > 0:
            movie = Movies.objects.get(id=id)
            movie.name = json_data['movie_name']
            movie.duration = json_data['duration']
            movie.save()
            data = {'message': "Success",}
        else:
            data = {'message': "Movie not found",}
        return JsonResponse(data)


    def delete(self, request, id):
        pass
