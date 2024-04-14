from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ListCategories, ListServices, MultipleServiceImageView, ProfileView, UsedServicesView, CreateUsedServicesView, UsedServicesDetailView, DetailServiceView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('categories/', ListCategories.as_view()),
    path('services/', ListServices.as_view()),
    path("services/<int:pk>/", DetailServiceView.as_view()),
    path('more_images/', MultipleServiceImageView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('used_services/', UsedServicesView.as_view()),
    path('used_services/<int:pk>/', UsedServicesDetailView.as_view()),
    path('add/', CreateUsedServicesView.as_view()),
    path('login/', obtain_auth_token, name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
]
