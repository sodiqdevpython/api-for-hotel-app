from django.contrib import admin
from .models import Category, Services, MultipleServiceImages, Profile, UsedServices, LoginSystem

admin.site.register(Category)

admin.site.register(MultipleServiceImages)

@admin.register(Services)
class AdminViewService(admin.ModelAdmin):
    list_display = ['title', 'open', 'close', 'who_has_this', 'category', 'tel_number']

@admin.register(Profile)
class AdminViewProfile(admin.ModelAdmin):
    list_display = ['who', 'gender', 'status', 'arrival_date', 'time_to_leave', 'tel_number']

@admin.register(UsedServices)
class AdminViewUsedServices(admin.ModelAdmin):
    list_display = ['who_used', 'which_services', 'when']

@admin.register(LoginSystem)
class AdminViewLoginSystem(admin.ModelAdmin):
    list_display = ['username', 'password']
    search_fields = ['username', 'password']