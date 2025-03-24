from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from .constants import *


class Categories(models.Model):
    label = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    floor = models.CharField(choices=FLOORS_LIST)
    building = models.CharField(choices=BUILDINGS_LIST)
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
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


class RoomPrice(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    tour_price = models.DecimalField(decimal_places=2, max_digits=10)
    hotel_price = models.DecimalField(decimal_places=2, max_digits=10)
    date_begin = models.DateField(validators=[MinValueValidator(date.today())])
    date_end = models.DateField(null=True, blank=True)


class NutritionPrice(models.Model):
    nutrition = models.CharField(choices=NUTRITION_LIST)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    date_begin = models.DateField(validators=[MinValueValidator(date.today())])
    date_end = models.DateField(null=True, blank=True)


class BookingRecords(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    checkin = models.DateField(validators=[MinValueValidator(date.today())])
    checkout = models.DateField(validators=[MinValueValidator(date.today())])
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    status = models.CharField(choices=BOOKING_STATUSES_LIST, default="free")
    total_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    prepayment_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                             blank=True)
    prepayment_money = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    tour_type = models.CharField(choices=TOUR_TYPES_LIST)
    has_breakfast = models.BooleanField(default=False)
    has_lunch = models.BooleanField(default=False)
    has_dinner = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        max_date = date.today() + timedelta(days=365 * 1.5)
        if self.checkin > max_date:
            raise ValidationError(f"Дата заезда не может быть позднее {max_date.strftime('%d.%m.%Y')}")
        if self.checkout > max_date:
            raise ValidationError(f"Дата отъезда не может быть позднее {max_date.strftime('%d.%m.%Y')}")


class Booking(models.Model):
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    date = models.DateField(validators=[MinValueValidator(date.today())])
    status = models.CharField(choices=BOOKING_STATUSES_LIST, default="free")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True)
    gender = models.CharField(choices=GENDER_ROOM_LIST, default="undefined")
    record = models.ForeignKey(BookingRecords, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        super().clean()
        max_date = date.today() + timedelta(days=365 * 1.5)
        if self.date > max_date:
            raise ValidationError(f"Дата не может быть позднее {max_date.strftime('%d.%m.%Y')}")


class Patient(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT)
    date_in = models.DateField()
    date_out = models.DateField()
    first_visit = models.BooleanField(default=False)
    second_visit = models.BooleanField(default=False)


class MedicalWorkers(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(validators=[MaxValueValidator(date.today())])
    speciality = models.CharField(choices=SPECIALITY_LIST)
    is_available = models.BooleanField(default=True)


class FirstVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    view_data = models.DateField()
    view_time = models.TimeField()
    doctor = models.ForeignKey(MedicalWorkers, on_delete=models.PROTECT)
    complaints = models.TextField()
    medical_story = models.TextField()
    genetics = models.TextField()
    allergy = models.TextField()
    previous_ills = models.TextField()
    tuberculosis = models.BooleanField()
    hepatitis = models.CharField(choices=HEPATITIS_LIST)
    venerealIlls = models.TextField()
    operations = models.TextField()
    smoking = models.BooleanField()
    alcohol = models.BooleanField()
    menstruation_reg = models.BooleanField(null=True)
    last_menstruation = models.DateField(null=True)
    menopause = models.CharField(max_length=100, null=True)
    general = models.CharField(choices=STATES_LIST)
    body = models.CharField(choices=BODIES_LIST)
    skin = models.CharField(choices=SKIN_LIST)
    skin_rash_details = models.CharField(max_length=100, null=True)
    skin_wetness = models.CharField(choices=SKIN_WETNESS_LIST)
    pulse = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    pressure = models.CharField(max_length=10)
    breath_type = models.CharField(choices=BREATH_TYPE_LIST)
    breath_type_details = models.CharField(max_length=100, null=True)
    rales = models.CharField(choices=RALES_LIST)
    rales_details = models.CharField(max_length=100, null=True)
    breath_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    heart_rhythm = models.CharField(choices=HEART_RHYTHM_LIST)
    heart_clarity = models.CharField(choices=HEART_CLARITY_LIST)
    heart_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    heart_murmurs = models.CharField(choices=HEART_MURMURS_LIST)
    heart_murmurs_details = models.CharField(max_length=100, null=True)
    accents = models.CharField(choices=ACCENTS_LIST)
    accents_details = models.CharField(max_length=100, null=True)
    tongue_wetness = models.CharField(choices=TONGUE_WETNESS_LIST)
    tongue_raid = models.CharField(choices=TONGUE_RAID_LIST)
    tongue_raid_details = models.CharField(max_length=100, null=True)
    belly_softness = models.CharField(choices=BELLY_SOFTNESS_LIST)
    belly_painnnes = models.CharField(choices=PAIN_LIST)
    belly_painnnes_details = models.CharField(max_length=100, null=True)
    liver_size = models.CharField(choices=LIVER_SIZE_LIST)
    liver_size_details = models.CharField(max_length=20, null=True)
    liver_painness = models.CharField(choices=PAIN_LIST)
    kidneys_shaking = models.CharField(choices=KIDNEYS_SHAKING_LIST)
    urination_painness = models.CharField(choices=PAIN_LIST)
    urination_freeness = models.CharField(choices=URINATION_FREENESS_LIST)
    edema = models.CharField(choices=EDEMA_LIST)
    edema_details = models.CharField(max_length=100, null=True)
    chair_dec = models.CharField(choices=CHAIR_DEC_LIST)
    chair_reg = models.CharField(choices=CHAIR_REG_LIST)
    chair_reg_details = models.CharField(max_length=100, null=True)
    conscience = models.CharField(choices=CONSCIENCE_LIST)
    conscience_details = models.CharField(max_length=100, null=True)
    orientation = models.CharField(choices=ORIENTATION_LIST)
    cranial_nervous = models.CharField(max_length=100, null=True)
    muscle_tone = models.CharField(max_length=100, null=True)
    muscle_power = models.CharField(max_length=100, null=True)
    tendon_reflexes = models.CharField(max_length=100, null=True)
    sensitivity = models.CharField(choices=SENSITIVITY_LIST)
    sensitivity_details = models.CharField(max_length=100, null=True)
    romberg_pose = models.CharField(choices=ROMBERG_POSE_LIST)
    romberg_pose_details = models.CharField(max_length=100, null=True)
    finger_test = models.CharField(choices=FINGER_TEST_LIST)
    finger_test_details = models.CharField(max_length=100, null=True)
    spine_deform = models.CharField(choices=DEFORM_LIST)
    spine_deform_details = models.CharField(max_length=100, null=True)
    spine_motion_limit = models.CharField(choices=SPINE_MOTION_LIMIT_LIST)
    spine_motion_painness = models.CharField(choices=PAIN_LIST)
    spine_motion_painness_details = models.CharField(max_length=100, null=True)
    paravertebral_points = models.CharField(choices=PAIN_LIST)
    paravertebral_points_details = models.CharField(max_length=100, null=True)
    lasega_sypthom_right = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    lasega_sypthom_left = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    joints_deform = models.CharField(choices=DEFORM_LIST)
    joints_deform_details = models.CharField(max_length=100, null=True)
    joints_palpation_painness = models.CharField(choices=PAIN_LIST)
    joints_palpation_painness_details = models.CharField(max_length=100, null=True)
    joints_motion_painness = models.CharField(choices=PAIN_LIST)
    joints_motion_painness_details = models.CharField(max_length=100, null=True)
    joints_motion_volume = models.CharField(choices=JOINTS_MOTION_VOLUME_LIST)
    joints_motion_volume_details = models.CharField(max_length=100, null=True)
    main_diagnosisMKB = models.CharField(max_length=20)
    main_diagnosis = models.TextField()
    concomitant_diagnosisMKB = models.CharField(max_length=20)
    concomitant_diagnosis = models.TextField()
    therapy_plan = models.TextField()


class SecondVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    view_data = models.DateField()
    view_time = models.TimeField()
    doctor = models.ForeignKey(MedicalWorkers, on_delete=models.PROTECT)
    recomendation = models.TextField()
    result_reason = models.TextField(null=True)
    result = models.CharField(choices=THERAPY_RESULT_LIST)


class Dairy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_visit = models.DateField()
    description = models.TextField()

class Procedure(models.Model):
    name=models.CharField(max_length=100, unique=True)
    label=models.CharField(max_length=100)
    category=models.CharField(choices=PROCEDURE_CATEGORIES_LIST)
    price=models.DecimalField(decimal_places=2, max_digits=10)
    is_available=models.BooleanField(default=True)
    parameters=models.TextField(null=True)


class RegisterRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    procedure=models.ForeignKey(Procedure, on_delete=models.PROTECT)
    first_date=models.DateField()
    number=models.IntegerField()
    periodicity=models.CharField(choices=PERIODICITY_LIST)
    notes=models.TextField(null=True)


class Register(models.Model):
    record=models.ForeignKey(RegisterRecord, on_delete=models.PROTECT)
    date=models.DateField()
    time=models.TimeField()
    is_completed=models.BooleanField(default=False)
    medical_worker=models.ForeignKey(MedicalWorkers, on_delete=models.PROTECT)
    medical_room=models.CharField(choices=MEDICAL_ROOMS_LIST)
