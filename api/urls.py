from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import ListCategories, ListServices, MultipleServiceImageView, ProfileView, UsedServicesView, CreateUsedServicesView, UsedServicesDetailView, DetailServiceView, LoginViewAPI
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('categories/', ListCategories.as_view()),
    path('services/<str:user>/', ListServices.as_view()),
    path("services/<int:id>/<str:user>/", DetailServiceView.as_view()),
    path('more_images/', MultipleServiceImageView.as_view()),
    path('profile/<str:user>/', ProfileView.as_view()),
    path('used_services/', UsedServicesView.as_view()),
    path('used_services/<str:user>/', UsedServicesDetailView.as_view()),
    path('add/', CreateUsedServicesView.as_view()),
    # path('auth/', include('rest_framework.urls'))
    path('login/<str:username>/<str:password>/', LoginViewAPI.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
]
