from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

urlpatterns = [
# 判断用户名是否重复
path('usernames/<username:username>/count/',views.UsernameCountView.as_view()),
]