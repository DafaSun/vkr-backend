# core/serializers.py
from rest_framework import serializers
from .models import Room, Price, Person, Guest, Booking, Occupancy

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'floor', 'building', 'capacity', 'category', 'room_type']

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'category', 'tour_price', 'hotel_price']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'surname', 'name', 'patronymic', 'birthday']

class GuestSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    class Meta:
        model = Guest
        fields = ['id', 'person', 'tour_type', 'age', 'gender', 'room', 'building', 'email', 'phone',
                  'home_address_country', 'home_address_region', 'home_address_city', 'home_address_street_and_house']

class BookingSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    room = RoomSerializer()
    class Meta:
        model = Booking
        fields = ['id', 'person', 'gender', 'room', 'place', 'check_in', 'check_out', 'status',
                  'total_price', 'has_breakfast', 'has_lunch', 'has_dinner', 'tour_type', 'prepayment_percent',
                  'prepayment_money']

class OccupancySerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    booking = BookingSerializer()
    class Meta:
        model = Occupancy
        fields = ['id', 'room', 'booking', 'date', 'status', 'gender']
