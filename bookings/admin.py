from django.contrib import admin
from .models import (
    Customer,
    VaccineCenter,
    Booking,
    DeleteVaccineCenter,
    QueryCount,
    QueryTodayCount
)


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_dispaly = ['id', 'user', 'name', 'age',
                    'locality', 'city', 'zipcode', 'state']

@admin.register(VaccineCenter)
class VaccineCentertModelAdmin(admin.ModelAdmin):
    list_display=['name','start_time','end_time']

@admin.register(DeleteVaccineCenter)
class DeleteVaccineCentertModelAdmin(admin.ModelAdmin):
    list_display=['name']

@admin.register(Booking)
class BookingModelAdmin(admin.ModelAdmin):
    list_display=['id','user','vaccine_center','date',]

@admin.register(QueryCount)
class QueryModelAdmin(admin.ModelAdmin):
    list_display=['id','curr_date','today_total']

@admin.register(QueryTodayCount)
class QueryTodayModelAdmin(admin.ModelAdmin):
    list_display=['curr_date','today_total']
    