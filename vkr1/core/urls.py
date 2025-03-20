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
    path("manager/bookings/", ManagerBookingsAPIView.as_view(), name="bookings"),
    path("manager/booking/place_name/", ManagerBookingPlaceNameAPIView.as_view(), name="bookings"),
    path("manager/bookings/record/", ManagerBookingsRecordGetAPIView.as_view(), name="bookings_record"),
    path("manager/bookings/record/delete/", ManagerBookingsRecordDeleteAPIView.as_view(), name="bookings_record_delete"),
    path("manager/bookings/record/update/", ManagerBookingsRecordUpdateAPIView.as_view(), name="bookings_record_update"),
    path("manager/rooms/", ManagerRoomsTableAPIView.as_view(), name="rooms"),
    path("manager/guests/", ManagerGuestsAPIView.as_view(), name="guests"),
    path("manager/guests/person/", ManagerGuestsGetPersonAPIView.as_view(), name="guests_person"),
    path("manager/guests/new/", ManagerGuestsNewPersonAPIView.as_view(), name="guests_person"),
    path("manager/guests/person/update/", ManagerGuestsEditPersonAPIView.as_view(), name="guests_person"),
    path("manager/guests/person/delete/", ManagerGuestsDeletePersonAPIView.as_view(), name="guests_person"),
]
