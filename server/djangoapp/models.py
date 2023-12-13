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

class CarMake(models.Model):
	name = models.CharField(null=False, max_length=255, default='Toyota')
	descripton = models.CharField(max_length=1000)
	
	def __str__(self):
		return "Name: " + self.name + "," + \
			"Description: " + self.description


class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as needed
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.CharField(max_length=50)  # Assuming dealer_id is a string
    car_type = models.CharField(max_length=10, choices=CAR_TYPES)
    year = models.DateField()


    def __str__(self):
        return f"Car Make: {self.car_make} - Name:{self.name} - Dealer:{self.dealer_id} - Car Type:{self.car_type} ({self.year.year})"
	

class CarDealer:
    def __init__(self, dealer_id, name, location):
        self.dealer_id = dealer_id
        self.name = name
        self.location = location


class DealerReview:
    def __init__(self, rating, comment, reviewer_name):
        self.rating = rating
        self.comment = comment
        self.reviewer_name = reviewer_name

