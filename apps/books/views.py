import copy
import datetime
import math
import uuid
from functools import cmp_to_key

from django.http import FileResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import FileInfo, UserInfo, Download, Collection, Comment, DailyInfo, ReportInfo
from books.serializers import BookSerializer, BookCommentSerializer, BasicBookInfo, BookReportSerializer
from user.serializers import UserInfoSerializer

import os
import fitz


# 分页函数
class BooksPagination(PageNumberPagination):
    # 表示每页多少条数据
    page_size = 10
    # 设置每页显示数量
    page_size_query_param = 'page_size'
    # 设置显示第几页
    page_query_param = "page"
    # 每页最大显示条数
    max_page_size = 15


# 读取pdf第一页
def analysis(file_path, save_path, num):
    # 资源列表
    file_array = []
    if os.path.isdir(file_path):
        # 目录循环压入
        file_count = get_path_file(file_path)
        for v in file_count:
            file_array.append(v)
    else:
        # 单文件，单次调用
        file_array.append(file_path)

    # 判断为空情况
    if not file_array:
        print("此目录下无文件")
    # 执行解析
    file_count_num = len(file_array)
    # print("程序运行中，共计%s个文件" % file_count_num)
    for v in file_array:
        # print("文件路径：%s" % v)
        # 获取文件名称及类型
        file_name = os.path.basename(v)
        # print("文件信息：%s" % file_name)
        if '.pdf' not in file_name:
            print("此文件非PDF文件")
        #  打开PDF文件，生成一个对象
        doc = fitz.open(v)
        # 总页数
        count_page = doc.pageCount
        # print("文件共计：%s页" % count_page)
        if count_page > 1:
            page = doc[num]
            rotate = int(0)
            # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
            zoom_x = 2.0
            zoom_y = 2.0
            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pm = page.getPixmap(matrix=trans, alpha=False)
            # 保存路径
            p_1 = v.replace(file_path, save_path)
            p_2 = p_1.replace(file_name, '')
            pm.writePNG(p_2)
            print("运行完成")
        else:
            print("此文档无内容，跳出")
            continue


def get_path_file(files_path):
    data = []
    for root, dirs, files in os.walk(files_path, topdown=False):
        for name in files:
            f_p = os.path.join(root, name).replace("\\", "/")
            data.append(f_p)
    return data


# Create your views here.
# 上传书籍
class BookViews(APIView):
    # 上传书籍
    def post(self, request):
        request.data["uploader"] = request.user
        count = FileInfo.objects.count()
        count += 1
        request.data["fid"] = count
        data = request.data
        temp = {}
        for key, value in data.items():
            if value != "":
                temp[key] = value
        data = temp
        serializer = BookSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        fid = data["fid"]
        file = FileInfo.objects.get(fid=fid)
        file_path = file.file.path
        username = file.uploader
        file_photo = 'img2/' + str(username) + '/' + '{}.{}'.format(uuid.uuid4().hex[:8], "png")
        FileInfo.objects.filter(fid=fid).update(file_photo=file_photo)
        file_photo = "media/" + file_photo
        if not os.path.exists('media/img2/' + str(username) + '/'):
            os.mkdir('media/img2/' + str(username) + '/')
        analysis(file_path, file_photo, 0)
        return Response({'msg': '上传成功！'})

    # 获取用户上传书籍
    def get(self, request):
        user = request.user
        data = FileInfo.objects.filter(uploader=user.username)
        sum = len(data)
        if (len(data) > 0):
            list = []
            for i in data:
                list.append(BookSerializer(i).data)

            page_obj = BooksPagination()
            list = page_obj.paginate_queryset(list, request=request, view=self)
        else:
            list = []
        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        return Response(
            {"data": list, "pageSum": math.ceil(sum / page_size), "pagesize": page_size, "sum": sum})


