from rest_framework import serializers
from account.models import User
import re

class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('email','first_name','last_name','phone','role','password','password2')
        extra_kwargs = {
            'password': {'write_only': True}, #to hide password field
        }

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_phone(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise serializers.ValidationError("Phone number must be 10 digits")
        return value

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return data
    
    def create(self,validated_data):
        validated_data.pop("password2")
        password = validated_data.get('password')
        user = User.objects.create_user(**validated_data)
        return user


        

