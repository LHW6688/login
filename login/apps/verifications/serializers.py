from rest_framework import serializers
from django_redis import get_redis_connection
from redis import RedisError

import logging

# 日志记录器
logger = logging.getLogger('django')


class ImageCodeCheckSerializer(serializers.Serializer):
    """校验图片验证码序列化器"""
    # 定义校验的字段：字段的名字要么和模型类属性名相同，要么和传入的校验参数胡名字相同
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    # 联合校验text,需要用到image_code_id
    # attrs == validated_data
    def validate(self, attrs):

        # 读取出初步校验后的字段
        image_code_id = attrs.get('image_code_id')
        text = attrs.get('text')

        # 获取链接到redis的对象
        redis_conn = get_redis_connection('verify_codes')

        # 使用image_code_id，从redis数据库中获取服务器存储的图片验证码
        image_code_server = redis_conn.get('img_%s' % image_code_id)
        if image_code_server is None:
            raise serializers.ValidationError('无效的图片验证码')

        # 删除图片验证码，防止暴力测试
        # image_code_server : 内存中的变量，将来比较时是读取内存中的变量比较的，跟redis已经没有关系了
        # redis_conn.delete : 删除的是redis中的图片验证码
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            # 这里自己捕获异常的原因是，这是附带的业务逻辑，可实现可不实现
            # 如果要实现，出现了异常，不能妨碍主线的业务逻辑，随意自己处理，让主线业务逻辑可以正常往下执行
            logger.error(e)

        # py3中的redis读取的任何数都是bytes类型的
        image_code_server = image_code_server.decode()

        # 使用text跟服务器存储的图片验证码进行比较
        # image_code_server ：在内存中，跟redis已经没有关系了
        if text.lower() != image_code_server.lower():
            raise serializers.ValidationError('验证码输入有误')

        # 判断用户是否使用同一个手机号码在60s内频繁的发送短信
        mobile = self.context['view'].kwargs['mobile']
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            raise serializers.ValidationError('发送短信频繁')

        return attrs