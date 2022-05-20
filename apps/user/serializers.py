from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from user.models import Download
from books.serializers import BasicBookInfo

User = get_user_model()


# 用户注册序列化器
class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="用户账户", required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="用户已经存在")])
    password = serializers.CharField(style={'input_type': 'password'}, label="用户密码", required=True, write_only=True)
    nickname = serializers.CharField(default="个人账户", label="用户名称", required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        nickname = attrs.get('nickname')
        if not username.isdigit():
            raise serializers.ValidationError("账号含有非数字！")

        if len(username) < 6 or len(username) > 16:
            raise serializers.ValidationError("账号小于六位数或大于十六位数！")
        if len(password) < 6 or len(password) > 20:
            raise serializers.ValidationError("密码小于六位数或大于二十位数！")
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError('密码应由字母与数字组成！')
        if len(nickname) > 20:
            raise serializers.ValidationError('昵称长度大于二十！')
        return attrs

    def create(self, validated_data):
        user = User(**validated_data)
        # 对明文密码进行加密
        user.set_password(user.password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "password", "nickname")


# 用户基本信息序列化器
class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField(label="用户账户", required=True)
    nickname = serializers.CharField(max_length=20, label="用户名称")

    score = serializers.IntegerField(label="个人积分")
    # photo = serializers.ImageField(label="个人头像")
    violation = serializers.IntegerField(label="违规次数")
    continuous = serializers.IntegerField(label="连续登入天数")
    login_time = serializers.DateField(label="上次登录时间")

    # 更新用户数据
    def update(self, instance, validated_data):
        instance.continuous = validated_data.get('continuous', instance.continuous)
        instance.score = validated_data.get('score', instance.score)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.violation = validated_data.get('violation', instance.violation)
        instance.login_time = validated_data.get('login_time', instance.login_time)
        # instance.photo = validated_data("photo", instance.photo)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("username", "nickname", "score", "violation", "continuous", "login_time")


class UserPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField(label="个人头像")

    class Meta:
        model = User
        fields = ("photo",)

# # 下载历史序列化器
# class DownloadHistorySerializer(serializers.Serializer):
#     # fid = serializers.IntegerField(label="书籍id", required=True)
#     fid = BasicBookInfo(many=True)
#     userid = serializers.CharField(label="用户id")
#     download_time = serializers.DateField(label="下载时间")
#
#     class Meta:
#         model = Download
#         fields = '__all__'
