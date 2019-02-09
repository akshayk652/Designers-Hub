from django import forms
from .models import ContractFile
from .models import Contract
from user_profile.models import Designer
from django.contrib.auth import get_user_model


User = get_user_model()

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = ContractFile
        fields = ('description', 'file_path',)


class ContractForm(forms.Form):
    title = forms.CharField(
        label="title",
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Name of Project'}),
        required=True
    )

    description = forms.CharField(
        label="description",
        widget=forms.Textarea(),
        required=True
    )

    username = forms.CharField(
        label="designer-username",
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Designer Username'}),
        required=True
    )    

    def clean_username(self):
        value = self.cleaned_data["username"]
        data = User.objects.filter(username=value).first()
        if data:
            return data

        raise forms.ValidationError("This username doesn't exist")

