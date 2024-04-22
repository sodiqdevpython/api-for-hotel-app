from django.urls import path
from .views import dashboard, show_profile, login_view, add_new_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('show_users/', show_profile, name='users_profile'),
    path('login2/', login_view, name='login2'),
    path('create/user/', add_new_user, name='create_user'),
    path('logout/', LogoutView.as_view(), name='logout')
]
