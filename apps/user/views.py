import math
import os
import uuid

from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.settings import api_settings

from books.views import BooksPagination
from user.serializers import UserRegSerializer, UserInfoSerializer, UserPhotoSerializer
from user.models import UserToken, UserInfo, Download, FileInfo, Collection
from books.serializers import BasicBookInfo
import datetime


# 注册视图
class RegisterViews(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserRegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # drf-jwt生成
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 创建token
        UserToken.objects.create(user=user, token=token)

        # 数据信息返回给前端
        dic = serializer.validated_data
        dic['token'] = token
        del dic['password']
        headers = {'Authorization': 'Bearer %s' % token}
        return Response(dic, status=201, headers=headers)


# 用户基本信息
class UserInfoViews(APIView):
    # 获取个人信息
    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        data = serializer.data
        return Response(data, status=201)

    # 修改昵称
    def put(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        data = serializer.data
        if request.data.get("nickname"):
            data["nickname"] = request.data["nickname"]
        serializer = UserInfoSerializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data)


# 用户头像
class UserPhotoView(APIView):
    def get(self, request):
        serializer = UserPhotoSerializer(request.user)
        data = serializer.data
        return Response(data, status=201)

    def post(self, request):
        photo = request.FILES['file']
        username = UserInfoSerializer(request.user).data["username"]
        file_name = 'img1/' + str(username) + '/' + '{}.{}'.format(uuid.uuid4().hex[:8], photo.name.split('.')[-1])
        UserInfo.objects.filter(username=username).update(photo=file_name)
        if not os.path.exists('media/img1/' + str(username) + '/'):
            os.mkdir('media/img1/' + str(username) + '/')
        with open('media/' + file_name, 'wb+') as f:
            f.write(photo.read())

        return Response({"msg": "ok"})


# 更新连续登录天数和积分
class CommonUpdateUserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        data = serializer.data

        # 获取上次登录时间和今天时间
        last_longin_time = data['login_time']
        last_longin_time = datetime.datetime.strptime(last_longin_time, "%Y-%m-%d")
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        now = datetime.datetime.strptime(now, "%Y-%m-%d")
        day = (now - last_longin_time).days
        if day == 1:
            data["continuous"] += 1
            data["score"] += 1
            if data["continuous"] % 30 == 0:
                data["score"] += 9
            elif data["continuous"] % 7 == 0:
                data["score"] += 4

            data["login_time"] = now.strftime("%Y-%m-%d")
            serializer = UserInfoSerializer(user, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        elif day > 1:
            data["continuous"] = 1
            data["login_time"] = now.strftime("%Y-%m-%d")
            serializer = UserInfoSerializer(user, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(data, status=201)


# 获取下载记录
class GetDownloadsView(APIView):
    def get(self, request):
        user = request.user
        files_id = Download.objects.filter(userid=user)
        sum = len(files_id)
        data = []
        for i in files_id:
            if (BasicBookInfo(i.fid).data in data):
                continue
            temp_data = BasicBookInfo(i.fid).data
            temp_data["download_time"] = i.download_time
            data.append(temp_data)
        data = sorted(data, key=lambda x: x["download_time"])
        data.reverse()
        page_obj = BooksPagination()
        data = page_obj.paginate_queryset(data, request=request, view=self)

        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        return Response(
            {"data": data, "pageSum": math.ceil(sum / page_size), "pagesize": page_size, "sum": sum})


# 获取收藏记录
class CollectionView(APIView):
    def get(self, request):
        user = request.user
        files_id = Collection.objects.filter(userid=user)
        sum = len(files_id)
        data = []
        for i in files_id:
            temp_data = BasicBookInfo(i.fid).data
            temp_data["collect_time"] = i.collect_time
            data.append(temp_data)
        data = sorted(data, key=lambda x: x["collect_time"])
        data.reverse()

        page_obj = BooksPagination()
        data = page_obj.paginate_queryset(data, request=request, view=self)

        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        return Response(
            {"data": data, "pageSum": math.ceil(sum / page_size), "pagesize": page_size, "sum": sum})
