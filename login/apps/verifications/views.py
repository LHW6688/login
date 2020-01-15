# -*- coding: utf-8 -*-
import base64

from django.shortcuts import render
from rest_framework.views import APIView
from django_redis import get_redis_connection
from django.http import HttpResponse
import random
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from . import constants
from login.libs.captcha.captcha import captcha
from . import serializers

# Create your views here.


import logging

# 日志记录器
logger = logging.getLogger('django')


# url(r'image_codes/', views.ImageCodeView.as_view()),
class ImageCodeView(APIView):
    """图片验证码"""

    def get(self, request):
        """提供图片验证码"""
        image_code_id = request.query_params.get('image_code_id')
        # 生成图片验证码内容和图片
        text, image = captcha.generate_captcha()
        logger.info(text)

        # 将图片验证码内容保存到redis
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.set('img_%s' % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        image = base64.b64encode(image)

        # 将图片验证码的图片响应给用户(image/jpg)
        return Response(data={'data': image}, content_type='image/jpg')