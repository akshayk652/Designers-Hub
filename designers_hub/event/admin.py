from django.contrib import admin
from .models import Event, Participants, Event_File, Event_Score

# Register your models here.
admin.site.register(Event)
admin.site.register(Participants)
admin.site.register(Event_File)
admin.site.register(Event_Score)