from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import ListCategories, ListServices, MultipleServiceImageView, ProfileView, UsedServicesView, CreateUsedServicesView, UsedServicesDetailView, DetailServiceView, LoginViewAPI, ReadOrderingView, ReadOrderingDetailView, CreateOrderingDetailView
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
    path('ordering/', ReadOrderingView.as_view()),
    path('ordering/<int:service>/<int:user>/', ReadOrderingDetailView.as_view()),
    path('ordering/add/', CreateOrderingDetailView.as_view())
    # path('add_order/<int:service_id>/<int:user_id>/', add_order)
    # path('order/', BasicOrderingModelSerializerListView.as_view()),
    # path('order/<int:service_id>/', BasicOrderingModelSerializerDetailView.as_view()),
    # path('add_order/<int:service_id>/<int:user_id>/', add_order),
]