# 下载书籍
class BookGetView(ModelViewSet):
    queryset = FileInfo.objects.all()
    serializer_class = BookSerializer

    @action(methods=['get', 'post'], detail=True)
    def download(self, request, pk=None, *args, **kwargs):
        user = request.user
        serializer = UserInfoSerializer(user)
        data = serializer.data
        score = data["score"]
        file_obj = self.get_object()
        file = FileInfo.objects.get(fid=pk)
        f_fee = file.f_fees
        if score >= f_fee:
            score = score - f_fee
            UserInfo.objects.filter(username=data["username"]).update(score=score)
            download_times = file.download_times + 1
            FileInfo.objects.filter(fid=pk).update(download_times=download_times)
            Download.objects.create(fid=file, userid=user)
            response = FileResponse(open(file_obj.file.path, 'rb'))
            return response
        else:
            return Response({"msg": "积分不足无法下载!"})


# 收藏书籍
class BookCollectionView(APIView):
    def get(self, request, pk=None):
        user = request.user
        file = FileInfo.objects.get(fid=pk)
        temp = Collection.objects.filter(fid=pk, userid=user.username)
        if not temp:
            collection_times = file.collection_times + 1
            FileInfo.objects.filter(fid=pk).update(collection_times=collection_times)
            Collection.objects.create(fid=file, userid=user)
            return Response({"msg": "收藏成功!"})
        else:
            return Response({"msg": "已收藏该书籍！"})


# 取消收藏书籍
class CancelCollectionView(APIView):
    def get(self, request, pk=None):
        user = request.user
        file = FileInfo.objects.get(fid=pk)
        collection_times = file.collection_times - 1
        FileInfo.objects.filter(fid=pk).update(collection_times=collection_times)
        Collection.objects.filter(fid=file, userid=user).delete()
        return Response({"msg": "取消收藏成功!"})


# 书籍封禁
class BanBookView(APIView):
    def get(self, request, pk=None):
        # 修改书籍是否封禁
        file = FileInfo.objects.get(fid=pk)
        if file.isvalid == True:
            FileInfo.objects.filter(fid=pk).update(isvalid=False)
            userid = file.uploader
            user = UserInfo.objects.get(username=userid)
            violation = user.violation + 1
            # 修改用户违规次数
            UserInfo.objects.filter(username=userid).update(violation=violation)
            return Response({"msg": "封禁成功！"})
        else:
            return Response({"msg": "该书已被封禁"})


# 书籍评论
class CommentView(APIView):

    # 获取书籍的评论
    def get(self, request, pk=None):
        comments = Comment.objects.filter(fid=pk)
        sum = len(comments)
        if len(comments) > 0:
            list = BookCommentSerializer(comments, many=True).data

            # 按照时间逆序排序（越靠近现在的先输出）
            list = sorted(list, key=lambda x: x["stime"])
            list.reverse()
            page_obj = BooksPagination()
            list = page_obj.paginate_queryset(list, request=request, view=self)
        else:
            list = []

        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)

        return Response(
            {"data": list, "pageSum": math.ceil(sum / page_size), "pagesize": page_size,
             "sum": sum})

    # 对书籍评论
    def post(self, request, pk=None):
        data = request.data
        user = request.user
        file = FileInfo.objects.get(fid=pk)
        comment_times = file.comment_times + 1
        sum_score = int(data["grade"]) + file.sum_score
        ave_score = sum_score / comment_times
        FileInfo.objects.filter(fid=pk).update(sum_score=sum_score, ave_score=ave_score, comment_times=comment_times)
        comment = Comment.objects.create(fid=file, userid=user, grade=data["grade"], evaluation=data["evaluation"])
        serializer = BookCommentSerializer(comment)
        data = serializer.data
        return Response(data)


# 每日书籍推荐排序
def daily_recommend_sort(x, y):
    if x.ave_score > y.ave_score:
        return -1
    elif x.download_times > y.download_times:
        return -1
    elif x.collection_times > y.collection_times:
        return -1
    elif x.comment_times > y.comment_times:
        return -1
    else:
        return 1
    return 0


