
from django.contrib.auth.models import Group
from rest_framework import serializers, exceptions
from .models import UserInfo, Customers,Country,State,Otpdata
from django.utils.translation import gettext_lazy as _




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['salutation', 'username', 'first_name', 'last_name', 'email','phone']


# class UserEmployeeSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, write_only=True)
#
#     class Meta:
#         model = UserInfo
#         fields = ['salutation', 'username', 'first_name', 'last_name', 'email', 'phone', 'password']


class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(label=_("Confirm_Password"), style={'input_type': 'password'},
                                             write_only=True)

    class Meta:
        model = UserInfo
        fields = ['password', 'confirm_password']


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['username']


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        exclude = ['groups', 'user_permissions', 'password']


class RegistrationSerializer(serializers.ModelSerializer):
    admin = UserSerializer(many=False)

    class Meta:
        model = Customers
        fields = '__all__'
        extra_fields = ['admin']

    def create(self, validated_data):
        user = validated_data.get('admin')
        user1 = UserInfo(**user)
        user1.save()
        admin = validated_data.pop('admin')
        admin1 = Customers.objects.create(admin=user1, **validated_data)
        admin1.save()
        return admin1

    def update(self, instance, validated_data):
        nested_serializer = self.fields['admin']
        nested_instance = instance.admin
        # note the data is `pop`ed
        nested_data = validated_data.pop('admin')
        nested_serializer.update(nested_instance, nested_data)
        # this will not throw an exception,
        # as `profile` is not part of `validated_data`
        return super(RegistrationSerializer, self).update(instance, validated_data)


class ChangeProfile(serializers.ModelSerializer):
    admin = UserSerializer(many=False)
    #password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Customers
        fields = '__all__'
        extra_fields = ['admin']


class UserEmployeeSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserInfo
        fields = ['salutation','username', 'first_name', 'last_name', 'email','phone',]
        
        
class DisplayCountry(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class DisplayState(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'        
        

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class PasswordOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp=serializers.IntegerField(label=_("Otp"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    confirm_password = serializers.CharField(label=_("Confirm password"), style={'input_type': 'password'})   
    
class ChangePasswordSerializer(serializers.Serializer):
    oldpassword=serializers.CharField()
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    confirm_password = serializers.CharField(label=_("Confirm password"), style={'input_type': 'password'})    