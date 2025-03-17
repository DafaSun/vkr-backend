from django.urls import path
from .views_constants import *
from .views_manager import *

urlpatterns = [
    path("constants/floors/", FloorsView.as_view(), name="floors"),
    path("constants/buildings/", BuildingsView.as_view(), name="buildings"),
    path("constants/categories/", CategoriesView.as_view(), name="categories"),
    path("constants/room_types/", RoomTypesView.as_view(), name="room_types"),
    path("constants/tour_types/", TourTypesView.as_view(), name="tour_types"),
    path("constants/booking_statuses/", BookingStatusesView.as_view(), name="booking_statuses"),
    path("constants/gender_room/", GenderRoomView.as_view(), name="gender_room"),
    path("constants/gender_person/", GenderPersonView.as_view(), name="gender_person"),

    path("manager/categories/", ManagerAvailableCategoriesAPIView.as_view(), name="categories"),
    path("manager/categories/places/", ManagerAvailablePlacesAPIView.as_view(), name="categories_places"),
    path("manager/booking/new/", ManagerBookingNewAPIView.as_view(), name="booking_new"),
    path("manager/bookings", ManagerBookingsAPIView.as_view(), name="bookings"),
]
