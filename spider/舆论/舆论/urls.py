
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app01/', include('celery_dome.urls')),  # http://127.0.0.1:8000/app01/send/  异步发邮件
]