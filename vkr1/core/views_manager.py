from django.db.models import Q, Count
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Place, Room, RoomPrice, Guest

class ManagerAvailableCategoriesAPIView(APIView):
    def get(self, request):
        checkin = request.GET.get("checkin")
        checkout = request.GET.get("checkout")
        gender = request.GET.get("gender")
        guests = int(request.GET.get("guests", 1))
        room_type = request.GET.get("room_type")

        # Проверка наличия обязательных параметров
        if not checkin or not checkout:
            return Response({"error": "Укажите checkin и checkout"}, status=status.HTTP_400_BAD_REQUEST)

        checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
        days = (checkout_date - checkin_date).days
        print(f"Количество дней: {days}")

        # 1. Получаем занятые места за указанный период
        booked_places = Booking.objects.filter(
            date__range=[checkin_date, checkout_date],
            status__in=["book", "prepay", "fullpay", "occupied"]
        ).values_list("place_id", flat=True).distinct()
        print(f"Занятые места: {booked_places}")

        # 2. Получаем список подходящих номеров (исключая занятые)
        available_places = Place.objects.exclude(id__in=booked_places).filter(
            room__capacity__gte=guests,  # Проверяем вместимость
            room__room_type=room_type,  # Проверяем тип удобств
        ).filter(
            Q(booking__gender=gender) | Q(booking__gender="undefined")  # Учитываем пол
        ).annotate(
            occupied_count=Count("booking",
                                 filter=Q(booking__status="free")
                                 )  # Подсчёт свободных мест
        # ).filter(
        #     occupied_count=0  # Только те, где нет занятых мест
        )

        if gender == "female":
            available_places = available_places.exclude(booking__gender="male")
        elif gender == "male":
            available_places = available_places.exclude(booking__gender="female")

        print(f"Пол: {gender}")
        print(f"Подходящие места: {available_places}")

        # 3. Группируем по категориям и считаем стоимость
        category_data = {}
        for place in available_places:
            category = place.room.category
            price_entry = RoomPrice.objects.filter(
                category=category,
                # date_begin__lte=checkin_date,
                # date_end__gte=checkout_date
            ).first()

            if price_entry:
                price = price_entry.tour_price * days  # Умножаем на количество дней

                if category not in category_data:
                    category_data[category] = {
                        "category": category,
                        "available_places": 0,
                        "price_per_stay": price
                    }

                category_data[category]["available_places"] += 1

        # Преобразуем данные в список, который будет возвращён в ответе
        response_data = [
            {
                "category": category,
                "available_places": data["available_places"],
                "price_per_stay": data["price_per_stay"]
            }
            for category, data in category_data.items()
        ]

        return Response(response_data, status=status.HTTP_200_OK)


