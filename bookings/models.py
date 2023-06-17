from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from datetime import time

STATE_CHOICES = (
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttarakhand','Uttarakhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),   
)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    age = models.IntegerField()
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)

class VaccineCenter(models.Model):
    name = models.CharField(primary_key = True,max_length=100)
    start_time = models.TimeField(default=time(10, 0))
    end_time = models.TimeField(default=time(18, 0))

    def __str__(self):
        return str(self.name)
    # Additional fields and methods specific to the VaccineCenter model

class DeleteVaccineCenter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vaccine_center = models.ForeignKey(VaccineCenter, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.id)

class QueryCount(models.Model):
    curr_date=models.DateField()
    today_total=models.IntegerField()
    
    def __str__(self):
        return str(self.id)

class QueryTodayCount(models.Model):
    curr_date=models.DateField(primary_key = True)
    today_total=models.IntegerField()
    
    def __str__(self):
        return str(self.curr_date)




           



