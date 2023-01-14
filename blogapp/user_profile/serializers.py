from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.Serializer):
    first_name=serializers.CharField(max_length=100)
    last_name=serializers.CharField(max_length=100)
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=20)

    def validate(self,data):

        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("Username already exists")
        else:
            return data
    

    def create(self,validated_data):
        user=User.objects.create(first_name=validated_data['first_name'],last_name=validated_data['last_name'],username=validated_data['username'].lower())

        user.set_password(validated_data['password'])

        return validated_data


class LoginSerializer(serializers.Serializer):

    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=20)


    def validate(self,data):

        if not User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("Account not found")
        else:
            return data
    

    def get_jwt_token(self,data):


        user = authenticate(username=data['username'], password=data['password'])  #authenticating the user who is trying to login in using django authentication

        if not user:

            return {'message':'invalid credentials','data':{}}


        refresh = RefreshToken.for_user(user)  #if authentication is successful,generating the jwt token

        return {
            'message':'token created successfully',
            'data':{
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }







