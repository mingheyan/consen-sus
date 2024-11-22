from django.contrib import admin
from django.urls import path,include

from utils.converters import UsernameConverter
from django.urls import register_converter

register_converter(UsernameConverter,'username')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app01/', include('apps.celery_dome.urls')),
    path('',include('apps.users.urls')),# http://127.0.0.1:8000/app01/send/  异步发邮件
]