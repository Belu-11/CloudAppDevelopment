from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
	model = CarModel


class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'dealer_id', 'car_type', 'year']
    search_fields = ['name', 'car_type']


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)