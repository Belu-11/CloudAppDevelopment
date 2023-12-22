import json
import logging
from datetime import datetime
from django.conf import settings
from decouple import config
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_reviews_from_cf, get_dealers_by_state
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.serializers import serialize

import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'onlinecourse/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = config('BASE_URL') + 'dealerships'
        dealerships = get_dealers_from_cf(url, db_name='dealerships')
        # print(f"dealerships {str(dealerships)}")

        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])

        context = {'dealerships': dealerships}
        # return render(request, 'djangoapp/index.html', context)
        return JsonResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = config('BASE_URL') + 'dealerships'
        reviews = get_dealer_reviews_from_cf(url, db_name='reviews', dealer_id=dealer_id)
        new_reviews = obj_to_dict(reviews, 'reviews')
        print()
        dealer_details = get_dealer_by_id(url, db_name='dealerships', dealer_id=dealer_id)
        new_dealer_details = obj_to_dict(dealer_details, 'dealerships')
        context = {'reviews': new_reviews, 'dealer':  new_dealer_details, 'MEDIA_URL': settings.MEDIA_URL}
        # return render(request, 'djangoapp/index.html', context)
        return JsonResponse(context)


def get_state_dealerships(request, state):
    context = {}
    if request.method == 'GET':
        url = config('BASE_URL') + 'dealerships'
        state_dealerships = get_dealers_by_state(url, db_name='dealerships', state=state)
        # print(f'state_dealerships {str(state_dealerships)}')
        context = {'dealers': state_dealerships}
        # return render(request, 'djangoapp/index.html', context)
        return HttpResponse(context)

def obj_to_dict(object_list, type):
    new_list = []
    if type == 'reviews':
        for obj in object_list:
            new_dict = {"dealership":obj.dealership, "name":obj.name, "purchase":obj.purchase,
                    "review":obj.review, "purchase_date":obj.purchase_date, "car_make":obj.car_make,
                    "car_model":obj.car_model, "car_year":obj.car_year,
                    "sentiment":obj.review, "id":obj.id}
            new_list.append(new_dict)
                
    if type == 'dealerships':
        for obj in object_list:
            new_dict = { "address": obj.address, "city": obj.city, "full_name":obj.full_name,
                    "id":obj.id, "lat":obj.lat, "long":obj.long,
                    "short_name":obj.short_name,"state":obj.state,
                    "zip":obj.zip}
            new_list.append(new_dict)
    
    print(f"type:{type} new list -> {new_list}")

    return new_list


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

