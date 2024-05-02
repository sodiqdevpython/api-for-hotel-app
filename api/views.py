from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Services, UsedServices, MultipleServiceImages, LoginSystem, Ordering
from .serializers import CategorySerializer, ServiceSerializer, MultipleServiceImageSerializer, ProfileSerializer, UsedServicesSerializer, ReadOrderingSerializer, CreateOrderingSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
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

class ReadOrderingView(ListAPIView):
    queryset = Ordering.objects.all()
    serializer_class = ReadOrderingSerializer

class ReadOrderingDetailView(APIView):
    def get(self, request, service, user):
        service_db = Ordering.objects.filter(service=service)
        serializered_data = ReadOrderingSerializer(service_db, many=True).data
        user_has = Ordering.objects.filter(service=service, user=user)
        return Response({'result': serializered_data, 'user_has': len(user_has)==1, 'len': len(serializered_data)})

class CreateOrderingDetailView(APIView):
    def post(self, request):
        get_data = request.data
        user_has = Ordering.objects.filter(service=get_data['service'], user=get_data['user'])
        if len(user_has)==0:
            serializered = CreateOrderingSerializer(data=get_data)
            if serializered.is_valid():
                serializered.save()
                return Response({'status': "ok"})
            else:
                return Response({'status': serializered.errors})
        else:
            user_has.delete()
            return Response({'status': 'deleted'})


# @api_view(['POST'])
# def add_order(request, service_id, user_id):
#     which_service = get_object_or_404(Services, id=service_id)
#     if not which_service.users_for.filter(id=user_id).exists():
#         which_service.users_for.add(user_id)
#         a = "Qo'shildi"
#     else:
#         which_service.users_for.remove(user_id)
#         a = "O'chirildi"
#
#     return Response({
#         'status': 'ok',
#         'service_id': service_id,
#         'user_id': user_id,
#         'result': a
#     })