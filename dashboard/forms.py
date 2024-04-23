from django import forms
from api.models import Profile, Services, UsedServices
from django.contrib.auth.models import User

class CreateNewUserForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Profile.GenderChoice.choices,
                               widget=forms.Select(attrs={'class': 'form-control'}),
                               label="Jins")
    status = forms.ChoiceField(choices=Profile.UserStatusChoice.choices,
                               widget=forms.Select(attrs={'class': 'form-control'}),
                               label="Holati")
    arrival_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                   label="Kelish sanasi")
    time_to_leave = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    label="Ketish sanasi")
    tel_number = forms.CharField(max_length=20,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label="Telefon raqami")

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': "Foydalanuvchi nomi",
            'password': "Parol",
            'first_name': "Ism",
            'last_name': "Familiya",
        }




class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['title', 'open', 'close', 'location', 'who_has_this', 'category', 'tel_number', 'info', 'image', 'more_images']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'open': forms.TextInput(attrs={'class': 'form-control'}),
            'close': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'who_has_this': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tel_number': forms.TextInput(attrs={'class': 'form-control'}),
            'info': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'more_images': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

        labels = {
            'title': 'Nomi',
            'open': "Ish vaqti(boshlanishi)",
            'close': 'Ish vaqti (tugashi)',
            'location': "Joylashuvi (masalan: 1-Qavat)",
            'who_has_this': "Qaysi turdagilar foydalana olsin",
            'category': 'Qaysi kategoriyaga tegishli',
            'tel_number': "Bog'lanish uchun telefon raqam",
            'info': "Ko'proq ma'lumot",
            'image': "Rasmi",
            'more_images': "Ko'proq rasmlari joylashgan papka nomi"
        }

class UsedServiceForm(forms.ModelForm):
    class Meta:
        model = UsedServices
        fields = ['who_used', 'which_services']
