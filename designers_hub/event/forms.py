from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class Event_Form(forms.Form):
    name = forms.CharField(
        label='name',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Name of the Event'}),
        required=True
    )

    description = forms.CharField(
        label="About event",
        widget=forms.Textarea(attrs={'cols': '40', 'rows': '10',}),
        required=True
    )

    topic = forms.CharField(
        label='topic',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Topic'}),
        required=True
    )

    points = forms.IntegerField(
        label='points',
        min_value=100,
        max_value=1000,
        widget=forms.NumberInput(attrs={'size':'10'})
    )

 