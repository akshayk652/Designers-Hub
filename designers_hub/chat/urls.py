# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('<username>/', views.chat, name='chat-room'),
    path('room/<room_name>/', views.room, name='room'),
]