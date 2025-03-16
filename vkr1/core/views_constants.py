from rest_framework.views import APIView
from rest_framework.response import Response
from .constants import *


class FloorsView(APIView):
    def get(self, request):
        return Response(dict(FLOORS_LIST))


class BuildingsView(APIView):
    def get(self, request):
        return Response(dict(BUILDINGS_LIST))


class CategoriesView(APIView):
    def get(self, request):
        return Response(dict(CATEGORIES_LIST))


class RoomTypesView(APIView):
    def get(self, request):
        return Response(dict(ROOM_TYPES_LIST))


class TourTypesView(APIView):
    def get(self, request):
        return Response(dict(TOUR_TYPES_LIST))


class BookingStatusesView(APIView):
    def get(self, request):
        return Response(dict(BOOKING_STATUSES_LIST))


class GenderRoomView(APIView):
    def get(self, request):
        return Response(dict(GENDER_ROOM_LIST))


class GenderPersonView(APIView):
    def get(self, request):
        return Response(dict(GENDER_PERSON_LIST))
