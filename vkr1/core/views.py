# from rest_framework import viewsets
# from rest_framework.permissions import AllowAny
# from .models import Room, Price, Person, Guest, Booking, Occupancy
# from .serializers import RoomSerializer, PriceSerializer, PersonSerializer, GuestSerializer, BookingSerializer, \
#     OccupancySerializer
#
#
# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     permission_classes = [AllowAny]
#
#
# class PriceViewSet(viewsets.ModelViewSet):
#     queryset = Price.objects.all()
#     serializer_class = PriceSerializer
#     permission_classes = [AllowAny]
#
#
# class PersonViewSet(viewsets.ModelViewSet):
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializer
#     permission_classes = [AllowAny]
#
#
# class GuestViewSet(viewsets.ModelViewSet):
#     queryset = Guest.objects.all()
#     serializer_class = GuestSerializer
#     permission_classes = [AllowAny]
#
#
# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = [AllowAny]
#
#
# class OccupancyViewSet(viewsets.ModelViewSet):
#     queryset = Occupancy.objects.all()
#     serializer_class = OccupancySerializer
#     permission_classes = [AllowAny]
#
#
# from django.utils.dateparse import parse_date
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.db.models import F
# from rest_framework.permissions import AllowAny
# from datetime import timedelta
# from .models import Room, Price, Booking
#
# from django.db.models import Case, When, Value, IntegerField
#
#
#
# class TourCategoryListView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request):
#         checkin = request.GET.get("checkin")
#         checkout = request.GET.get("checkout")
#         people = request.GET.get("people")
#         gender = request.GET.get("gender")
#         tour_type = request.GET.get("tour_type")
#
#         if not all([checkin, checkout, people, gender, tour_type]):
#             return Response({"error": "Все параметры должны быть указаны"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             checkin_date = parse_date(checkin)
#             checkout_date = parse_date(checkout)
#             people = int(people)
#             gender = int(gender)
#             tour_type = int(tour_type)
#         except (ValueError, TypeError):
#             return Response({"error": "Неверный формат параметров"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if checkin_date >= checkout_date:
#             return Response({"error": "Дата заезда должна быть раньше даты выезда"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Получаем все категории номеров, которые соответствуют количеству людей
#         available_rooms = Room.objects.filter(capacity__gte=people)
#
#         # Исключаем уже забронированные номера на эти даты
#         booked_rooms = Booking.objects.filter(
#             check_in__lt=checkout_date, check_out__gt=checkin_date
#         ).values_list("room_id", flat=True)
#
#         available_rooms = available_rooms.exclude(id__in=booked_rooms)
#
#         # Получаем цены для доступных категорий и добавляем текстовые названия категорий
#         categories = (
#             Price.objects.filter(category__in=available_rooms.values("category"))
#             .annotate(category_name=F("category"))
#             .values("category_name", "category", "tour_price")
#         )
#
#         response_data = [
#             {
#                 "category_name": Room.objects.get(id=category["category"]).get_category_display(),
#                 "category_number": category["category"],
#                 "price": category["tour_price"]
#             }
#             for category in categories
#         ]
#
#         return Response(response_data, status=status.HTTP_200_OK)
#
#
# class TourCategoryListView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request):
#         checkin = request.GET.get("checkin")
#         checkout = request.GET.get("checkout")
#         people = request.GET.get("people")
#         gender = request.GET.get("gender")
#         tour_type = request.GET.get("tour_type")
#
#         if not all([checkin, checkout, people, gender, tour_type]):
#             return Response({"error": "Все параметры должны быть указаны"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             checkin_date = parse_date(checkin)
#             checkout_date = parse_date(checkout)
#             people = int(people)
#             gender = int(gender)
#             tour_type = int(tour_type)
#         except (ValueError, TypeError):
#             return Response({"error": "Неверный формат параметров"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if checkin_date >= checkout_date:
#             return Response({"error": "Дата заезда должна быть раньше даты выезда"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Получаем все категории номеров
#         available_rooms = Room.objects.filter(capacity__gte=people)
#
#         # Исключаем уже забронированные номера на эти даты
#         booked_rooms = Booking.objects.filter(
#             check_in__lt=checkout_date, check_out__gt=checkin_date
#         ).values_list("room_id", flat=True)
#
#         available_rooms = available_rooms.exclude(id__in=booked_rooms)
#
#         # Получаем цены для доступных категорий
#         categories = (
#             Price.objects.filter(category__in=available_rooms.values("category"))
#             .annotate(category_name=F("category"))
#             .values("category_name", "category", "tour_price")
#         )
#
#         response_data = [
#             {
#                 "category_name": category["category_name"],
#                 "category_number": category["category"],
#                 "price": category["tour_price"]
#             }
#             for category in categories
#         ]
#
#         return Response(response_data, status=status.HTTP_200_OK)
#


from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from rest_framework.permissions import AllowAny
from .models import Room, Price, Booking

class TourCategoryListView(APIView):
    permission_classes = [AllowAny]

    # Маппинг категорий (можно добавить/изменить текстовые значения по мере необходимости)
    CATEGORY_MAPPING = {
        '1': 'Двухкомнатный номер на 1 этаже в 4 корпусе с удобствами в номере',
        '2': 'Двухместный номер на 1 этаже в 4 корпусе с удобствами в блоке',
        '3': 'Двухместный номер на 1 этаже в 4 корпусе с удобствами в номере',
        '4': 'Одноместный номер на 1 этаже в 4 корпусе с удобствами в номере',
        '5': 'Двухместный номер на 2 этаже в 4 корпусе с удобствами в блоке',
        '6': 'Двухместный номер на 1 этаже в 6 корпусе с удобствами в номере',
        '7': 'Двухместный номер на 2 этаже в 6 корпусе с удобствами в номере',
    }

    def get(self, request):
        checkin = request.GET.get("checkin")
        checkout = request.GET.get("checkout")
        people = request.GET.get("people")
        gender = request.GET.get("gender")
        tour_type = request.GET.get("tour_type")

        if not all([checkin, checkout, people, gender, tour_type]):
            return Response({"error": "Все параметры должны быть указаны"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            checkin_date = parse_date(checkin)
            checkout_date = parse_date(checkout)
            people = int(people)
            gender = int(gender)
            tour_type = int(tour_type)
        except (ValueError, TypeError):
            return Response({"error": "Неверный формат параметров"}, status=status.HTTP_400_BAD_REQUEST)

        if checkin_date >= checkout_date:
            return Response({"error": "Дата заезда должна быть раньше даты выезда"}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем все категории номеров, которые соответствуют количеству людей
        available_rooms = Room.objects.filter(capacity__gte=people)

        # Исключаем уже забронированные номера на эти даты
        booked_rooms = Booking.objects.filter(
            check_in__lt=checkout_date, check_out__gt=checkin_date
        ).values_list("room_id", flat=True)

        available_rooms = available_rooms.exclude(id__in=booked_rooms)

        # Получаем цены для доступных категорий
        categories = (
            Price.objects.filter(category__in=available_rooms.values("category"))
            .values("category", "tour_price")
        )

        # Формируем ответ
        response_data = [
            {
                "category_name": self.CATEGORY_MAPPING.get(str(category["category"]), "Неизвестная категория"),
                "category_number": category["category"],
                "price": category["tour_price"]
            }
            for category in categories
        ]

        return Response(response_data, status=status.HTTP_200_OK)

