from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.create_event, name="create-event"),
    path("", views.events, name="events-list"),
    path("<int:id>", views.event, name="event"),
    path("rating/<int:id>/", views.rating, name="rating"),
    path("result/<int:id>", views.result, name="result")

]