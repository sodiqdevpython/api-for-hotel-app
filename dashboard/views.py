from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from api.models import Profile, LoginSystem, UsedServices, Services
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CreateNewUserForm, CustomLoginForm, CreateServiceForm, UsedServiceForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

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

@login_required
def add_new_user(request):
    if request.method == 'POST':
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

            return redirect('user_profile_detail', username=data['username'])
        else:
            print(form.errors)
            return HttpResponse('Nimadir xato ketdi')
    else:
        form = CreateNewUserForm()
    
    context = {
        'form': form
    }

    return render(request, 'profile/register.html', context)

@login_required
def create_new_service(request):
    if request.method == 'POST':
        form = CreateServiceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            pass

    else:
        form = CreateServiceForm()
    
    context = {
        'form': form
    }

    return render(request, 'service/create_service.html', context)

@login_required
def show_user_profile(request, username):
    user = get_object_or_404(User, username=username)
    used_services = UsedServices.objects.filter(who_used__who__username=username)
    return render(request, 'profile/detail_user_profile.html', {'user': user, 'used_services': used_services})

@login_required
def delete_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.delete()
        return redirect('users_profile')
    else:
        return HttpResponse('Nimadir xato ketdi')

def add_used_service(request, username, which_service_id):

    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, who=user)
    service = get_object_or_404(Services, pk=which_service_id)

    if request.method == 'POST':
        form = UsedServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        initial_data = {'who_used': profile.id, 'which_services': service.id}
        form = UsedServiceForm(initial=initial_data)

    context = {
        'form': form,
        'user_name': user.first_name,
        'service': service
    }

    return render(request, 'service/add_used_service.html', context)

def success_page(request):
    return render(request, 'service/success_used_service.html')