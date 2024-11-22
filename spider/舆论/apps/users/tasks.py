import time

from celery import shared_task

### 写个类，继承 Task，写方法
from celery import Task

from django.core.mail import send_mail
from django.conf import settings




@shared_task
def add(a, b):
    return a + b
