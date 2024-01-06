from django.db import models
from django.utils.timezone import now

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid
# Create your models here.

class React(models.Model):
    employee = models.CharField(max_length=50)
    department = models.CharField(max_length=200)


class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    
    def __str__(self):
        return f"{self.name} - {self.description}"


class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('VAN', 'Van'),
        ('TRUCK', 'Truck'),
        ('SPORT', 'Sport'),
        ('ROADSTER', 'Roadster'),
        # Add more choices as needed
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='CarModel')
    dealer_id = models.IntegerField(null=False)
    car_type = models.CharField(null=False, max_length=30, choices=CAR_TYPES, default=CAR_TYPES[0])
    year = models.DateField(null=False, default=now)

    def __str__(self):
        return f"{self.car_make} - {self.name} - {self.dealer_id} - {self.car_type} - {self.year}"
	

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.state = state
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

