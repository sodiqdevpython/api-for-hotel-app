from rest_framework.serializers import ModelSerializer
from .models import Category, Services, Profile, UsedServices, MultipleServiceImages
from django.contrib.auth.models import User
from rest_framework import serializers


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'
        depth = 1


class MultipleServiceImageSerializer(ModelSerializer):
    class Meta:
        model = MultipleServiceImages
        fields = '__all__'


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UsedServicesSerializer(ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = UsedServices
        fields = ['who_used', 'user_name', 'which_services', 'when']

    def get_user_name(self, obj):
        return obj.who_used.who.username
