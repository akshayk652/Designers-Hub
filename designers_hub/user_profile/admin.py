from django.contrib import admin
from .models import User, Skill, Designer, Project

# Register your models here.
admin.site.register(User)
admin.site.register(Skill)
admin.site.register(Designer)
admin.site.register(Project)
