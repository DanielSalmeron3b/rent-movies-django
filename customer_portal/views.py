from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
from movie_admin_portal.models import *
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'customer/login.html')
    else:
        return render(request, 'customer/home_page.html')


def login(request):
    return render(request, 'customer/login.html')


def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'customer/home_page.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, 
            username=username, 
            password=password
            )
        try:
            customer = Customer.objects.get(user = user)
        except:
            customer = None
        if customer is not None:
            auth.login(request, user)
            return render(request, 'customer/home_page.html')
        else:
            return render(request, 'customer/login_failed.html')


def logout_view(request):
    auth.logout(request)
    return render(request, 'customer/login.html')


def register(request):
    return render(request, 'customer/register.html')


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
            email = email
            )
        user.name = name
        user.save()
    except:
        return render(request, 'customer/registration_error.html')

    try:
        area = Area.objects.get(city=city)
    except:
        area = None

    if area is not None:
        customer = Customer(
            user=user, 
            phone_number=phone_number, 
            area=area
            )
    else:
        area = Area(city=city)
        area.save()
        area = Area.objects.get(city = city)
        customer = Customer(
            user=user, 
            phone_number=phone_number, 
            area = area
            )
    
    customer.save()

    return render(request, 'customer/registered.html')


@login_required
def search(request):
    return render(request, 'customer/search.html')


# NEED TO CHANGE THIS --------------------------------------------
@login_required
def search_results(request):
    city = request.POST.get('city')
    city = city.lower()
    movies_list = []
    area = Area.objects.filter(city=city)
    
    for a in area:
        movies = Movies.objects.filter(area = a)
        for movie in movies:
            if movie.is_available == True:
                movie_dictionary = {
                    "name": movie.movie_name,
                    "genre": movie.genre,
                    "id": movie.id,
                    "duration": movie.duration,
                    "description": movie.description,
                }
                movies_list.append(movie_dictionary)

    request.session['movies_list'] = movies_list
    return render(request, 'customer/search_results.html')
# ----------------------------------------------------------------


@login_required
def rent_movie(request):
    id = request.POST.get('id')
    movie = Movies.objects.get(id=id)
    cost_per_day = int(movie.duration) * 13
    return render(request, 'customer/confirmation.html', {'movie': movie, 'cost_per_day': cost_per_day})


@login_required
def confirm(request):
    movie_id = request.POST.get('id')
    username = request.user
    user = User.objects.get(username=username)
    days = request.POST.get('days')
    movie = Movies.objects.get(id=movie_id)

    if movie.is_available:
        movie_admin = movie.added_by
        rent = (int(movie.duration))*13*(int(days))
        movie_admin.wallet += rent
        movie_admin.save()

        try:
            order = Orders(
                movie = movie,
                movie_admin = movie_admin,
                user=user,
                rent=rent,
                days=days
                )
            order.save()
        except:
            order = Orders.objects.get(
                movie = movie,
                movie_admin = movie_admin,
                user=user,
                rent=rent,
                days=days
            )
        movie.is_available = True
        movie.save()
        return render(request, 'customer/confirmed.html', {'order':order})
    else:
        return render(request, 'customer/order_failed.html')


@login_required
def manage(request):
    order_list = []
    user = User.objects.get(username = request.user)
    try:
        orders = Orders.objects.filter(user=user)
    except:
        orders = None

    if orders is not None:
        for order in orders:
            if order.is_complete == False:
                order_dictionary = {
                    "id": order.id,
                    "rent": order.rent,
                    "vehicle": order.vehicle,
                    "days": order.days,
                    "movie_admin": order.movie_admin,
                }
                order_list.append(order_dictionary)
    return render(request, 'customer/manage.html', {"order":order_list})


@login_required
def update_order(request):
    order_id = request.POST.get('id')
    order = Orders.objects.get(id = order_id)
    movie = order.movie
    movie.is_available = True
    movie.save()

    movie_admin = order.movie_admin
    movie_admin.wallet -= int(order.rent)
    movie_admin.save()

    order.delete()
    cost_per_day = int(movie.duration)*13

    return render(request, 'customer/confirmation.html', {"movie": movie}, {"cost_per_day":cost_per_day})


@login_required
def delete_order(request):
    order_id = request.POST.get('id')
    order = Orders.objects.get(id = order_id)
    movie_admin = order.movie_admin
    movie_admin.wallet -= int(order.rent)
    movie_admin.save()

    movie = order.movie
    movie.is_available = True
    movie.save()
    order.delete()

    return HttpResponseRedirect('/customer_portal/manage/')