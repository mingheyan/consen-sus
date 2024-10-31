from django.shortcuts import render

# Create your views here.

from django.views import View
from apps.users.models import User
from django.http import JsonResponse
import json
from django.contrib.auth import login
import re


def index():
    return JsonResponse({'code': 0, 'errmsg': 'ok'})
class UsernameCountView(View):
    def get(self, request, username):
        # 验证合法
        if not re.match('^[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 1, 'errmsg': '用户不满足要求'})
        # 数据库查询
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})