# 获取每日推荐书籍
class DailyRecommendView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        query_set = DailyInfo.objects.all()
        # 如果数据库内为空
        if not query_set:
            books = FileInfo.objects.filter(isvalid=True)
            list = []
            for book in books:
                list.append(book)

            list = sorted(list, key=cmp_to_key(daily_recommend_sort))
            if len(list) >= 20:
                list = list[:20]
            sum = len(list)
            for i in range(len(list)):
                DailyInfo.objects.create(did=(i + 1), fid=list[i])
                list[i] = BookSerializer(list[i]).data

        # 数据库有内容
        else:
            books = DailyInfo.objects.all()
            for i in books:

                daily_time = datetime.datetime.strptime(str(i.daily_time), "%Y-%m-%d")
                now = datetime.datetime.now().strftime("%Y-%m-%d")
                now = datetime.datetime.strptime(now, "%Y-%m-%d")
                # 数据库内的内容是今天的内容
                if daily_time == now:
                    sum = len(books)
                    list = []
                    for i in books:
                        book = FileInfo.objects.get(fid=i.fid.fid)
                        list.append(BookSerializer(book).data)
                    break
                # 数据库内的内容是旧的内容
                else:
                    DailyInfo.objects.all().delete()
                    books = FileInfo.objects.filter(isvalid=True)
                    list = []
                    for book in books:
                        list.append(book)

                    list = sorted(list, key=cmp_to_key(daily_recommend_sort))
                    if len(list) >= 20:
                        list = list[:20]
                    sum = len(list)
                    for i in range(len(list)):
                        DailyInfo.objects.create(did=(i + 1), fid=list[i])
                        list[i] = BookSerializer(list[i]).data
                    break
        # 数据分页
        page_obj = BooksPagination()
        list = page_obj.paginate_queryset(list, request=request, view=self)

        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        return Response(
            {"data": list, "pageSum": math.ceil(sum / page_size), "pagesize": page_size, "sum": sum})


# 书籍举报类
class BookReportView(APIView):
    # 获取用户相关的处理完成的举报信息
    def get(self, request):
        reported = ReportInfo.objects.filter(imformer=request.user.username, isdealt=True)
        sum = len(reported)
        list = []
        for i in reported:
            result = i.get_result_display()
            serializer = BookReportSerializer(i)
            data = serializer.data
            data["result"] = result
            list.append(data)
        list = sorted(list, key=lambda x: x["Reporttime"], reverse=True)
        # 数据分页
        page_obj = BooksPagination()
        list = page_obj.paginate_queryset(list, request=request, view=self)

        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        return Response(
            {"data": list, "pageSum": math.ceil(sum / page_size), "pagesize": page_size,
             "sum": sum})

    # 提交举报信息
    def post(self, request, pk=None):
        data = request.data.copy()
        user = request.user
        fid = pk
        file = FileInfo.objects.get(fid=fid)
        reported = file.uploader
        count = ReportInfo.objects.count()
        data["reportid"] = count + 1
        data["fid"] = file.fid
        data["imformer"] = user
        data["reported"] = reported
        serializer = BookReportSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "提交成功！"})


# 查询未处理书籍举报
class UndoBookReportView(APIView):
    # 查询未处理信息
    def get(self, request):
        reports = ReportInfo.objects.filter(isdealt=False)
        sum = len(reports)
        list = []
        for i in reports:
            result = i.get_result_display()
            serializer = BookReportSerializer(i)
            data = serializer.data
            data["result"] = result
            list.append(data)
            # list.append(serializer.data)

        list = sorted(list, key=lambda x: x["Reporttime"])
        # 数据分页
        page_obj = BooksPagination()
        list = page_obj.paginate_queryset(list, request=request, view=self)

        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        return Response(
            {"data": list, "pageSum": math.ceil(sum / page_size), "pagesize": page_size, "sum": sum})

    # 处理举报信息
    def post(self, request, pk=None):
        result = request.data["result"]
        user = request.user
        ReportInfo.objects.filter(reportid=pk).update(isdealt=True, result=result, adminstrate=user)
        return Response({'msg': '处理成功！'})


# 查询已处理书籍举报
class DoneBookReportView(APIView):
    # 查询已处理信息
    def get(self, request):
        reports = ReportInfo.objects.filter(isdealt=True)
        sum = len(reports)
        list = []
        for i in reports:
            result = i.get_result_display()
            serializer = BookReportSerializer(i)
            data = serializer.data
            data["result"] = result
            list.append(data)

        list = sorted(list, key=lambda x: x["Reporttime"])
        list.reverse()
        page_obj = BooksPagination()
        list = page_obj.paginate_queryset(list, request=request, view=self)

        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        return Response(
            {"data": list, "pageSum": math.ceil(sum / page_size), "pagesize": page_size, "sum": sum})


