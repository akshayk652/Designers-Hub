from .models import Skill, Project

def all_skills(request):
    context = {
        'skills':Skill.objects.all(),
        'projects': Project.objects.all(),
    }
    return context

