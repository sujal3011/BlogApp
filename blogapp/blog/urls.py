from django.contrib import admin
from django.urls import path

from .views import BlogView,PublicBlogView,CommentView

urlpatterns = [
    path('home', BlogView.as_view()),
    path('public-blogs', PublicBlogView.as_view()),
    path('comments', CommentView.as_view())
]
