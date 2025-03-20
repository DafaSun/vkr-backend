from django.db.models import Q, Count
from django.db import transaction
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Booking, Place, Room, RoomPrice, Guest, BookingRecords, NutritionPrice, Categories


class ManagerAvailableCategoriesAPIView(APIView):
    def get(self, request):
        checkin = request.GET.get("checkin")
        checkout = request.GET.get("checkout")
        gender = request.GET.get("gender")
        guests = int(request.GET.get("guests", 1))
        room_type = request.GET.get("room_type")
        tour_type = request.GET.get("tour_type")

        if not checkin or not checkout:
            return Response({"error": "Укажите checkin и checkout"}, status=status.HTTP_400_BAD_REQUEST)

        checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
        days = (checkout_date - checkin_date).days

        booked_places = Booking.objects.filter(
            date__range=[checkin_date, checkout_date],
            status__in=["book", "prepay", "fullpay", "occupied"]
        ).values_list("place_id", flat=True).distinct()

        available_places = Place.objects.exclude(id__in=booked_places).filter(
            room__capacity__gte=guests,
            room__room_type=room_type,
        ).filter(
            Q(booking__gender=gender) | Q(booking__gender="undefined")
        ).annotate(
            occupied_count=Count("booking",
                                 filter=Q(booking__status="free")
                                 )
            # ).filter(
            #     occupied_count=0  # Только те, где нет занятых мест
        )

        if gender == "female":
            available_places = available_places.exclude(booking__gender="male")
        elif gender == "male":
            available_places = available_places.exclude(booking__gender="female")

        category_data = {}
        for place in available_places:
            category = place.room.category
            price_entry = RoomPrice.objects.filter(
                category=category,
                # date_begin__lte=checkin_date,
                # date_end__gte=checkout_date
            ).first()

            if price_entry:
                price = price_entry.tour_price * days

                if category not in category_data:
                    category_data[category.id] = {
                        "category_id": category.id,
                        "category_label": category.label,
                        "category_name": category.name,
                        "available_places": 0,
                        "price": price
                    }

                category_data[category.id]["available_places"] += 1

        response_data = [
            {
                "category_label": data["category_label"],
                "category_name": data["category_name"],
                "available_places": data["available_places"],
                "price": data["price"]
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
        category_label = request.GET.get("category")
        category = Categories.objects.get(label=category_label)
        tour_type = request.GET.get("tour_type")

        if not checkin or not checkout:
            return Response({"error": "Укажите checkin и checkout"}, status=status.HTTP_400_BAD_REQUEST)

        checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
        days = (checkout_date - checkin_date).days

        booked_places = Booking.objects.filter(
            date__range=[checkin_date, checkout_date],
            status__in=["book", "prepay", "fullpay", "occupied"]
        ).values_list("place_id", flat=True).distinct()

        available_places = Place.objects.exclude(id__in=booked_places).filter(
            room__category=category,  # Проверяем category
        ).filter(
            Q(booking__gender=gender) | Q(booking__gender="undefined")  # Учитываем пол
            # ).annotate(
            #     occupied_count=Count("booking",
            #                          filter=Q(booking__status="free")
            #                          )
            # ).filter(
            #     occupied_count=0
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
                price = price_entry.tour_price * days

                if place.id not in places_data:
                    places_data[place.id] = {
                        "category_name": place.room.category.name,
                        "place_name": place.name,
                        "room_name": place.room.name,
                        "price": price
                    }
                    i += 1

        response_data = [
            {
                "place_id": place_id,
                "place_name": data["place_name"],
                "room_name": data["room_name"],
                "price": data["price"],
                "category_name": data["category_name"],
            }
            for place_id, data in places_data.items()
        ]

        return Response(response_data, status=status.HTTP_200_OK)


class ManagerBookingNewAPIView(APIView):
    def post(self, request):
        data = request.data
        place_id = data["place_id"]

        place = Place.objects.get(id=place_id)

        checkin = datetime.strptime(data["checkin"], "%Y-%m-%d").date()
        checkout = datetime.strptime(data["checkout"], "%Y-%m-%d").date()
        surname = data["surname"]
        name = data["name"]
        patronymic = data.get("patronymic", None)
        birthday = data["birthday"]
        phone = data["phone"]
        email = data.get("email", None)
        gender = data["gender"]
        tour_type = data["tour_type"]
        breakfast = data.get("breakfast", False)
        lunch = data.get("lunch", False)
        dinner = data.get("dinner", False)
        price = data.get("price", 10000)

        bookings = Booking.objects.filter(
            place_id=place_id,
            status__in=["book", "prepay", "fullpay", "occupied"],
            date__gt=checkin,
            date__lt=checkout
        )

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
            email=email,
            tour_type=tour_type,
        )

        days = (checkout - checkin).days
        # price = RoomPrice.objects.get(category=place.room.category)
        # total_price = 800
        # if tour_type == "usual":
        #     total_price = days * price.tour_price
        # elif tour_type == "hotel":
        #     total_price = days * price.hotel_price
        #
        #     breakfast_price = NutritionPrice.objects.get(nutrition='breakfast').price
        #     lunch_price = NutritionPrice.objects.get(nutrition='breakfast').price
        #     dinner_price = NutritionPrice.objects.get(nutrition='dinner').price
        #
        #     if breakfast:
        #         total_price += days * breakfast_price
        #     if lunch:
        #         total_price += days * lunch_price
        #     if dinner:
        #         total_price += days * dinner_price

        record = BookingRecords.objects.create(
            guest=guest,
            checkin=checkin,
            checkout=checkout,
            place=place,
            status="book",
            total_price=price,
            prepayment_percent=None,
            prepayment_money=None,
            hasBreakfast=breakfast,
            hasLunch=lunch,
            hasDinner=dinner,
            tour_type=tour_type,
        )

        current_date = checkin
        booking_ids = []
        while current_date < checkout:
            booking_for_delete = Booking.objects.filter(
                place=place,
                status='free',
                date=current_date,)
            booking_for_delete.delete()

            booking = Booking.objects.create(
                place=place,
                date=current_date,
                gender=gender,
                guest=guest,
                status='book',
                record=record,
            )
            booking_ids.append(booking.id)
            current_date += timedelta(days=1)

        return Response(
            {"message": "Бронирование успешно создано", "record_id": record.id},
            status=status.HTTP_201_CREATED
        )


class ManagerBookingsAPIView(APIView):
    def get(self, request):
        category_label = request.query_params.get('category', None)
        surname = request.query_params.get('surname', None)
        checkin = request.query_params.get('checkin', None)

        records = BookingRecords.objects.all()

        if checkin:
            checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
            records = records.filter(checkin=checkin_date)

        if category_label:
            category = Categories.objects.get(label=category_label)
            records = records.filter(place__room__category=category)

        if surname:
            records = records.filter(guest__surname__icontains=surname)

        records_list = [
            {
                "booking_id": record.id,
                "surname": record.guest.surname if record.guest else None,
                "name": record.guest.name if record.guest else None,
                "patronymic": record.guest.patronymic if record.guest else None,
                "room_name": record.place.room.name if record.place else None,
                "place_name": record.place.name if record.place else None,
                "place_id": record.place.id if record.place else None,
                "checkin_date": record.checkin.strftime("%Y-%m-%d"),
                "category_label": record.place.room.category.label,
                "category_name": record.place.room.category.name,
            }
            for record in records
        ]

        return Response(records_list, status=status.HTTP_200_OK)

class ManagerBookingPlaceNameAPIView(APIView):
    def get(self, request):
        place_id = request.query_params.get('place_id')

        place = Place.objects.get(id=place_id)

        response =  {
                "place_id": place.id,
                "place_name": place.name,
            }

        return Response(response, status=status.HTTP_200_OK)


class ManagerBookingsRecordGetAPIView(APIView):
    def get(self, request):
        record_id = request.GET.get("id")

        if not id:
            return Response({"error": "Укажите id"}, status=status.HTTP_400_BAD_REQUEST)

        record = BookingRecords.objects.get(
            id=record_id
        )

        response_data = {
            "guest_surname": record.guest.surname if record.guest else None,
            "guest_name": record.guest.name if record.guest else None,
            "guest_patronymic": record.guest.patronymic if record.guest else None,
            "checkin": record.checkin.strftime("%Y-%m-%d"),
            "checkout": record.checkout.strftime("%Y-%m-%d"),
            "room_name": record.place.room.name if record.place else None,
            "category_label": record.place.room.category.label,
            "category_name": record.place.room.category.name,
            "place_name": record.place.name if record.place else None,
            "status": record.status,
            "total_price": record.total_price,
            "prepayment_percent": record.prepayment_percent,
            "prepayment_money": record.prepayment_money,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ManagerBookingsRecordDeleteAPIView(APIView):
    def delete(self, request):
        record_id = request.GET.get("id")

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
        category_label = request.query_params.get('category', None)
        building = request.query_params.get('building', None)
        date0 = request.query_params.get('date', None)

        if not date0:
            start_date = datetime.now().date()
        else:
            start_date = datetime.strptime(date0, "%Y-%m-%d").date()

        end_date = start_date + timedelta(days=30)
        date_range = [(start_date + timedelta(days=i)).isoformat() for i in range(31)]

        places = Place.objects.all().order_by("id")

        if category_label:
            category = Categories.objects.get(label=category_label)
            places = places.filter(room__category=category)

        if building:
            places = places.filter(room__building=building)

        bookings = Booking.objects.filter(date__range=[start_date, end_date])

        data = {
            "places": [place.name for place in places],
            "dates": date_range,
            "bookings": {place.name: {} for place in places}
        }

        for booking in bookings:
            if booking.place.name not in data["bookings"]:
                data["bookings"][booking.place.name] = {}

            data["bookings"][booking.place.name][booking.date.isoformat()] = booking.status

        for place in data["places"]:
            for d in date_range:
                data["bookings"][place].setdefault(d, "free")

        return Response(data)


class ManagerGuestsAPIView(APIView):
    def get(self, request):
        surname = request.query_params.get('surname', None)

        guests = Guest.objects.all()

        if surname:
            guests = guests.filter(surname__icontains=surname)

        response_data = [
            {
                "guest_id": guest.id,
                "surname": guest.surname,
                "name": guest.name,
                "patronymic": guest.patronymic,
                "birthday": guest.birthday,
                "tour_type": guest.tour_type
            }
            for guest in guests
        ]

        return Response(response_data, status=status.HTTP_200_OK)


class ManagerGuestsGetPersonAPIView(APIView):
    def get(self, request):
        guest_id = request.GET.get("id")

        if not guest_id:
            return Response({"error": "Укажите id"}, status=status.HTTP_400_BAD_REQUEST)

        guest = Guest.objects.get(id=guest_id)
        record = BookingRecords.objects.filter(guest=guest).first()

        response_data = {
            "guest_id": guest.id,
            "surname": guest.surname,
            "name": guest.name,
            "patronymic": guest.patronymic,
            "birthday": guest.birthday,
            "gender": guest.gender,
            "tour_type": guest.tour_type,
            "email": guest.email,
            "phone": guest.phone,
            "home_address_country": guest.home_address_country,
            "home_address_region": guest.home_address_region,
            "home_address_city": guest.home_address_city,
            "home_address_street_and_house": guest.home_address_street_and_house,
            "workplace": guest.workplace,
            "place_name": record.place.name,
            "room_name": record.place.room.name,
            "checkin": record.checkin,
            "checkout": record.checkout,
            "category_label": record.place.room.category.label,
            "category_name": record.place.room.category.name,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ManagerGuestsNewPersonAPIView(APIView):
    def post(self, request):
        data = request.data
        surname = data["surname"]
        name = data["name"]
        patronymic = data.get("patronymic", None)
        gender = data.get("gender")
        birthday = data["birthday"]
        phone = data["phone"]
        email = data.get("email", None)
        home_address_country = data.get("home_address_country", None)
        home_address_region = data.get("home_address_region", None)
        home_address_city = data.get("home_address_city", None)
        home_address_street_and_house = data.get("home_address_street_and_house", None)
        workplace = data.get("workplace", None)

        guest, created = Guest.objects.get_or_create(
            surname=surname,
            name=name,
            patronymic=patronymic,
            gender=gender,
            birthday=birthday,
            phone=phone,
            email=email,
            home_address_country=home_address_country,
            home_address_region=home_address_region,
            home_address_city=home_address_city,
            home_address_street_and_house=home_address_street_and_house,
            workplace=workplace
        )

        return Response(
            {"message": "Гость успешно создан", "guest_id": guest.id},
            status=status.HTTP_201_CREATED
        )


class ManagerGuestsEditPersonAPIView(APIView):
    def patch(self, request):
        guest_id = request.GET.get("id")
        guest = Guest.objects.get(id=guest_id)
        print('______________________________________')
        print('______________________________________')
        print('______________________________________')
        print('______________________________________')
        print(guest_id)
        print('______________________________________')
        print('______________________________________')
        print('______________________________________')
        print('______________________________________')

        surname = request.data.get("surname", guest.surname)
        name = request.data.get("name", guest.name)
        patronymic = request.data.get("patronymic", guest.patronymic)
        gender = request.data.get("gender", guest.gender)
        birthday = request.data.get("birthday", guest.birthday)
        phone = request.data.get("phone", guest.phone)
        email = request.data.get("email", guest.email)
        home_address_country = request.data.get("home_address_country", guest.home_address_country)
        home_address_region = request.data.get("home_address_region", guest.home_address_region)
        home_address_city = request.data.get("home_address_city", guest.home_address_city)
        home_address_street_and_house = request.data.get("home_address_street_and_house",
                                                         guest.home_address_street_and_house)
        workplace = request.data.get("workplace", guest.workplace)

        guest.surname = surname
        guest.name = name
        guest.patronymic = patronymic
        guest.gender = gender
        guest.birthday = birthday
        guest.phone = phone
        guest.email = email
        guest.home_address_country = home_address_country
        guest.home_address_region = home_address_region
        guest.home_address_city = home_address_city
        guest.home_address_street_and_house = home_address_street_and_house
        guest.workplace = workplace

        guest.save()

        return Response({
            "id": guest.id,
            "name": guest.name,
            "surname": guest.surname,
            "patronymic": guest.patronymic,
        }, status=status.HTTP_200_OK)


class ManagerGuestsDeletePersonAPIView(APIView):
    def delete(self, request):
        guest_id = request.GET.get("id")

        if not id:
            return Response({"error": "Укажите id"}, status=status.HTTP_400_BAD_REQUEST)

        guest = Guest.objects.get(id=guest_id)
        guest.delete()

        return Response({"message": "Booking record deleted and bookings updated successfully"},
                            status=status.HTTP_204_NO_CONTENT)


