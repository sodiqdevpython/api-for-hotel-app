from rest_framework.fields import DateTimeField
from rest_framework.serializers import ModelSerializer
from .models import Category, Services, Profile, UsedServices, MultipleServiceImages, Ordering
from rest_framework import serializers


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Services
        fields = ['id' ,'title', 'open', 'close', 'location', 'who_has_this', 'category', 'tel_number', 'info', 'image','qr_code' ,'more_images', 'users_for', 'duration']
        depth = 2


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
    which_services_title = serializers.SerializerMethodField()
    when = DateTimeField(format="%Y-%m-%d %H:%M:%S")
    image = serializers.SerializerMethodField()

    class Meta:
        model = UsedServices
        fields = ['who_used', 'user_name', 'which_services', 'which_services_title', 'when', 'image']

    def get_user_name(self, obj):
        return obj.who_used.who.username

    def get_which_services_title(self, obj):
        return obj.which_services.title

    def get_image(self, obj):
        return str(obj.which_services.image)


class ReadOrderingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    class Meta:
        model = Ordering
        fields = ['service', 'user', 'order_date', 'user_id']

    def get_user(self, obj):
        return obj.user.username.username

    def get_user_id(self, obj):
        return obj.user.id

class CreateOrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordering
        fields = ['service', 'user']