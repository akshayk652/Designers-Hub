from django.shortcuts import render, get_object_or_404,redirect 
from django.forms.models import model_to_dict
from django.http import HttpResponse ,JsonResponse
from django.utils.translation import gettext as _
# from django.views.generic import DetailView
from .models import User, Designer, Skill, Project
# from .forms import ProjectForm, DesignerSettingsForm, UserSettingsForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.urls import reverse_lazy
from .decorators import designer_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.views.generic import CreateView, UpdateView, TemplateView, DetailView
from .forms import DesignerSignUpForm, ClientSignUpForm, DesignerSkillsForm, ProjectForm, DesignerSettingsForm, UserSettingsForm
from contract.views import get_rating
from contract.models import Contract


class SignUpView(TemplateView):
    template_name = 'user_profile/register.html'


def landing_page(request):
    return render(request, "user_profile/landing_page.html")


def home(request):
    user = request.user
    projects = Project.objects.all()
    skills = Skill.objects.all()  
    for project in projects:
        print(project.image_file_path)
    context = {
        'projects':projects,
        'skills':skills,   
        'user': user,
    }
    return render(request, "user_profile/home.html", context)


def search_data(request):
    query = request.GET.get('q')
    results = Project.objects.filter(Q(name__icontains=query))
    context = {
        'results':results
    }
    return render(request, "user_profile/search.html", context)


@login_required
def upload_portfolio(request, username):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():            
            project = form.save(commit=False)
            project.designer = request.user.designer
            project.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'user_profile/project_upload.html', {'form': form, 'username':username})
    

class DesignerSignUpView(CreateView):
    model = User
    form_class = DesignerSignUpForm
    template_name = 'user_profile/register_form.html'

    def get_context_data(self, **kwargs):
        """
        import pdb; pdb.set_trace()
        n -> next line
        s -> step into
        u -> step out
        p <variable_name>
        c -> continue
        """
        kwargs['user_type'] = 'designer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('login')

@method_decorator([login_required, designer_required], name='dispatch')
class DesignerSkillsView(UpdateView):
    model = Designer
    form_class = DesignerSkillsForm
    template_name = 'user_profile/skills_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.designer

    def form_valid(self, form):
        messages.success(self.request, 'Skills updated with success!')
        return super().form_valid(form)





class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'user_profile/register_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('login')




def designer_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    designer = get_object_or_404(Designer, user_id=profile_user.id)
    skills = designer.skills.all()
    projects = designer.projects.all()
    rating = get_rating(request, username)
    contract = Contract.objects.filter(designer=designer)
    count_contract = len(contract.filter(status="active"))
    context = {
        "user": request.user,
        "designer_user": profile_user,
        "designer": designer, 
        "skills": skills,
        "projects": projects,
        "username": username,
        "rating": rating,
        "count_contract": count_contract
    }
    return render(request, 'user_profile/designer_detail.html', context)


def client_profile(request, username):
    user = get_object_or_404(User, username=username)
    contract = Contract.objects.filter(client=user)
    count_contract = len(contract)
    present_user = request.user.username    
    context = {
        "client_user": user,         
        "username": username,
        "present_user": present_user,
        "count_contract": count_contract
    }
    return render(request, 'user_profile/client_detail.html', context)


def project_detail(request, username, pk):
    user = get_object_or_404(User, username=username)
    designer = get_object_or_404(Designer, user_id=user.id)
    project = designer.projects.get(pk=pk)
    context = {
        "designer_user": user,
        "designer": designer,
        "project": project
    }
    return render(request, 'user_profile/project_detail.html', context)


@login_required
def update_profile(request, username):
    if request.method == 'POST':
        if request.user.is_designer:     
            user_form = UserSettingsForm(request.POST, request.FILES or None, instance=request.user)
            profile_form = DesignerSettingsForm(request.POST, instance=request.user.designer)
            if user_form.is_valid() and profile_form.is_valid():       
                user_form.save()     
                profile_form.save()
                messages.success(request, _('Your profile was successfully updated!'))
                return redirect('designer_profile', username=request.user.username)
            else:
                messages.error(request, 'Please correct the error below.')
        elif request.user.is_client:     
            user_form = UserSettingsForm(request.POST, request.FILES or None, instance=request.user)
            
            if user_form.is_valid():       
                user_form.save()     
                messages.success(request, _('Your profile was successfully updated!'))
                return redirect('client_profile', username=request.user.username)
            else:
                messages.error(request, 'Please correct the error below.')
    else:   
        if request.user.is_designer:
            user_form = UserSettingsForm(instance=request.user)      
            profile_form = DesignerSettingsForm(instance=request.user.designer)
            context = {      
        'user_form': user_form,  
        'profile_form': profile_form,
        'username': username
            }
        elif request.user.is_client:
            user_form = UserSettingsForm(instance=request.user)            
            context = {      
        'user_form': user_form,        
        'username': username
            }
    return render(request, 'user_profile/settings.html', context)


def delete_profile(request, pk):
    instance = User.objects.get(pk=pk)
    instance.delete()
    return redirect('home')





def profile(request, username):
    profile_user = User.objects.get(username=username)
    if profile_user.is_designer:
        designer = get_object_or_404(Designer, user_id=profile_user.id)
        skills = designer.skills.all()
        projects = designer.projects.all()
        context = {
            "user": request.user,
            "designer_user": profile_user,
            "designer": designer, 
            "skills": skills,
            "projects": projects,
            "username": username
        }
        return render(request, 'user_profile/designer_detail.html', context)
    else:
        user = get_object_or_404(User, username=username)    
        context = {
            "client_user": user,         
            "username": username
        }
        return render(request, 'user_profile/client_detail.html', context)

    return HttpResponse(username)