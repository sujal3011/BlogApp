from django.shortcuts import render
from .serializers import BlogSerializer,CommentSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog,Comment
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3Mzg0MjgyMCwiaWF0IjoxNjczNzU2NDIwLCJqdGkiOiJlOTNhZDVmYzAxNjM0Zjg0OTczMDM0OWRkZDBiMzlhOCIsInVzZXJfaWQiOjV9.i6WsGNE3MyJUXVM3uEM8rd_GL8IRmNkTBZa52HoPOA8


class PublicBlogView(APIView):

    def get(self,request):
        try:
            blogs=Blog.objects.all().order_by("?")  

            if request.GET.get('search'): 
                search=request.GET.get('search')
                print(search)
                
                blogs=blogs.filter( Q(title__icontains=search) | Q(description__icontains=search))
                print(blogs)
            
            paginator=Paginator(blogs,2)
            page_number=request.GET.get('page')

            page_blogs=paginator.page(page_number)


            serializer=BlogSerializer(page_blogs,many=True)

            return Response({
                    'data':serializer.data,
                    'message':"blogs fetched successfully"
                },status=status.HTTP_200_OK)



        except Exception as e:

            return Response({
                    'data':{},
                    'message':"something went wrong or invalid page number"
                },status=status.HTTP_400_BAD_REQUEST)



class BlogView(APIView):

    authentication_classes = [JWTAuthentication]  #authenticating using JWT token 
    permission_classes = [IsAuthenticated]  #permissions(authorization)

    def get(self,request):
        try:
            blogs=Blog.objects.filter(user=request.user)
            print(blogs)

            if request.GET.get('search'):  # request.GET is a dictionary(key-value pairs) of all the GET variables,.get() methos is used to get value of a particular key
                search=request.GET.get('search')
                print(search)

                blogs=blogs.filter(Q(title__icontains=search) | Q(description__icontains=search))  # Q objects is used doing advanced quering
                print(blogs)



            serializer=BlogSerializer(blogs,many=True)  #serializing data

            return Response({
                    'data':serializer.data,
                    'message':"blogs fetched successfully"
                },status=status.HTTP_200_OK)



        except Exception as e:

            return Response({
                    'data':{},
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)


    def post(self,request):

        try:

            data=request.data
            data['user']=request.user.id
            serializer=BlogSerializer(data=data)  # deserializing data

            if not serializer.is_valid():

                return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                    'data':serializer.data,
                    'message':"blog created successfully"
                },status=status.HTTP_201_CREATED)


        except Exception as e:

            return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self,request):
        try:

            data=request.data

            blog=Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():

                return Response({
                    'data':{},
                    'message':"blog not found"
                },status=status.HTTP_400_BAD_REQUEST)

            if blog[0].user!=request.user:

                return Response({
                    'data':{},
                    'message':"not authorized"
                },status=status.HTTP_400_BAD_REQUEST)

            serializer=BlogSerializer(blog[0],data=data,partial=True)

            if not serializer.is_valid():

                return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                    'data':serializer.data,
                    'message':"blog updated successfully"
                },status=status.HTTP_201_CREATED)
        
        except Exception as e:

            return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:

            data=request.data

            blog=Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():

                return Response({
                    'data':{},
                    'message':"blog not found"
                },status=status.HTTP_400_BAD_REQUEST)

            if blog[0].user!=request.user:

                return Response({
                    'data':{},
                    'message':"not authorized"
                },status=status.HTTP_400_BAD_REQUEST)

            blog[0].delete()

            return Response({
                    'data':{},
                    'message':"blogs deleted successfully"
                },status=status.HTTP_200_OK)

        except Exception as e:

            return Response({
                    'data':{},
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)




class CommentView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            comments=Comment.objects.filter(blog=request.data.get('blog'))
            print(comments)

            serializer=CommentSerializer(comments,many=True)  #serializing data

            return Response({
                    'data':serializer.data,
                    'message':"comments fetched successfully"
                },status=status.HTTP_200_OK)



        except Exception as e:

            return Response({
                    'data':{},
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)


    def post(self,request):

        try:

            data=request.data
            data['user']=request.user.id
            # data['blog']=request.blog.id
            serializer=CommentSerializer(data=data)  # deserializing data

            if not serializer.is_valid():

                return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                    'data':serializer.data,
                    'message':"blog created successfully"
                },status=status.HTTP_201_CREATED)


        except Exception as e:

            return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request):
        try:

            data=request.data

            comment=Comment.objects.filter(uid=data.get('uid'))

            if not comment.exists():

                return Response({
                    'data':{},
                    'message':"comment not found"
                },status=status.HTTP_400_BAD_REQUEST)

            if comment[0].user!=request.user:

                return Response({
                    'data':{},
                    'message':"not authorized"
                },status=status.HTTP_400_BAD_REQUEST)

            serializer=CommentSerializer(comment[0],data=data,partial=True)

            if not serializer.is_valid():

                return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                    'data':serializer.data,
                    'message':"blog updated successfully"
                },status=status.HTTP_201_CREATED)
        
        except Exception as e:

            return Response({
                    'data':serializer.errors,
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:

            data=request.data

            comment=Comment.objects.filter(uid=data.get('uid'))

            if not comment.exists():

                return Response({
                    'data':{},
                    'message':"comment not found"
                },status=status.HTTP_400_BAD_REQUEST)

            if comment[0].user!=request.user:

                return Response({
                    'data':{},
                    'message':"not authorized"
                },status=status.HTTP_400_BAD_REQUEST)

            comment[0].delete()

            return Response({
                    'data':{},
                    'message':"comment deleted successfully"
                },status=status.HTTP_200_OK)

        except Exception as e:

            return Response({
                    'data':{},
                    'message':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)


        























