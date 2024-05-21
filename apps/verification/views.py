from random import random,randint

from django.shortcuts import render
from django.views import View
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse
from django.http import JsonResponse
from libs.yuntongxun.sms import CCP

# Create your views here.


class ImageCodeView(View):
    def get(self, request, uuid):
        text,image=captcha.captcha.generate_captcha()
        redis_cil = get_redis_connection('code')
        redis_cil.setex(uuid,100,text)
        return HttpResponse(image,content_type='image/jpeg')
class SmsCodeView(View):
    def get(self, request, mobile):
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        if not all([image_code,uuid]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        redis_cil = get_redis_connection('code')
        redis_image_code = redis_cil.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code':400,'mrrmsg':'图片验证码过期'})
        if redis_image_code.decode() .lower() != image_code.lower():
            return JsonResponse({'code':400,'errmsg':'图片验证码错误'})


        sms_code = '%04d' % randint(0,9999)
        print(sms_code)

        redis_cil.setex(mobile,300,sms_code)
        CCP().send_template_sms(mobile,[sms_code,5],1)
        return JsonResponse({'code':0,'errmsg':'ok'})





