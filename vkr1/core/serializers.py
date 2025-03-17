from rest_framework import serializers
from datetime import date, timedelta
from .models import Room, Place, Guest, Booking, RoomPrice

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = "__all__"

class RoomPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPrice
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def validate_date(self, value):
        max_date = date.today() + timedelta(days=365 * 1.5)
        if value > max_date:
            raise serializers.ValidationError(f"Дата не может быть позднее {max_date.strftime('%d.%m.%Y')}")
        return value

class BookingNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["surname", "name", "patronymic", "birthday",
                  "phone", "checkin", "checkout", "place_id", "gender"]

    def validate_date(self, value):
        max_date = date.today() + timedelta(days=365 * 1.5)
        if value > max_date:
            raise serializers.ValidationError(f"Дата не может быть позднее {max_date.strftime('%d.%m.%Y')}")
        return value
