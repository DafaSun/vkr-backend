from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta
from django.core.exceptions import ValidationError


class Room(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True, blank=False)
    FLOOR_LIST = [
        ('1', '1 этаж'),
        ('2', '2 этаж')
    ]
    floor = models.IntegerField(null=False, unique=False, blank=False, choices=FLOOR_LIST)
    BUILDING_LIST = [
        ('4', '4 корпус'),
        ('5', '5 корпус'),
        ('6', '6 корпус')
    ]
    building = models.IntegerField(null=False, unique=False, blank=False, choices=BUILDING_LIST)
    capacity = models.IntegerField(null=False, unique=False, blank=False,
                                   validators=[MinValueValidator(1), MaxValueValidator(3)])
    CATEGORY_LIST = [
        ('1', 'Двухкомнатный номер на 1 этаже в 4 корпусе с удобствами в номере'),
        ('2', 'Двухместный номер на 1 этаже в 4 корпусе с удобствами в блоке'),
        ('3', 'Двухместный номер на 1 этаже в 4 корпусе с удобствами в номере'),
        ('4', 'Одноместный номер на 1 этаже в 4 корпусе с удобствами в номере'),
        ('5', 'Двухместный номер на 2 этаже в 4 корпусе с удобствами в блоке'),
        ('6', 'Двухместный номер на 1 этаже в 6 корпусе с удобствами в номере'),
        ('7', 'Двухместный номер на 2 этаже в 6 корпусе с удобствами в номере')
    ]
    category = models.IntegerField(null=False, unique=False, blank=False, choices=CATEGORY_LIST)
    ROOM_TYPE_LIST = [
        ('1', 'Удобства в номере'),
        ('2', 'Удобства на этаже')
    ]
    room_type = models.IntegerField(null=False, unique=False, blank=False, choices=ROOM_TYPE_LIST)


class Price(models.Model):
    CATEGORY_LIST = [
        ('1', 'Двухкомнатный номер на 1 этаже в 4 корпусе с удобствами в номере'),
        ('2', 'Двухместный номер на 1 этаже в 4 корпусе с удобствами в блоке'),
        ('3', 'Двухместный номер на 1 этаже в 4 корпусе с удобствами в номере'),
        ('4', 'Одноместный номер на 1 этаже в 4 корпусе с удобствами в номере'),
        ('5', 'Двухместный номер на 2 этаже в 4 корпусе с удобствами в блоке'),
        ('6', 'Двухместный номер на 1 этаже в 6 корпусе с удобствами в номере'),
        ('7', 'Двухместный номер на 2 этаже в 6 корпусе с удобствами в номере')
    ]
    category = models.IntegerField(null=False, unique=False, blank=False, choices=CATEGORY_LIST)
    tour_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, unique=False)
    hotel_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, unique=False)


class Person(models.Model):
    surname = models.CharField(max_length=100, null=False, unique=False, blank=False)
    name = models.CharField(max_length=100, null=False, unique=False, blank=False)
    patronymic = models.CharField(max_length=100, null=True, unique=False, blank=False)
    birthday = models.DateField(null=False, blank=False, unique=False, validators=[
        MinValueValidator(limit_value=date(1908, 6, 8)),
        MaxValueValidator(limit_value=date.today())
    ])


