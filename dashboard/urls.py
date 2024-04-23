from django.urls import path
from .views import dashboard, show_profile, login_view, add_new_user, create_new_service, show_user_profile, delete_user, add_used_service
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('show_users/', show_profile, name='users_profile'),
    path('login2/', login_view, name='login2'),
    path('create/user/', add_new_user, name='create_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/service/', create_new_service, name='create_service'),
    path('profile/data/<str:username>/', show_user_profile, name='user_profile_detail'),
    path('delete/user/<str:username>/', delete_user, name='delete_user'),
    path('add_used_service/<str:username>/<int:which_service_id>/', add_used_service, name='add_used_service'),
]
