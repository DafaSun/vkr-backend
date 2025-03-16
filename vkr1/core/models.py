from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from .constants import *


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    floor = models.CharField(choices=FLOORS_LIST)
    building = models.CharField(choices=BUILDINGS_LIST)
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    category = models.CharField(choices=CATEGORIES_LIST)
    room_type = models.CharField(choices=ROOM_TYPES_LIST)


class Place(models.Model):
    name = models.CharField(max_length=100, unique=True)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)


class Guest(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(choices=GENDER_PERSON_LIST)
    birthday = models.DateField(validators=[MinValueValidator(date(1908, 6, 8)), MaxValueValidator(date.today())])
    tour_type = models.CharField(choices=TOUR_TYPES_LIST)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    home_address_country = models.CharField(null=True, blank=True, max_length=30)
    home_address_region = models.CharField(null=True, blank=True, max_length=30)
    home_address_city = models.CharField(null=True, blank=True, max_length=30)
    home_address_street_and_house = models.CharField(null=True, blank=True, max_length=70)
    workplace = models.CharField(null=True, blank=True, max_length=100)
    prepayment_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    prepayment_money = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)


class Booking(models.Model):
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    date = models.DateField(validators=[MinValueValidator(date.today())])
    status = models.CharField(choices=BOOKING_STATUSES_LIST, default="free")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True)
    gender = models.CharField(choices=GENDER_ROOM_LIST, default="undefined")
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def clean(self):
        super().clean()
        max_date = date.today() + timedelta(days=365 * 1.5)
        if self.date > max_date:
            raise ValidationError(f"Дата не может быть позднее {max_date.strftime('%d.%m.%Y')}")


class RoomPrice(models.Model):
    category = models.CharField(choices=CATEGORIES_LIST)
    tour_price = models.DecimalField(decimal_places=2, max_digits=10)
    hotel_price = models.DecimalField(decimal_places=2, max_digits=10)
    date_begin = models.DateField(validators=[MinValueValidator(date.today())])
    date_end = models.DateField(null=True, blank=True)