class Guest(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    TOUR_TYPE_LIST = [
        ('1', 'Социальная путевка по контракту (льгота)'),
        ('2', 'Обычная путевка за свои деньги'),
        ('3', 'Только проживание')
    ]
    tour_type = models.IntegerField(null=False, unique=False, blank=False, choices=TOUR_TYPE_LIST)
    age = models.IntegerField(null=False, unique=False, blank=False,
                              validators=[MinValueValidator(0), MaxValueValidator(117)])
    GENDER_LIST = [
        ('1', 'Мужской'),
        ('2', 'Женский')
    ]
    gender = models.IntegerField(null=False, unique=False, blank=False, choices=GENDER_LIST)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    BUILDING_LIST = [
        ('4', '4 корпус'),
        ('5', '5 корпус'),
        ('6', '6 корпус')
    ]
    building = models.IntegerField(null=False, unique=False, blank=False, choices=BUILDING_LIST)
    email = models.EmailField(null=True, unique=False, blank=True)
    phone = models.CharField(max_length=15, null=False, unique=False, blank=False)
    home_address_country = models.CharField(max_length=30, null=False, unique=False, blank=False)
    home_address_region = models.CharField(max_length=30, null=False, unique=False, blank=False)
    home_address_city = models.CharField(max_length=30, null=False, unique=False, blank=False)
    home_address_street_and_house = models.CharField(max_length=70, null=False, unique=False, blank=False)


class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    GENDER_LIST = [
        ('1', 'Мужской'),
        ('2', 'Женский')
    ]
    gender = models.IntegerField(null=False, unique=False, blank=False, choices=GENDER_LIST)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    place = models.IntegerField(null=False, unique=False, blank=False,
                                validators=[MinValueValidator(1), MaxValueValidator(3)])
    check_in = models.DateField(null=False, blank=False, unique=False,
                               validators=[MinValueValidator(limit_value=date(2025, 1, 1))])
    check_out = models.DateField(null=False, blank=False, unique=False,
                               validators=[MinValueValidator(limit_value=date(2025, 1, 1))])
    BOOKING_STATUS_LIST = [
        ('1', 'Забронировано'),
        ('2', 'Внесена предоплата'),
        ('3', 'Полностью оплачен'),
        ('4', 'Заселен')
    ]
    status = models.IntegerField(null=False, unique=False, blank=False, choices=BOOKING_STATUS_LIST)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, unique=False)
    has_breakfast=models.BooleanField(null=True, unique=False, blank=True)
    has_lunch=models.BooleanField(null=True, unique=False, blank=True)
    has_dinner=models.BooleanField(null=True, unique=False, blank=True)
    TOUR_TYPE_LIST = [
        ('1', 'Социальная путевка по контракту (льгота)'),
        ('2', 'Обычная путевка за свои деньги'),
        ('3', 'Только проживание')
    ]
    tour_type = models.IntegerField(null=False, unique=False, blank=False, choices=TOUR_TYPE_LIST)
    prepayment_percent=models.IntegerField(null=False, blank=False, unique=False,
                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    prepayment_money=models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, unique=False)

    def clean(self):
        super().clean()
        max_date = date.today() + timedelta(days=365 * 1.5)
        if self.check_in > max_date:
            raise ValidationError(f"Дата заезда не может быть позднее {max_date.strftime('%d.%m.%Y')}")
        if self.check_out > max_date:
            raise ValidationError(f"Дата отъезда не может быть позднее {max_date.strftime('%d.%m.%Y')}")
        if self.check_in > self.check_out:
            raise ValidationError(f"Дата заезда не может быть позднее даты отъезда")


class Occupancy(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT)
    date = models.DateField(null=False, blank=False, unique=False)
    ROOM_STATUS_LIST = [
        ('1', 'Забронировано'),
        ('2', 'Внесена предоплата'),
        ('3', 'Полностью оплачен'),
        ('4', 'Заселен')
    ]
    status = models.IntegerField(null=False, unique=False, blank=False, choices=ROOM_STATUS_LIST)
    GENDER_LIST = [
        ('1', 'Мужской'),
        ('2', 'Женский'),
        ('3', 'Не указан'),
        ('4', 'Желательно мужской'),
        ('5', 'Желательно женский')
    ]
    gender = models.IntegerField(null=False, unique=False, blank=False, choices=GENDER_LIST)

    def clean(self):
        super().clean()
        max_date = date.today() + timedelta(days=365 * 1.5)
        if self.date > max_date:
            raise ValidationError(f"Дата не может быть позднее {max_date.strftime('%d.%m.%Y')}")