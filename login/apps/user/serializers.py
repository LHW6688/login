# -*- coding: utf-8 -*-
'''
PROJECT_NAME：login 
FILE:serializers 
USERNAME: 李宏伟
DATE:2020/1/15 
TIME:上午10:13 
PRODUCT_NAME:PyCharm 
'''
import re

from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
	"""
	创建用户序列化器
	"""
	password2 = serializers.CharField(label="确认密码", write_only=True)
	allow = serializers.CharField(label="同意协议", write_only=True)
	
	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'password2', 'mobile', 'allow',)
	
		extra_kwargs = {
			"username": {
				"min_length": 5,
				"max_length": 20,
				"error_messages": {
					"min_length": "仅允许5-20个字符的用户名",
					"max_length": "仅允许5-20个字符的用户名",
				}
			},
			"password": {
				"write_only": True,
				"min_length": 8,
				"max_length": 20,
				"error_messages": {
					"min_length": "仅允许8-20个字符的密码",
					"max_length": "仅允许8-20个字符的密码",
				}
			}
		}
	def validate_mobile(self, value):
		"""验证手机号码"""
		if not re.match(r"1[1-9]\d{9}", value):
			raise serializers.ValidationError("手机号码格式错误")
		return value
	
	def validate_allow(self, value):
		if value != 'true':
			raise serializers.ValidationError('请同意用户协议')
		return value
	
	def validate(self, attrs):
		# 判断两次密码
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError('两次密码不一致')
		return attrs
	
	def create(self, validate_data):
		"""创建用户"""
		# 移除数据库模型中不存在的属性
		del validate_data['password2']
		del validate_data['allow']
		user = super(CreateUserSerializer, self).create(validate_data)
		# 调用Django的认证系统加密密码
		user.set_password(validate_data["password"])
		user.save()
		# 生成token
		from rest_framework_jwt.settings import api_settings
		
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		
		payload = jwt_payload_handler(user)
		token = jwt_encode_handler(payload)
		user.token = token
		return user
