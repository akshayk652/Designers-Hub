from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_designer     = models.BooleanField(default=False)
    is_client       = models.BooleanField(default=False)
    description     = models.TextField(max_length=500, blank=True)    
    date_created    = models.DateField(auto_now_add=True)
    profile_img     = models.ImageField(upload_to="gallery",null=True, blank=True)


class Skill(models.Model):
    skill = models.CharField(max_length=50)

    def __str__(self):
        return self.skill


class Designer(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)    
    skills          = models.ManyToManyField(Skill, related_name='skills')
    experience      = models.IntegerField(blank=True, null=True)
    points          = models.IntegerField(default=0)     

    def __str__(self):
        return self.user.username



class Project(models.Model):
    designer        = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name='projects')    
    name            = models.CharField(max_length=100)
    description     = models.TextField(max_length=500, blank=True)
    image_file_path = models.ImageField(upload_to="gallery")
    date_created    = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name