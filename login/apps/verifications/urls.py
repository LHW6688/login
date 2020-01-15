# -*- coding: utf-8 -*-
'''
PROJECT_NAME：login 
FILE:urls 
USERNAME: 李宏伟
DATE:2020/1/12 
TIME:下午12:47 
PRODUCT_NAME:PyCharm 
'''
from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'image_codes/', views.ImageCodeView.as_view()),

]