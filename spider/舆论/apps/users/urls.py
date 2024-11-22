from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views
# from .views import index

urlpatterns = [
# 判断用户名是否重复
path('usernames/<username:username>/count/',views.UsernameCountView.as_view()),
path('start/',views.LoginView.as_view()),
path('register/',views.RegisterView.as_view()),
# path('index/',index),
]

