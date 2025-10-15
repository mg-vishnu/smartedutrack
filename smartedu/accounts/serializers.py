from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
    def validate_role(self, value):
        if value not in ['teacher', 'parent']:
            raise serializers.ValidationError("Role must be teacher or parent")
        return value

    def create(self, validated_data):   
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class SessionLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        if not user.is_active:
            raise serializers.ValidationError("Account disabled, contact administrator")

        return user

class PasswordResetRequestSerializers(serializers.Serializer):
    email=serializers.EmailField()

    def validate_email(self,value):
        try:
            user=User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user with this email does not exits")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid=serializers.CharField()
    token=serializers.CharField()
    new_password=serializers.CharField(write_only=True)

    def validate(self,data):
        try:
            uid=force_str(urlsafe_base64_decode(data['uid']))
            user=User.objects.get(pk=uid)
        except (User.DoesNotExist,ValueError,TypeError,OverFlowError):
            raise serializers.ValidationError("invalid Uid")

        if not default_token_generator.check_token(user,data['token']):
            raise serializers.ValidationError("invalid or expired")
        
        data['user']=user
        return data
    
    def save(self):
        user=self.validated_data['user']
        new_password=self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user