from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^username/$', views.UsernameCountView.as_view()),		#验证用户名唯一
	url(r'^mobile/$', views.MobileCountView.as_view()),		#验证手机号唯一
	url(r'^users/$', views.UserView.as_view()),		#注册
]
