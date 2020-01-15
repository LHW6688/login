# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import CreateUserSerializer


class UsernameCountView(APIView):
	'''验证用户名唯一'''
	
	def get(self, request):
		username = request.query_params.get('username')
		count = User.objects.filter(username=username).count()
		data = {
			'username': username,
			'count': count
		}
		return Response(data={'data': data})


class MobileCountView(APIView):
	'''验证手机号唯一'''
	
	def get(self, request):
		mobile = request.query_params.get('mobile')
		count = User.objects.filter(username=mobile).count()
		data = {
			'mobile': mobile,
			'count': count
		}
		return Response(data={'data': data})


class UserView(APIView):
	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		password2 = request.data.get('password2')
		mobile = request.data.get('mobile')
		allow = request.data.get('allow')
		data = dict({'username': username,
					 'password': password,
					 'password2': password2,
					 'mobile': mobile,
					 'allow': allow,
					 })
		serializer_class = CreateUserSerializer(data=data)
		if serializer_class.is_valid():
			user = serializer_class.create(data)
			return Response(data={'id': user.id, 'username': user.username, 'token': user.token})
		else:
			error_messages = serializer_class.errors
			for key,value in error_messages.items():
				message = value[0]
			return Response(data={'data': message})
