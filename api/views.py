from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from .models import Category, Services, Profile, UsedServices, MultipleServiceImages, LoginSystem
from .serializers import CategorySerializer, ServiceSerializer, MultipleServiceImageSerializer, ProfileSerializer, UsedServicesSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User


class ListCategories(APIView):
    def get(self, request):
        categories = Category.objects.all()[:50]
        serialized = CategorySerializer(categories, many=True)
        context = {
            'user': self.request.user.username,
            'categories': serialized.data
        }
        return Response(context)

# class DetailServiceView(RetrieveAPIView):
#     queryset = Services
#     serializer_class = ServiceSerializer

class DetailServiceView(APIView):

    def get(self, request, id, user):
        service = get_object_or_404(Services, id=id)
        which_user = get_object_or_404(User, username=user)

        is_used = UsedServices.objects.filter(who_used=which_user.id, which_services=id).count()
        serializered = ServiceSerializer(service).data

        if service.who_has_this=='ST' and which_user.profile.status=='ST':
            if is_used==2:
                is_allowed = 'false'
            else:
                is_allowed = 'true'
        elif service.who_has_this=='LY' and which_user.profile.status=='ST':
            is_allowed = 'false'
        elif (service.who_has_this=='ST' and which_user.profile.status=='LY') or (service.who_has_this=='LY' and which_user.profile.status=='LY'):
            if is_used==4:
                is_allowed = 'false'
            else:
                is_allowed = 'true'

        return Response({
            'status': 'ok',
            'used': is_used,
            'is_allowed': is_allowed,
            'data': serializered
        })

class ListServices(APIView):
    
    def get(self, request, user):
        user_data = get_object_or_404(User, username=user)
        get_list = Services.objects.all()
        serializered = ServiceSerializer(get_list, many=True).data
        if user_data.profile.status=='ST':
            allowed_services_data = Services.objects.filter(who_has_this='ST')
            serializered_allowed_services = ServiceSerializer(allowed_services_data, many=True).data
            context = {
                'status': 'Standard',
                'result': serializered,
                'allowed_services': serializered_allowed_services
            }
        else:
            context = {
                'status': 'Lyuks',
                'result': serializered,
                'allowed_services': serializered
            }
        return Response(context)

class MultipleServiceImageView(ListAPIView):
    queryset = MultipleServiceImages.objects.all()
    serializer_class = MultipleServiceImageSerializer

# class ProfileView(ListAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

class ProfileView(APIView):

    def get(self, request, user):
        user_profile = get_object_or_404(User, username = user)
        serializered = ProfileSerializer(user_profile.profile).data
        context = {
            'name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'user': serializered
        }

        return Response(context)

class UsedServicesView(ListAPIView):
    queryset = UsedServices.objects.all()
    serializer_class = UsedServicesSerializer

class UsedServicesDetailView(APIView):
    def get(self, request, user):
        which_user = get_object_or_404(User, username=user)
        used_services = UsedServices.objects.filter(who_used=which_user.id)
        serializered = UsedServicesSerializer(used_services, many=True)
        context = {
            'results': serializered.data
        }
        return Response(context)

class CreateUsedServicesView(CreateAPIView):
    queryset = UsedServices
    serializer_class = UsedServicesSerializer

class LoginViewAPI(APIView):

    def get(self, request, username, password):
        user = get_object_or_404(User, username=username)
        if LoginSystem.objects.filter(username=user.id, password=password):
            context = {
                'status': 'ok'
            }
        else:
            context = {
                'status': 'error'
            }
        
        return Response(context)