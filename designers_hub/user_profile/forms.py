from django import forms
from .models import Project, Designer, Skill, User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class DesignerSignUpForm(UserCreationForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'description', 'profile_img')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_designer = True
        user.save()
        designer = Designer.objects.create(user=user)
        designer.skills.add(*self.cleaned_data.get('skills'))
        # import pdb; pdb.set_trace()
        return user



class ClientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'description', 'profile_img')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True
        if commit:
            user.save()
        return user



class DesignerSkillsForm(forms.ModelForm):
    class Meta:
        model = Designer
        fields = ('skills', )
        widgets = {
            'skills': forms.CheckboxSelectMultiple
        }




# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


# class DesignerRegisterForm(UserCreationForm):
    
#     class Meta:
#         model = Designer
#         fields = ['account_type', 'profile_img']


# class ClientRegisterForm(UserCreationForm):
    
#     class Meta:
#         model = Client
#         fields = ['account_type', 'profile_img']



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('designer',)

      # def save(self, commit=True):
      #   self.instance.designer = self.request.user
      #   return super().save(commit=commit)

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_img')


class DesignerSettingsForm(forms.ModelForm):
    class Meta:
        model = Designer
        fields = ('skills', 'experience',)