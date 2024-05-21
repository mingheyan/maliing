import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import login
from .models import User
import re
from django_redis import get_redis_connection
import redis


# Create your views here.
class UsernameCountView(View):
        def get(self, request,username):
            #验证合法
                if not re.match('^[a-zA-Z0-9_-]{5,20}', username):
                    return  JsonResponse({'code':1,'errmsg':'用户不满足要求'})
            #数据库查询
                count = User.objects.filter(username=username).count()
                return JsonResponse({'code':0,'count':count,'errmsg':'ok'})


class MobilecountView(View):

    def get(self, request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})

class RegisterView(View):
    def post(self, request):
        # 1. 接收请求
        body_bytes = request.body
        # python 解释器有关 3.6 不需要 decode()
        body_dict = json.loads(body_bytes)

        # 2. 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        sms_code = body_dict.get('sms_code')
        allow = body_dict.get('allow')

        # 3. 数据验证
        #   1. 用户名 密码 确认密码 手机号 协议等参数必备
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必要参数'})

        #   2. 用户名满足规则
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误'})

        #     3. 密码满足规则
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        #     4. 确认密码必须与之前输入的密码一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        #     5. 手机号满足规则，并不能重复
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        #     6. 必须同意协议
        # allow: true
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})

        # 4. 数据入库 通过user模型进行保存 没有密码加密
        # User.objects.create(username=username, password=password, mobile=mobile)

        # 针对当前短信验证码进行验证
        redis_cli = get_redis_connection('code')
        sms_code_server = redis_cli.get(mobile)

        # 判断当前验证码是否过期
        if sms_code_server is None:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
        # 判断用户输入的短信验证码是否和redis一致
        if sms_code != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '验证码填写不正确'})
        try:
            user = User.objects.create_user(
                            username=username,
                            password=password,
                            mobile=mobile
                            )
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})

        # 5. 返回响应
        '''
        1. 当你注册完账号之后进行自动登录 *   状态保持
        2. 用户注册完账号之后跳转到登录页 用户手动登录
        '''
        request.session['user_id'] = user.id
        login(request, user)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})
