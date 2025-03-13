from django.contrib import admin
from .models import Room, Price, Person, Guest, Booking, Occupancy

admin.site.register(Room)
admin.site.register(Price)
admin.site.register(Person)
admin.site.register(Guest)
admin.site.register(Booking)
admin.site.register(Occupancy)