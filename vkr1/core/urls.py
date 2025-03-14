from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import RoomViewSet, PriceViewSet, PersonViewSet, GuestViewSet, BookingViewSet, OccupancyViewSet
from django.urls import path
from .views import TourCategoryListView

router = DefaultRouter()
# router.register(r'rooms', RoomViewSet)
# router.register(r'prices', PriceViewSet)
# router.register(r'persons', PersonViewSet)
# router.register(r'guests', GuestViewSet)
# router.register(r'bookings', BookingViewSet)
# router.register(r'occupancies', OccupancyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("api/manager/tour/tour/", TourCategoryListView.as_view(), name="tour-categories"),
]
