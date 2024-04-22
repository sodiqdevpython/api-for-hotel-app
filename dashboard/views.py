from django.shortcuts import render, redirect, HttpResponse
from api.models import Services, Profile, UsedServices, LoginSystem
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CreateNewUserForm, CustomLoginForm
from django.contrib.auth import authenticate, login

@login_required
def dashboard(request):
    services = Services.objects.all()[:10]
    overall_users = Profile.objects.all().count()
    male = Profile.objects.filter(gender="ER").count()
    used_services = UsedServices.objects.all()[:6][::-1]
    context = {
        'services': services,
        'male': male,
        'overall_users': overall_users,
        'female': overall_users-male,
        'users': Profile.objects.all()[:5],
        'used_services': used_services
    }


    return render(request, 'index.html', context)

@login_required
def show_profile(request):
    profile_data = Profile.objects.all()[:50]
    return render(request, 'profile/users.html', {'profile_data': profile_data})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse('Wrong username or password')
        else:
            print(form.errors)
            return HttpResponse('Form is not valid')
    else:
        form = CustomLoginForm()

    context = {
        'form': form
    }
    return render(request, 'authentication-login.html', context)


def add_new_user(request):
    if request.method=='POST':
        form = CreateNewUserForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(
                username = data['username'],
                password = data['password'],
                first_name = data['first_name'],
                last_name = data['last_name']
            )
            new_user_login = LoginSystem.objects.create(
                username = new_user,
                password = data['password'] 
            )
            new_user_login.save()

            profile = Profile.objects.create(
                who = new_user,
                gender = data['gender'],
                status = data['status'],
                arrival_date = data['arrival_date'],
                time_to_leave = data['time_to_leave'],
                tel_number = data['tel_number']
            )

            return redirect('users_profile')
        else:
            print(form.errors)
            return HttpResponse('Nimadir xato ketdi')
    else:
        form = CreateNewUserForm()
    
    context = {
        'form': form
    }

    return render(request, 'profile/register.html', context)