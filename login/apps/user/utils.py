# -*- coding: utf-8 -*-
import re

from django.contrib.auth.backends import ModelBackend

from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
	"""
	自定义jwt认证成功返回数据
	"""
	return {
		'token': token,
		'user_id': user.id,
		'username': user.username
	}


def get_user_by_account(account):
	"""
	根据用户传入的账号，查询user
	:param account: 有可能是手机号，有可能是用户名
	:return: 查询到，返回user;反之，None
	"""
	try:
		if re.match(r'^1[3-9]\d{9}$', account):
			user = User.objects.get(mobile=account)
		else:
			user = User.objects.get(username=account)
	except User.DoesNotExist:
		return None
	else:
		return user


class UsernameMobileAuthBackend(ModelBackend):
	"""自定义用户认证的后端"""
	
	def authenticate(self, request, username=None, password=None, **kwargs):
		"""
		最终认证用户的方法
		:param request: 本次登录请求
		:param username: 本次登录用户名(手机号或者用户名)
		:param password: 本次登录用户密码
		:param kwargs: 其他参数
		:return: 如果认证成功（该用户确实是本网站的用户）返回user；反之，返回None
		"""
		# 查询出用户对象
		user = get_user_by_account(username)
		
		if user and user.check_password(password):
			return user
