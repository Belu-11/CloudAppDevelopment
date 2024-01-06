import json
import logging
from datetime import datetime
from django.conf import settings
from decouple import config
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import *
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_reviews_from_cf, get_dealers_by_state, post_request, get_dealer_carmodels
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *

import requests

logger = logging.getLogger(__name__)

class ReactView(APIView):
    def get(self, request):
        output = [
            {"employee": output.employee,
            "department": output.department}
            for output in React.objects.all()]
        return Response(output)

    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:main')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'onlinecourse/login.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:main')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
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
            return redirect("djangoapp:main")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = config('BASE_URL') + 'dealerships'
        dealerships = get_dealers_from_cf(url, db_name='dealerships')
        context = {'dealership_list': dealerships}
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = config('BASE_URL') + 'dealerships'
        reviews = get_dealer_reviews_from_cf(url, db_name='reviews', dealer_id=dealer_id)
        dealer_details = get_dealer_by_id(url, db_name='dealerships', dealer_id=dealer_id)
        context = {'reviews': reviews, 'dealer':  dealer_details[0]}
        return render(request, 'djangoapp/dealer_details.html', context)


def get_state_dealerships(request, state):
    context = {}
    if request.method == 'GET':
        url = config('BASE_URL') + 'dealerships'
        state_dealerships = get_dealers_by_state(url, db_name='dealerships', state=state)
        context = {'dealers': state_dealerships}
        return render(request, 'djangoapp/index.html', context)


@login_required
def add_review(request, dealer_id):
    context = {}

    if request.method == "POST":
        review = {}
        
        car_id = request.POST['car']
        car_details = CarModel.objects.filter(dealer_id=dealer_id, id=car_id)

        for car in car_details:
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["name"] = request.user.username
            review["purchase"] = request.POST['purchasecheck']
            review["purchase_date"] = request.POST['purchasedate']
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year
            review["review"] = request.POST['content']

            json_payload = {"review": review}

            print(f"========== add_review =========== json payload {json_payload}")

            url = config('BASE_URL') + 'reviews'
            post_request(url, json_payload, db_name="reviews", dealer_id=dealer_id)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        # form = ReviewForm(data, dealership=dealer_id, name=request.user.username)
        # if form.is_valid():
        #     data = form.cleaned_data.copy()
        #     data["purchase_date"] = data["purchase_date"].strftime("%m/%d/%Y")
        #     car = CarModel.objects.get(pk=data["car"])
        #     data["car_make"] = car.make.name
        #     data["car_model"] = car.name
        #     data["car_year"] = car.year.year
        #     post_request(url, {"review":data})
        #     return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        # else:
        #     return render(request, 'djangoapp/add_review.html', {'dealer_id': dealer_id, 'form': form})
    else:
        dealer_details = get_dealer_carmodels(db_name="dealerships", dealer_id=dealer_id)
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = {'dealer_id': dealer_id, 'cars': list(cars), 'dealer':dealer_details[0]}
        return render(request, 'djangoapp/add_review.html', context)
        # return render(request, 'djangoapp/add_review.html', {'dealer_id': dealer_id, 'form': ReviewForm(dealership=dealer_id, name=request.user.username)})
        # return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
