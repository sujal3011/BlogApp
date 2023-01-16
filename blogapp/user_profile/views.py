from django.shortcuts import render
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class RegisterView(APIView):

    def post(self,request):

        try:


            data=request.data
            serializer=RegisterSerializer(data=data)

            if not serializer.is_valid():

                return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                    'data':serializer.data,
                    'message':"account created successfully"
                },status=status.HTTP_201_CREATED)

        
        except Exception as e:

            return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):

    def post(self,request):

        try:

            data=request.data
            serializer=LoginSerializer(data=request.data)

            if not serializer.is_valid():

                return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)


            response=serializer.get_jwt_token(serializer.data)  #if serializer is valid,the getting the jwt token

            return Response(response,status=status.HTTP_200_OK)

        except Exception as e:

            return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)


        



        

        


    
