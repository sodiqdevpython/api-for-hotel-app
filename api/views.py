from django.shortcuts import render
from rest_framework.response import Response
from .models import Category, Services, Profile, UsedServices, MultipleServiceImages
from .serializers import CategorySerializer, ServiceSerializer, MultipleServiceImageSerializer, ProfileSerializer, UsedServicesSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class ListCategories(APIView):
    def get(self, request):
        categories = Category.objects.all()[:10]
        serialized = CategorySerializer(categories, many=True)
        context = {
            'user': self.request.user.username,
            'categories': serialized.data
        }
        return Response(context)

class ListServices(ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_fields = ['category']

class MultipleServiceImageView(ListAPIView):
    queryset = MultipleServiceImages.objects.all()
    serializer_class = MultipleServiceImageSerializer

class ProfileView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UsedServicesView(ListAPIView):
    queryset = UsedServices.objects.all()
    serializer_class = UsedServicesSerializer

class UsedServicesDetailView(APIView):
    def get(self, request, pk):
        used_services = UsedServices.objects.filter(who_used=pk)
        serializered = UsedServicesSerializer(used_services, many=True)
        context = {
            'results': serializered.data
        }
        return Response(context)

class CreateUsedServicesView(CreateAPIView):
    queryset = UsedServices
    serializer_class = UsedServicesSerializer

