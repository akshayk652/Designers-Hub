import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.http import HttpResponse

from contract.views import email

@login_required
def index(request):
    return render(request, 'chat/index.html', {})


@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


@login_required
def chat(request, username):
    if request.method == "POST":
        print('++++++++++++++++++',username)
        url = username
        subject = "Chat url"
        message = "http://localhost:8000/chats/room/{0}/".format(username)
        #    send info to email and returns none
        email(request,subject,message,type="chat")
        print(message)
        return redirect('room', room_name=username)