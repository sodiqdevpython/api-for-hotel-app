from django import forms
from api.models import Profile
from django.contrib.auth.models import User

class CreateNewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
    
    gender = forms.ChoiceField(choices=Profile.GenderChoice.choices)
    status = forms.ChoiceField(choices=Profile.UserStatusChoice.choices)
    arrival_date = forms.DateField()
    time_to_leave = forms.DateField()
    tel_number = forms.CharField(max_length=20)

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
