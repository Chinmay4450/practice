from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Customers, UserInfo,Country,State,Otpdata
from datetime import timedelta
from .serializers import RegistrationSerializer, PasswordSerializer, ChangeProfile,UserSerializer,DisplayCountry,DisplayState,EmailSerializer,PasswordOtpSerializer,ChangePasswordSerializer
from Cedar.settings import DEFAULT_FROM_EMAIL
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import account_activation_token
from rest_framework.reverse import reverse
from django.core.mail import EmailMessage
from rest_framework.generics import GenericAPIView
from django.contrib import messages
import random
import string
from django.utils import timezone
from rest_framework.permissions import DjangoModelPermissions,DjangoObjectPermissions,IsAuthenticated
from rest_framework import permissions
import copy

randomab = ''.join([random.choice(string.ascii_letters + string.digits ) for n in range(8)])

randomotp = ''.join([random.choice(string.digits ) for n in range(6)])



class CustomDjangoModelPermission(permissions.DjangoModelPermissions):

    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)  # from EunChong's answer
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class RegistrationView(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = Customers.objects.all()

    def create(self, request, *args, **kwargs):
    
        
        if UserInfo.objects.filter(email=request.data['admin']['email']).exists():
            return Response({'email_error': 'sorry email in use,choose another one '}, status=409)
        
        data = request.data
        
        if request.user.id is None:
            pass      
        else:
            data['created_by'] = request.user.id
            data['updated_by'] = request.user.id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        current_site = get_current_site(request)
        user = UserInfo.objects.get(email=request.data['admin']['email'])
        user.set_password(randomab)
        user.save()
        
        link = reverse('rest_login')

        email_subject = 'Account Created Successfully' + current_site.domain

        activate_url = 'http://' + current_site.domain + link

        emailsend = EmailMessage(
            email_subject,
            'Hi ' + user.first_name +'\n'+"username : "+user.username +'\n'+"password : "+ randomab +'\n'+', Please click the link below to login \n' + activate_url,
            DEFAULT_FROM_EMAIL,
            [user.email],
        )

        emailsend.send(fail_silently=False)
        
        return Response({'Message': 'User created Successfully.'},
                        status=status.HTTP_201_CREATED)
        
                    


class PasswordView(GenericAPIView):
    serializer_class = PasswordSerializer

    def post(self, request, *args, **kwargs):

        if request.data['password'] != request.data['confirm_password']:
            return Response({'password error': 'passwords do not match'}, status=409)
        else:
            obj = UserInfo.objects.get(pk=request.user.id)
            obj.set_password(request.data['password'])
            obj.verified=True
            obj.save()
            return Response({'password set': 'password set for your account '}, status=200)


class ChangeProfileForAdminView(viewsets.ModelViewSet):
    serializer_class = ChangeProfile

    def get_queryset(self):
        return Customers.objects.filter(admin__username=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        admin = Customers.objects.get(pk=self.kwargs.get('pk'))
        data = request.data
        data['updated_by'] = request.user.id
        x = Customers.objects.filter(id=self.kwargs.get('pk')).values_list('admin__id', flat=True).last()
        user_object = UserInfo.objects.get(id=x)

        serializer = ChangeProfile(admin, data=data,
                                   partial=True)
        serializer1 = UserSerializer(user_object, data=data,
                                     partial=True)

        if serializer.is_valid(raise_exception=True) and serializer1.is_valid():
            self.perform_update(serializer)
            self.perform_update(serializer1)
            serializer.save()
            serializer1.save()

            return Response({'data': [serializer.data]}, status=status.HTTP_200_OK)

        return Response({'message': 'Wrong Parameters'}, status=status.HTTP_400_BAD_REQUEST)


class DisplayCountryView(viewsets.ModelViewSet):
    serializer_class = DisplayCountry
    queryset = Country.objects.all()
    permission_classes = (DjangoModelPermissions,)


class DisplayStateView(viewsets.ModelViewSet):
    serializer_class = DisplayState
    queryset = State.objects.all()

    filterset_fields = {'country': ['exact']}
    

class ResetPasswordRequestToken(GenericAPIView):
   
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        activeuser = UserInfo.objects.filter(email=email)
        if not activeuser:
            return Response({'status':'There is no active user associated with this e-mail address'})
        email_subject = 'Reset Password'
        emailsend = EmailMessage(
            email_subject,
            'Hi ' +'\n'+"otp is : "+ randomotp ,
            DEFAULT_FROM_EMAIL,
            [email],
        )
     
        emailsend.send(fail_silently=False)
        Otpdata.objects.create(email=email,otp=randomotp)
        return Response({'status': 'Otp has been sent to the provided email ID'})
    
    
class ResetPasswordConfirm(GenericAPIView):
    
    serializer_class = PasswordOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']
        if password != confirm_password:
            return Response({'status': 'Password did not match'}, status=status.HTTP_400_BAD_REQUEST)
        

        reset_password_otp = Otpdata.objects.filter(email=email).last()
        print(reset_password_otp)
        if not reset_password_otp:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)

        expiry_time = reset_password_otp.created_at + timedelta(hours=1)
         
        if timezone.now() > expiry_time:
            return Response({'status': 'token is expired'}, status=status.HTTP_404_NOT_FOUND)
        if reset_password_otp.otp!=otp:
            return Response({'status': 'Wrong Otp'}, status=status.HTTP_404_NOT_FOUND)
        obj = UserInfo.objects.get(email=email)
        obj.set_password(password)
        obj.save()
        return Response({'status': 'password changed successfully'}, status=status.HTTP_404_NOT_FOUND)
    
    
class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):

        if request.data['password'] != request.data['confirm_password']:
            return Response({'password error': 'passwords do not match'}, status=409)
        
        if not request.user.check_password(request.data['oldpassword']):
            return Response({'password error': 'old password not correct'}, status=409)
        
        obj = UserInfo.objects.get(pk=request.user.id)
        obj.set_password(request.data['password'])
        obj.save()
        return Response({'password ': 'password changed '}, status=200)    


class employee_csvupload_ViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = RegistrationSerializer
    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data["customers"], list):
            print(data["customers"])
            data_class = data["customers"]
            for i in data_class:
                serializer = self.get_serializer(data=i)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                user = UserInfo.objects.get(email=i['admin']['email'])
                user.set_password("123")
                user.save()
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
        return Response({'success ': 'csv uploaded successfully'}, status=200)