class ManagerAvailablePlacesAPIView(APIView):
    def get(self, request):
        checkin = request.GET.get("checkin")
        checkout = request.GET.get("checkout")
        gender = request.GET.get("gender")
        guests = int(request.GET.get("guests", 1))
        category = request.GET.get("category")

        # Проверка наличия обязательных параметров
        if not checkin or not checkout:
            return Response({"error": "Укажите checkin и checkout"}, status=status.HTTP_400_BAD_REQUEST)

        checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
        days = (checkout_date - checkin_date).days
        print(f"Количество дней: {days}")

        # 1. Получаем занятые места за указанный период
        booked_places = Booking.objects.filter(
            date__range=[checkin_date, checkout_date],
            status__in=["book", "prepay", "fullpay", "occupied"]
        ).values_list("place_id", flat=True).distinct()
        print(f"Занятые места: {booked_places}")

        # 2. Получаем список подходящих номеров (исключая занятые)
        available_places = Place.objects.exclude(id__in=booked_places).filter(
            room__category=category,  # Проверяем category
        ).filter(
            Q(booking__gender=gender) | Q(booking__gender="undefined")  # Учитываем пол
        # ).annotate(
        #     occupied_count=Count("booking",
        #                          filter=Q(booking__status="free")
        #                          )  # Подсчёт свободных мест
        # ).filter(
        #     occupied_count=0  # Только те, где нет занятых мест
        )

        if gender == "female":
            available_places = available_places.exclude(booking__gender="male")
        elif gender == "male":
            available_places = available_places.exclude(booking__gender="female")

        # 3. Группируем по категориям и считаем стоимость
        category_data = {}
        places_data = {}
        i=0
        for place in available_places:
            category = place.room.category
            price_entry = RoomPrice.objects.filter(
                category=category,
                # date_begin__lte=checkin_date,
                # date_end__gte=checkout_date
            ).first()

            if price_entry:
                price = price_entry.tour_price * days  # Умножаем на количество дней

                if place.id not in places_data:
                    places_data[place.id] = {
                        "place_name": place.name,
                        "room_name": place.room.name,
                        "price": price
                    }
                    i+=1

        # Преобразуем данные в список, который будет возвращён в ответе
        response_data = [
            {
                "place_id": place_id,
                "place_name": data["place_name"],
                "room_name": data["room_name"],
                "price": data["price"]
            }
            for place_id, data in places_data.items()
        ]

        return Response(response_data, status=status.HTTP_200_OK)


class ManagerBookingNewAPIView(APIView):
    def post(self, request):
        data = request.data
        place_id = data["place_id"]

        place = Place.objects.get(id=place_id)

        checkin = datetime.strptime(data["checkin"], "%Y-%m-%d")
        checkout = datetime.strptime(data["checkout"], "%Y-%m-%d")
        surname=data["surname"]
        name=data["name"]
        patronymic = data.get("patronymic", None)
        birthday=data["birthday"]
        phone=data["phone"]
        email = data.get("email", None)
        gender=data["gender"]

        # Проверяем, свободно ли место
        # Получаем все бронирования для данного места с нужными статусами
        bookings = Booking.objects.filter(
            place_id=place_id,
            status__in=["book", "prepay", "fullpay", "occupied"],
            date__gt=checkin,
            date__lt=checkout
        )

        # Проверяем, есть ли такие записи
        is_booked = bookings.exists()

        if is_booked:
            return Response({"error": "Место уже занято"}, status=status.HTTP_400_BAD_REQUEST)

        guest, created = Guest.objects.get_or_create(
            surname=surname,
            name=name,
            patronymic=patronymic,
            gender=gender,
            birthday=birthday,
            phone=phone,
            email=email
        )

        current_date = checkin
        booking_ids = []
        while current_date < checkout:
            # Создание записи бронирования для каждой даты
            booking = Booking.objects.create(
                place=place,
                date=current_date,
                status="book",
                gender=gender,
                guest=guest
            )
            booking_ids.append(booking.id)
            current_date += timedelta(days=1)

        return Response(
            {"message": "Бронирование успешно создано", "booking_ids": booking_ids},
            status=status.HTTP_201_CREATED
        )


class ManagerBookingsAPIView(APIView):
    def get(self, request):
        category = request.query_params.get('category', None)
        surname = request.query_params.get('surname', None)
        checkin = request.query_params.get('checkin', None)

        if not checkin:
            checkin_date = datetime.now().strftime("%Y-%m-%d")
        else:
            checkin_date = datetime.strptime(checkin, "%Y-%m-%d")

        bookings = Booking.objects.all()
        bookings = bookings.filter(date__gte=checkin_date)

        if category:
            bookings = bookings.filter(place__category=category)

        if surname:
            bookings = bookings.filter(guest__surname__icontains=surname)



        # Преобразуем данные в список, который будет возвращён в ответе
        response_data = [
            {
                "place_id": place_id,
                "place_name": data["place_name"],
                "room_name": data["room_name"],
                "price": data["price"]
            }
            for place_id, data in places_data.items()
        ]

        return Response(response_data, status=status.HTTP_200_OK)