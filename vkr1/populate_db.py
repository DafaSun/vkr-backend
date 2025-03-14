import os
import django
from django.utils.timezone import now
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vkr1.settings')
django.setup()

from core.models import Room, Price, Person, Guest, Booking, Occupancy


def create_test_data():
    rooms = []
    for i in range(20):
        room = Room.objects.create(
            name=f"Номер{i+100}",
            floor=(i % 2) + 1,
            building=(i % 3) + 4,
            capacity=(i % 2) + 1,
            category=(i % 7) + 1,
            room_type=(i % 2) + 1,
        )
        rooms.append(room)

    prices = []
    for i in range(20):
        price = Price.objects.create(
            category=(i % 7) + 1,
            tour_price=((i % 3) + 1) * 2000,
            hotel_price=((i % 3) + 1) * 3000,
        )
        prices.append(price)

    persons = []
    for i in range(20):
        person = Person.objects.create(
            name=f"{(i % 7) + 1}",
            surname=f"{((i % 3) + 1) * 2000}",
            patronymic=f"{((i % 3) + 1) * 3000}",
            birthday="1983-05-12",
        )
        persons.append(person)

    guests = []
    for i in range(20):
        guest = Guest.objects.create(
            person=random.choice(persons),
            tour_type=(i % 3) + 1,
            age=i + 20,
            gender=(i % 2) + 1,
            room=random.choice(rooms),
            building=(i % 3) + 3,
            email=f"mail{i}mail@mail.ru",
            phone="12345678904582",
            home_address_country="Russia",
            home_address_region="Moscow",
            home_address_city="Moscow",
            home_address_street_and_house="Gagarin street, 78, 6",
        )
        guests.append(guest)

    bookings = []
    for i in range(20):
        booking = Booking.objects.create(
            person=random.choice(persons),
            gender=f"{(i % 2) + 1}",
            room=random.choice(rooms),
            place=f"{(i % 2) + 1}",
            check_in="2025-04-09",
            check_out="2025-04-28",
            status=f"{(i % 4) + 1}",
            total_price=f"{(i % 4) + 1}",
            has_breakfast=True,
            has_lunch=True,
            has_dinner=False,
            tour_type=(i%3)+1,
            prepayment_percent=50,
            prepayment_money=34000
        )
        bookings.append(booking)

    occupancies=[]
    for i in range(20):
        occupancy = Occupancy.objects.create(
            room=random.choice(rooms),
            booking=random.choice(bookings),
            date="2025-04-15",
            status=f"{(i % 4) + 1}",
            gender=f"{(i % 5) + 1}"
        )
        occupancies.append(occupancy)


if __name__ == '__main__':
    create_test_data()
    print("Данные успешно добавлены!")
