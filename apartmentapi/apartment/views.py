import string
import urllib
from rest_framework import viewsets, generics, parsers, permissions
from rest_framework.response import Response as ResponseRest
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.conf import settings
from apartment.models import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
import cloudinary.uploader
from django.utils import timezone
import json
import hmac
import hashlib
import requests
import uuid
import random
from time import time
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from apartment.models import ResidentFee



class ResidentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Resident.objects.all()
    serializer_class = serializers.ResidentSerializer
    parser_classes = [parsers.MultiPartParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action in ['add_reflections', 'get_residentfees', 'upload_avatar', 'update_infor', 'get_reflection',
    #                        'register_vehicle']:
    #         return [permissions.IsAuthenticated()]
    #     return [permissions.AllowAny()]
    @action(methods=['get'], url_path='get_residentfees', detail=False)
    def get_residentfees(self, request):
        user_id = request.user.id
        bill_status = request.query_params.get('status')
        bill_type = request.query_params.get('type')
        bill_name = request.query_params.get('name')
        resident = get_object_or_404(Resident, user_info=user_id)
        residentfees = resident.resident_fees.all()

        if bill_status == "payed":
            residentfees = residentfees.filter(status=ResidentFee.EnumStatusFee.DONE)
        elif bill_status == "unpayed":
            residentfees = residentfees.filter(status=ResidentFee.EnumStatusFee.PENDING)
        elif bill_status == "deny":
            residentfees = residentfees.filter(status=ResidentFee.EnumStatusFee.DENY)

        if bill_type:
            residentfees = residentfees.filter(fee__types=bill_type)

        if bill_name:
            residentfees = residentfees.filter(fee__fee_name__icontains=bill_name)

        paginator = paginators.ServicePaginator()
        page = paginator.paginate_queryset(residentfees, request)
        if page is not None:
            serializer = serializers.ResidentFeeSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return ResponseRest(serializers.ResidentFeeSerializer(residentfees, many=True).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='upload_avatar', url_name='upload_avatar')
    def upload_avatar(self, request, pk):
        # user_id = request.user.id
        user_id = self.get_object()
        print(user_id)
        avatar_file = request.data.get('avatar', None)

        try:
            resident = get_object_or_404(Resident, user_info_id=user_id)
            user = resident.user_info
            new_avatar = cloudinary.uploader.upload(avatar_file)
            user.avatar = new_avatar['secure_url']
            user.save()
        except Resident.DoesNotExist:
            return ResponseRest({'detail': 'Resident not found'}, status=status.HTTP_404_NOT_FOUND)

        return ResponseRest(serializers.ResidentSerializer(resident).data, status=status.HTTP_200_OK)

    @action(methods=['patch'], url_path='update_infor', detail=True)
    def update_infor(self, request, pk=None):
        user_id = self.get_object()
        try:
            resident = get_object_or_404(Resident, user_info_id=user_id)
            user = resident.user_info  # Get the User object associated with the Resident
            for k, v in request.data.items():
                if k == 'id' or k == 'username':
                    continue
                setattr(user, k, v)
            user.save()  # Save the User object
        except Resident.DoesNotExist:
            return ResponseRest({'detail': 'Resident not found'}, status=status.HTTP_404_NOT_FOUND)
        return ResponseRest(serializers.ResidentSerializer(resident).data)  # Return the serialized Resident object

    @action(methods=['post'], url_path='pay_service', detail=True)
    def add_residentfee(self, request, pk=None):
        resident = self.get_object()
        residentfee_data = request.data.copy()
        residentfee_data['resident'] = resident.user_info
        fee_id = residentfee_data.get('fee_id')
        if fee_id:
            try:
                service = Service.objects.get(id=fee_id)
                residentfee_data['fee'] = service  # Set the Service object directly
            except Service.DoesNotExist:
                return ResponseRest({'error': 'Invalid fee_id'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return ResponseRest({'error': 'fee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ResidentFeeSerializer(data=residentfee_data)
        if serializer.is_valid():
            serializer.save()
            return ResponseRest(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return ResponseRest(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class ApartmentViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Apartment.objects.all()
    serializer_class = serializers.ApartmentSerializer
    permission_classes = [permissions.AllowAny]


class ItemViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(item_name__icontains=q)
        return queryset

    @action(methods=['get'], detail=False)
    def get_items(self, request):

        stt = request.query_params.get('status')
        if stt == 'received':
            items = self.queryset.filter(status=True)
        elif stt == 'pending':
            items = self.queryset.filter(status=False)
        else:
            return ResponseRest({'detail': 'Invalid status parameter. Use "received" or "pending".'},
                                status=status.HTTP_400_BAD_REQUEST)

        return ResponseRest(serializers.ItemSerializer(items, many=True).data, status=status.HTTP_200_OK)

   


class ReservationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ReservationVehicle.objects.all()
    serializer_class = serializers.ReservationVehicleSerializer





class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, PermissionRequiredMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, JSONParser]

    def get_permissions(self):
        if self.action in ['get_current_user', 'register_user']:
            return [perms.AdminOwner()]

        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='register_user', url_name='register_user')
    def register_user(self, request):
        try:
            data = request.data
            avatar = data.get("avatar")
            new_avatar = cloudinary.uploader.upload(avatar)

            new_user = User.objects.create_user(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                username=data.get("username"),
                email=data.get("email"),
                password=make_password(data.get("password")),
                avatar=new_avatar['secure_url'],
                phone=data.get("phone"),
                sex=data.get("sex", User.EnumSex.MALE),
                role=data.get("role", User.EnumRole.RESIDENT)
            )

            if new_user.role == User.EnumRole.RESIDENT:
                Resident.objects.create(user_info=new_user)

            return ResponseRest(data=serializers.UserSerializer(new_user, context={'request': request}).data,
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            return ResponseRest(dict(error=str(e)), status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['patch'], url_path='update_password', url_name='change_password')
    def update_password(self, request):
        user = get_object_or_404(User, id=request.user.id)
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)
        print(user)
        if not old_password or not new_password:
            return ResponseRest({'detail': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(old_password):
            user.set_password(new_password)
            user.is_first_login = False
            user.save()
            return ResponseRest({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return ResponseRest({'detail': 'Invalid old password'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return ResponseRest(serializers.UserSerializer(user).data)

    @action(detail=False, methods=['post'], url_path='forgot_password', url_name='forgot_password')
    def forgot_password(self, request):
        email = request.data.get('email', None)
        if not email:
            return ResponseRest({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return ResponseRest({'detail': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        user.password = make_password(new_password)
        user.save()

        send_mail(
            'New Password',
            f'Your new password is: {new_password}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return ResponseRest({'detail': 'New password has been sent to your email address.'}, status=status.HTTP_200_OK)


class AnswerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


class ResponseViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Response.objects.all()
    serializer_class = serializers.ResponseSerializer


class PostViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = paginators.PostPaginator