# 获取被举报违规信息
class ReportedView(APIView):
    def get(self, request):
        user = request.user
        # print(type(user))
        reports = ReportInfo.objects.filter(reported=user.username, result=1)
        sum = len(reports)
        list = []
        for i in reports:
            result = i.get_result_display()
            serializer = BookReportSerializer(i)
            data = serializer.data
            data["result"] = result
            list.append(data)
        list = sorted(list, key=lambda x: x["Reporttime"])
        list.reverse()
        page_obj = BooksPagination()
        list = page_obj.paginate_queryset(list, request=request, view=self)

        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        return Response(
            {"data": list, "pageSum": math.ceil(sum / page_size), "pagesize": page_size, "sum": sum})


def book_recommend_sort(x, y):
    if x["ave_score"] > y["ave_score"]:
        return -1
    elif x["download_times"] > y["download_times"]:
        return -1
    elif x["collection_times"] > y["collection_times"]:
        return -1
    elif x["comment_times"] > y["comment_times"]:
        return -1
    else:
        return 1
    return 0


# # 搜索查询书籍
class SearchBookView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        queryset = FileInfo.objects.filter(isvalid=True)
        # 筛选
        screen = request.GET.get("screen", "")
        # 搜索框
        search = request.GET.get("search", "")
        # global list
        list = []

        for i in queryset:
            file = BookSerializer(i).data
            list.append(file)

        if len(screen) == 0 and len(search) == 0:
            list = sorted(list, key=cmp_to_key(book_recommend_sort))

        # 筛选
        if len(screen) != 0:
            temp = []
            for i in list:
                category = i["category"]
                if screen in category:
                    temp.append(i)
            list = sorted(temp, key=cmp_to_key(book_recommend_sort))

        # 搜索框
        if len(search) != 0:
            temp = []
            for i in list:
                if search == i["ISBN_num"] and (i not in temp):
                    temp.append(i)
                if search in i["fname"] and (i not in temp):
                    temp.append(i)
                if search in i["publisher"] and (i not in temp):
                    temp.append(i)
                if search in i["writer"] and (i not in temp):
                    temp.append(i)
                if search in i["content"] and (i not in temp):
                    temp.append(i)
            # 对查询结果计算相关度
            for i in range(len(temp)):
                if temp[i]["ISBN_num"] == search:
                    relevancy = temp[i].get("relevancy", 0) + 200
                    temp[i]["relevancy"] = relevancy
                if temp[i]["fname"] == search:
                    relevancy = temp[i].get("relevancy", 0) + 150
                    temp[i]["relevancy"] = relevancy
                elif search in temp[i]["fname"]:
                    relevancy = temp[i].get("relevancy", 0) + 80
                    temp[i]["relevancy"] = relevancy
                if temp[i]["writer"] == search:
                    relevancy = temp[i].get("relevancy", 0) + 120
                    temp[i]["relevancy"] = relevancy
                elif search in temp[i]["writer"]:
                    relevancy = temp[i].get("relevancy", 0) + 60
                    temp[i]["relevancy"] = relevancy
                if temp[i]["publisher"] == search:
                    relevancy = temp[i].get("relevancy", 0) + 80
                    temp[i]["relevancy"] = relevancy
                elif search in temp[i]["publisher"]:
                    relevancy = temp[i].get("relevancy", 0) + 50
                    temp[i]["relevancy"] = relevancy
                if temp[i]["content"] == search:
                    relevancy = temp[i].get("relevancy", 0) + 60
                    temp[i]["relevancy"] = relevancy
                elif search in temp[i]["content"]:
                    relevancy = temp[i].get("relevancy", 0) + 20
                    temp[i]["relevancy"] = relevancy
            list = temp
            list = sorted(list, key=lambda x: x["relevancy"], reverse=True)
        sum = len(list)
        # 数据分页
        page_obj = BooksPagination()
        list = page_obj.paginate_queryset(list, request=request, view=self)

        page_size = request.GET.get("page_size")
        if not page_size:
            page_size = 10
        page_size = int(page_size)
        return Response(
            {"data": list, "pageSum": math.ceil(sum / page_size), "pagesize": page_size, "sum": sum})
