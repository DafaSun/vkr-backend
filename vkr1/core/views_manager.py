from django.db.models import Q, Count
from django.db import transaction
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Booking, Place, Room, RoomPrice, Guest, BookingRecords


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

        # 1. Получаем занятые места за указанный период
        booked_places = Booking.objects.filter(
            date__range=[checkin_date, checkout_date],
            status__in=["book", "prepay", "fullpay", "occupied"]
        ).values_list("place_id", flat=True).distinct()

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

        # 1. Получаем занятые места за указанный период
        booked_places = Booking.objects.filter(
            date__range=[checkin_date, checkout_date],
            status__in=["book", "prepay", "fullpay", "occupied"]
        ).values_list("place_id", flat=True).distinct()

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

        places_data = {}
        i = 0
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
                    i += 1

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
        surname = data["surname"]
        name = data["name"]
        patronymic = data.get("patronymic", None)
        birthday = data["birthday"]
        phone = data["phone"]
        email = data.get("email", None)
        gender = data["gender"]

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
                gender=gender,
                guest=guest
            )
            booking_ids.append(booking.id)
            current_date += timedelta(days=1)
        record = BookingRecords.objects.create(
            guest=guest,
            checkin=checkin,
            checkout=checkout,
            place=place,
            status="book",
            total_price=None,
            prepayment_percent=None,
            prepayment_money=None
        )

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

        records = BookingRecords.objects.all()
        records = records.filter(checkin=checkin_date)

        if category:
            records = records.filter(place__room__category=category)

        if surname:
            records = records.filter(guest__surname__icontains=surname)

        records_list = [
            {
                "surname": record.guest.surname if record.guest else None,
                "name": record.guest.name if record.guest else None,
                "patronymic": record.guest.patronymic if record.guest else None,
                "room_name": record.place.room.name if record.place else None,
                "place_name": record.place.name if record.place else None,
                "place_id": record.place.id if record.place else None,
                "checkin_date": record.checkin.strftime("%Y-%m-%d"),
                "category": record.place.room.category,
            }
            for record in records
        ]

        return Response(records_list, status=status.HTTP_200_OK)


class ManagerBookingsRecordGetAPIView(APIView):
    def get(self, request):
        record_id = request.GET.get("id")

        # Проверка наличия обязательных параметров
        if not id:
            return Response({"error": "Укажите id"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Получаем занятые места за указанный период
        record = BookingRecords.objects.filter(
            id=record_id
        ).first()

        # Преобразуем данные в список, который будет возвращён в ответе
        response_data = {
            "guest_surname": record.guest.surname if record.guest else None,
            "guest_name": record.guest.name if record.guest else None,
            "guest_patronymic": record.guest.patronymic if record.guest else None,
            "checkin": record.checkin.strftime("%Y-%m-%d"),
            "checkout" : record.checkout.strftime("%Y-%m-%d"),
            "room_name": record.place.room.name if record.place else None,
            "category": record.place.room.category,
            "place_name" : record.place.name if record.place else None,
            "status" : record.status,
            "total_price" : record.total_price,
            "prepayment_percent" : record.prepayment_percent,
            "prepayment_money": record.prepayment_money,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ManagerBookingsRecordDeleteAPIView(APIView):
    def delete(self, request):
        record_id = request.GET.get("id")

        # Проверка наличия обязательных параметров
        if not id:
            return Response({"error": "Укажите id"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            record_to_delete = get_object_or_404(BookingRecords, id=record_id)

            bookings_to_update = Booking.objects.filter(record=record_to_delete)

            bookings_to_update.update(
                guest=None,
                status='free',
                record=None
            )

            record_to_delete.delete()

            # Возвращаем успешный ответ
            return Response({"message": "Booking record deleted and bookings updated successfully"},
                            status=status.HTTP_204_NO_CONTENT)

class ManagerBookingsRecordUpdateAPIView(APIView):
    def patch(self, request):
        record_id = request.GET.get("id")
        record = BookingRecords.objects.get(id=record_id)
        status0 = request.data.get('status', record.status)
        prepayment_percent = request.data.get('prepayment_percent', record.prepayment_percent)
        prepayment_money = request.data.get('prepayment_money', record.prepayment_money)

        record_to_delete = get_object_or_404(BookingRecords, id=record_id)
        bookings_to_update = Booking.objects.filter(record=record_to_delete)
        bookings_to_update.update(
            status=status0,
        )

        record.status = status0
        record.prepayment_percent = prepayment_percent
        record.prepayment_money = prepayment_money

        record.save()
        return Response({
            "id": record.id,
            "status": record.status,
            "prepayment_percent": record.prepayment_percent,
            "prepayment_money": record.prepayment_money
        }, status=status.HTTP_200_OK)

class ManagerRoomsTableAPIView(APIView):
    def get(self, request):
        category = request.query_params.get('category', None)
        building = request.query_params.get('building', None)
        date0 = request.query_params.get('date', None)

        if not date0:
            start_date = datetime.now().date()
        else:
            start_date = datetime.strptime(date0, "%Y-%m-%d").date()

        end_date = start_date + timedelta(days=30)
        date_range = [(start_date + timedelta(days=i)).isoformat() for i in range(31)]

        places = Place.objects.all().order_by("id")

        if category:
            places = places.filter(room__category=category)

        if building:
            places = places.filter(room__building=category)

        bookings = Booking.objects.filter(date__range=[start_date, end_date])

        data = {
            "places": [place.name for place in places],
            "dates": date_range,
            "bookings": {place.name: {} for place in places}
        }

        for booking in bookings:
            data["bookings"][booking.place.name][booking.date.isoformat()] = booking.status

        for place in data["places"]:
            for d in date_range:
                data["bookings"][place].setdefault(d, "free")

        return Response(data)