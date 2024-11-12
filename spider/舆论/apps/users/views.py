from django.shortcuts import render

# Create your views here.

from django.views import View
from apps.users.models import User
from django.http import JsonResponse,HttpResponse
import json
from django.contrib.auth import login
import re
from .tasks import add
from django.shortcuts import render


class UsernameCountView(View):
    def get(self, request, username):
        # 验证合法
        if not re.match('^[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 1, 'errmsg': '用户不满足要求'})
        # 数据库查询
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})



class LoginView(View):
    def get(self, request):
        # res=add.delay(11,22)
        # print(res)
        return render(request,'登录/login.html')
class RegisterView(View):
    def get(self, request):
        request_a = request.body
        print(request_a)
        password=request.GET.get('password')
        response = HttpResponse("Cookie 设置成功")
        response.set_cookie('my_cookie', 'cookie_value', max_age=30)  # 设置 Cookie，有效期为 1 小时
        print(password)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

