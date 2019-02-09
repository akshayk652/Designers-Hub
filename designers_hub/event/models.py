from django.db import models

from user_profile.models import Designer, User

# Create your models here.

class Event(models.Model):
    creator         = models.ForeignKey(User, on_delete=models.CASCADE) 
    name            = models.CharField(max_length=20)
    description     = models.TextField()
    topic           = models.CharField(max_length=20)
    points          = models.IntegerField(default=100)
    date_created    = models.DateField(auto_now_add=True, auto_now=False)
    status          = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name


class Participants(models.Model):
    participants    = models.ForeignKey(User, on_delete=models.CASCADE)
    event           = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.event

class Event_File(models.Model):
    participant     = models.ForeignKey(User, on_delete=models.CASCADE)
    img_file        = models.FileField(upload_to="event_file/", verbose_name="Attach file")

class Event_Score(models.Model):
    participant     = models.ForeignKey(User, on_delete=models.CASCADE)
    score           = models.IntegerField(default=0) 