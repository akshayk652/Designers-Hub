from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Sum, Max

from .models import Event, Event_File, Event_Score
from .forms import Event_Form
from user_profile.models import Designer, User

User = get_user_model()

def create_event(request):
    form = Event_Form(request.POST or None)
    template_name = 'event/create.html'
    if request.method == "POST":
        if form.is_valid():
            event = Event()
            designer = User.objects.get(username=request.user.username)
            event.creator = designer
            event.name = form.cleaned_data["name"]
            event.description = form.cleaned_data["description"]
            event.topic = form.cleaned_data["topic"]
            event.points = form.cleaned_data["points"]
            event.save()
            return redirect("events-list")
    return render(request, template_name, {'form':form})

def events(request):
    template_name = "event/events.html"
    events = Event.objects.exclude(status=False)
    context = {
        "events": events
    }
    return render(request, template_name, context)

def event(request, id):
    event = Event.objects.get(pk=id)
    if request.method == "POST":
        event_file = Event_File()
        event_file.participant = request.user
        event_file.img_file = request.FILES.get("myfile")
        event_file.save()
        return render(request, "event/rating-wait.html", {"id":id})
    context = {
        "event": event
    }
    return render(request, "event/contest.html", context)


def rating(request, id):
    template_name = "event/ratings.html"
    if request.method == "POST":
        event_imgs = Event_File.objects.all()
        for event_img in event_imgs:
            if event_img.participant == request.user:
                continue
            file_user = event_img.participant 
     
            print("+++++++++++++++++++++++++++++++++++++++++")     
            event_score = Event_Score()
            event_score.participant = file_user
            event_score.score = request.POST[file_user.username]
            event_score.save()
        return redirect('result', id=id)
    event_imgs = Event_File.objects.exclude(participant = request.user)
    context = {
        "event_imgs": event_imgs
    }
    return render(request,template_name,context)


def result(request, id):
    if request.method == "POST":
        result = Event_Score.objects.values('participant').annotate(scores=Sum('score')).order_by('-scores')
        winner_id = result[0]['participant']
        winner_score = result[0]['scores']
        winner = User.objects.get(id=winner_id)
        designer = Designer.objects.get(user=winner)
        points = designer.points
        designer.points = points + Event.objects.get(id=id).points

        winner_img = Event_File.objects.filter(participant=winner).first()
        context = {
            "winner_name":  winner.username,
            "winner_score": winner_score,
            "winner_img": winner_img.img_file
        }
        print(winner.username, winner_score)
        event = Event.objects.get(id=id)
        event.status = False
        event.save()
        return render(request, "event/result.html", context)
    template_name = "event/result-waiting.html"
    return render(request, template_name, {})

