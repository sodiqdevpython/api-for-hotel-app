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
        fields = ['id' ,'title', 'open', 'close', 'location', 'who_has_this', 'category', 'tel_number', 'info', 'image', 'more_images']
        depth = 2


class MultipleServiceImageSerializer(ModelSerializer):
    class Meta:
        model = MultipleServiceImages
        fields = '__all__'


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


from rest_framework.fields import DateTimeField

class UsedServicesSerializer(ModelSerializer):
    user_name = serializers.SerializerMethodField()
    which_services_title = serializers.SerializerMethodField()
    when = DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UsedServices
        fields = ['who_used', 'user_name', 'which_services', 'which_services_title', 'when']

    def get_user_name(self, obj):
        return obj.who_used.who.username

    def get_which_services_title(self, obj):
        return obj.which_services.title

