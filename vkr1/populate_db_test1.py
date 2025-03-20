import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vkr1.settings')
django.setup()

from core.models import Room, Place, Guest, Booking, RoomPrice, BookingRecords, Categories


def create_test_data():
    # ----------CATEGORIES--------------------
    categories = []
    category = Categories.objects.create(
        name="1 - Двухкомнатный номер на 1 этаже в 4 корпусе с удобствами в номере",
        label="1cat",
    )
    categories.append(category)
    category = Categories.objects.create(
        name="2 - Двухместный номер на 1 этаже в 4 корпусе с удобствами в блоке",
        label="2cat",
    )
    categories.append(category)
    category = Categories.objects.create(
        name="3 - Двухместный номер на 1 этаже в 4 корпусе с удобствами в номере",
        label="3cat",
    )
    categories.append(category)
    category = Categories.objects.create(
        name="4 - Одноместный номер на 1 этаже в 4 корпусе с удобствами в номере",
        label="4cat",
    )
    categories.append(category)
    category = Categories.objects.create(
        name="5 - Двухместный номер на 2 этаже в 4 корпусе с удобствами в блоке",
        label="5cat",
    )
    categories.append(category)
    category = Categories.objects.create(
        name="6 - Двухместный номер на 1 этаже в 6 корпусе с удобствами в номере",
        label="6cat",
    )
    categories.append(category)
    category = Categories.objects.create(
        name="7 - Двухместный номер на 2 этаже в 6 корпусе с удобствами в номере",
        label="7cat",
    )
    categories.append(category)
    print(f"Добавлено {len(categories)} категорий!")

    # ----------ROOMS--------------------
    rooms = []
    room = Room.objects.create(
        name="Номер 101",
        floor="1floor",
        building="4building",
        capacity=2,
        category=categories[0],
        room_type="in_room"
    )
    rooms.append(room)
    room = Room.objects.create(
        name="Номер 102",
        floor="1floor",
        building="4building",
        capacity=2,
        category=categories[1],
        room_type="in_block"
    )
    rooms.append(room)
    room = Room.objects.create(
        name="Номер 103",
        floor="1floor",
        building="4building",
        capacity=2,
        category=categories[2],
        room_type="in_room"
    )
    rooms.append(room)
    room = Room.objects.create(
        name="Номер 104",
        floor="1floor",
        building="4building",
        capacity=1,
        category=categories[3],
        room_type="in_room"
    )
    rooms.append(room)
    room = Room.objects.create(
        name="Номер 205",
        floor="2floor",
        building="4building",
        capacity=2,
        category=categories[4],
        room_type="in_block"
    )
    rooms.append(room)
    room = Room.objects.create(
        name="Номер 106",
        floor="1floor",
        building="6building",
        capacity=2,
        category=categories[5],
        room_type="in_room"
    )
    rooms.append(room)
    room = Room.objects.create(
        name="Номер 207",
        floor="2floor",
        building="6building",
        capacity=2,
        category=categories[6],
        room_type="in_room"
    )
    rooms.append(room)
    print(f"Добавлены {len(rooms)} номеров!")

    # ----------PLACES--------------------
    places = []
    place = Place.objects.create(
        name="Место 101/1",
        room=rooms[0]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 101/2",
        room=rooms[0]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 102/1",
        room=rooms[1]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 102/2",
        room=rooms[1]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 103/1",
        room=rooms[2]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 103/2",
        room=rooms[2]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 104/1",
        room=rooms[3]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 105/1",
        room=rooms[4]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 105/2",
        room=rooms[4]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 106/1",
        room=rooms[5]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 106/2",
        room=rooms[5]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 107/1",
        room=rooms[6]
    )
    places.append(place)
    place = Place.objects.create(
        name="Место 107/2",
        room=rooms[6]
    )
    places.append(place)
    print(f"Добавлены {len(places)} мест!")

    # ----------GUESTS--------------------
    guests = []
    guest = Guest.objects.create(
        surname='Иванов',
        name='Иван',
        patronymic='Иванович',
        gender='male',
        birthday='1978-04-03',
        tour_type='usual',
        email=None,
        phone='89114404789',
        workplace=None,
        home_address_country=None,
        home_address_region=None,
        home_address_city=None,
        home_address_street_and_house=None
    )
    guests.append(guest)
    guest = Guest.objects.create(
        surname='Петров',
        name='Петр',
        patronymic='Петрович',
        gender='male',
        birthday='1967-09-15',
        tour_type='usual',
        email=None,
        phone='891783423499',
        workplace=None,
        home_address_country=None,
        home_address_region=None,
        home_address_city=None,
        home_address_street_and_house=None
    )
    guests.append(guest)
    guest = Guest.objects.create(
        surname='Сидоров',
        name='Сергей',
        patronymic='Алексеевич',
        gender='male',
        birthday='1961-06-23',
        tour_type='social',
        email=None,
        phone='891980756979',
        workplace=None,
        home_address_country=None,
        home_address_region=None,
        home_address_city=None,
        home_address_street_and_house=None
    )
    guests.append(guest)
    guest = Guest.objects.create(
        surname='Кротов',
        name='Анатолий',
        patronymic='Игоревич',
        gender='male',
        birthday='1983-12-08',
        tour_type='usual',
        email=None,
        phone='891882296729',
        workplace=None,
        home_address_country=None,
        home_address_region=None,
        home_address_city=None,
        home_address_street_and_house=None
    )
    guests.append(guest)
    guest = Guest.objects.create(
        surname='Коровьева',
        name='Елена',
        patronymic='Витальевна',
        gender='female',
        birthday='1992-04-18',
        tour_type='usual',
        email=None,
        phone='823983440789',
        workplace=None,
        home_address_country=None,
        home_address_region=None,
        home_address_city=None,
        home_address_street_and_house=None
    )
    guests.append(guest)
    guest = Guest.objects.create(
        surname='Семенова',
        name='Анна',
        patronymic='Сергеевна',
        gender='female',
        birthday='1970-11-14',
        tour_type='usual',
        email=None,
        phone='895523446779',
        workplace=None,
        home_address_country=None,
        home_address_region=None,
        home_address_city=None,
        home_address_street_and_house=None
    )
    guests.append(guest)
    guest = Guest.objects.create(
        surname='Старушкова',
        name='Елена',
        patronymic='Георгиевна',
        gender='female',
        birthday='1981-08-01',
        tour_type='social',
        email=None,
        phone='899876432789',
        workplace=None,
        home_address_country=None,
        home_address_region=None,
        home_address_city=None,
        home_address_street_and_house=None
    )
    guests.append(guest)
    print(f"Добавлены {len(guests)} гостей!")

    # ----------PRICES--------------------
    prices = []
    price = RoomPrice.objects.create(
        category=categories[0],
        tour_price=10100,
        hotel_price=11100,
        date_begin='2025-01-01',
        date_end='2025-12-31'
    )
    prices.append(price)
    price = RoomPrice.objects.create(
        category=categories[1],
        tour_price=10200,
        hotel_price=11200,
        date_begin='2025-01-01',
        date_end='2025-12-31'
    )
    prices.append(price)
    price = RoomPrice.objects.create(
        category=categories[2],
        tour_price=10300,
        hotel_price=11300,
        date_begin='2025-01-01',
        date_end='2025-12-31'
    )
    prices.append(price)
    price = RoomPrice.objects.create(
        category=categories[3],
        tour_price=10400,
        hotel_price=11400,
        date_begin='2025-01-01',
        date_end='2025-12-31'
    )
    prices.append(price)
    price = RoomPrice.objects.create(
        category=categories[4],
        tour_price=10500,
        hotel_price=11500,
        date_begin='2025-01-01',
        date_end='2025-12-31'
    )
    prices.append(price)
    price = RoomPrice.objects.create(
        category=categories[5],
        tour_price=10600,
        hotel_price=11600,
        date_begin='2025-01-01',
        date_end='2025-12-31'
    )
    prices.append(price)
    price = RoomPrice.objects.create(
        category=categories[6],
        tour_price=10700,
        hotel_price=11700,
        date_begin='2025-01-01',
        date_end='2025-12-31'
    )
    prices.append(price)
    print(f"Добавлены {len(prices)} цен!")

    # ----------RECORDS--------------------
    records = []
    record = BookingRecords.objects.create(
        guest=guests[0],
        tour_type='usual',
        checkin='2025-05-01',
        checkout='2025-05-09',
        place=places[0],
        status="book",
        total_price=None,
        prepayment_percent=None,
        prepayment_money=None,
    )
    records.append(record)
    record = BookingRecords.objects.create(
        guest=guests[1],
        tour_type='usual',
        checkin='2025-05-01',
        checkout='2025-05-07',
        place=places[1],
        status="prepay",
        total_price=None,
        prepayment_percent=None,
        prepayment_money=None,
    )
    records.append(record)
    record = BookingRecords.objects.create(
        guest=guests[2],
        tour_type='social',
        checkin='2025-05-04',
        checkout='2025-05-11',
        place=places[4],
        status="fullpay",
        total_price=None,
        prepayment_percent=None,
        prepayment_money=None,
    )
    records.append(record)
    record = BookingRecords.objects.create(
        guest=guests[3],
        tour_type='usual',
        checkin='2025-05-02',
        checkout='2025-05-14',
        place=places[6],
        status="book",
        total_price=None,
        prepayment_percent=None,
        prepayment_money=None,
    )
    records.append(record)
    record = BookingRecords.objects.create(
        guest=guests[4],
        tour_type='usual',
        checkin='2025-05-07',
        checkout='2025-05-12',
        place=places[7],
        status="prepay",
        total_price=None,
        prepayment_percent=None,
        prepayment_money=None,
    )
    records.append(record)
    record = BookingRecords.objects.create(
        guest=guests[5],
        tour_type='usual',
        checkin='2025-05-02',
        checkout='2025-05-09',
        place=places[8],
        status="book",
        total_price=None,
        prepayment_percent=None,
        prepayment_money=None,
    )
    records.append(record)
    record = BookingRecords.objects.create(
        guest=guests[6],
        tour_type='social',
        checkin='2025-05-10',
        checkout='2025-05-15',
        place=places[2],
        status="book",
        total_price=None,
        prepayment_percent=None,
        prepayment_money=None,
    )
    records.append(record)
    print(f"Добавлены {len(records)} записей!")

    # ----------BOOKINGS--------------------
    booking_matrix = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 0],
        [0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    bookings = []
    for i in range(13):
        for j in range(15):
            if (booking_matrix[i][j] == 0):
                booking = Booking.objects.create(
                    place=places[i],
                    date=f"2025-05-{j + 1}"
                )
            elif (booking_matrix[i][j] == 1):
                booking = Booking.objects.create(
                    place=places[i],
                    date=f"2025-05-{j + 1}",
                    guest=guests[0],
                    status="book",
                    gender='male',
                    record=records[0]
                )
            elif (booking_matrix[i][j] == 2):
                booking = Booking.objects.create(
                    place=places[i],
                    date=f"2025-05-{j + 1}",
                    guest=guests[1],
                    status="prepay",
                    gender='male',
                    record=records[1]
                )
            elif (booking_matrix[i][j] == 3):
                booking = Booking.objects.create(
                    place=places[i],
                    date=f"2025-05-{j + 1}",
                    guest=guests[2],
                    status="book",
                    gender='male',
                    record=records[2]
                )
            elif (booking_matrix[i][j] == 4):
                booking = Booking.objects.create(
                    place=places[i],
                    date=f"2025-05-{j + 1}",
                    status="fullpay",
                    guest=guests[3],
                    gender='male',
                    record=records[3]
                )
            elif (booking_matrix[i][j] == 5):
                booking = Booking.objects.create(
                    place=places[i],
                    date=f"2025-05-{j + 1}",
                    status="prepay",
                    guest=guests[4],
                    gender='female',
                    record=records[4]
                )
            elif (booking_matrix[i][j] == 6):
                booking = Booking.objects.create(
                    place=places[i],
                    date=f"2025-05-{j + 1}",
                    status="book",
                    guest=guests[5],
                    gender='female',
                    record=records[5]
                )
            elif (booking_matrix[i][j] == 7):
                booking = Booking.objects.create(
                    place=places[i],
                    date=f"2025-05-{j + 1}",
                    status="book",
                    guest=guests[6],
                    gender='female',
                    record=records[6]
                )
            else:
                booking = Booking.objects.create(
                    place=places[i],
                    date=f"2025-05-{j + 1}"
                )

            bookings.append(booking)
    print(f"Добавлены {len(bookings)} дней брони!")


if __name__ == '__main__':
    create_test_data()
    print()
    print("Данные успешно добавлены!")
