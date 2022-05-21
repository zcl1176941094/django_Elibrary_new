import datetime
from functools import cmp_to_key

from django.http import FileResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import FileInfo, UserInfo, Download, Collection, Comment, DailyInfo, ReportInfo
from books.serializers import BookSerializer, BookCommentSerializer, BasicBookInfo, BookReportSerializer
from user.serializers import UserInfoSerializer


# Create your views here.
# 上传书籍
class BookViews(APIView):

    def post(self, request):
        # userSerializer = UserInfoSerializer(request.user)
        # username = userSerializer.data["username"]
        request.data["uploader"] = request.user
        # request.data["uploader"] = username
        count = FileInfo.objects.count()
        count += 1
        request.data["fid"] = count
        # print(request.data)
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': '上传成功！'})


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
        collection_times = file.collection_times + 1
        FileInfo.objects.filter(fid=pk).update(collection_times=collection_times)
        Collection.objects.create(fid=file, userid=user)
        return Response({"msg": "收藏成功!"})


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
        FileInfo.objects.filter(fid=pk).update(isvalid=False)
        file = FileInfo.objects.get(fid=pk)
        userid = file.uploader
        user = UserInfo.objects.get(username=userid)
        violation = user.violation + 1
        # 修改用户违规次数
        UserInfo.objects.filter(username=userid).update(violation=violation)

        return Response({"msg": "封禁成功！"})


# 书籍评论
class CommentView(APIView):
    # 获取书籍的评论
    def get(self, request, pk=None):
        comments = Comment.objects.filter(fid=pk)
        list = []
        for comment in comments:
            serializer = BookCommentSerializer(comment)
            data = serializer.data
            list.append(data)
        # 按照时间逆序排序（越靠近现在的先输出）
        list = sorted(list, key=lambda x: x["stime"])
        list.reverse()
        return Response(list)

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
            for i in range(len(list)):
                DailyInfo.objects.create(did=(i + 1), fid=list[i])
                list[i] = BasicBookInfo(list[i]).data
        # 数据库有内容
        else:
            books = DailyInfo.objects.all()
            for i in books:

                daily_time = datetime.datetime.strptime(str(i.daily_time), "%Y-%m-%d")
                now = datetime.datetime.now().strftime("%Y-%m-%d")
                now = datetime.datetime.strptime(now, "%Y-%m-%d")
                # 数据库内的内容是今天的内容
                if daily_time == now:

                    list = []
                    for i in books:
                        book = FileInfo.objects.get(fid=i.fid.fid)
                        list.append(BasicBookInfo(book).data)
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
                    for i in range(len(list)):
                        DailyInfo.objects.create(did=(i + 1), fid=list[i])
                        list[i] = BasicBookInfo(list[i]).data
                    break

        return Response(list)


# 书籍举报类
class BookReportView(APIView):
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
        return Response(serializer.data)


# 查询未处理书籍举报
class UndoBookReportView(APIView):
    # 查询未处理信息
    def get(self, request):
        reports = ReportInfo.objects.filter(isdealt=False)
        list = []
        for i in reports:
            list.append(BookReportSerializer(i).data)
        list = sorted(list, key=lambda x: x["Reporttime"])
        return Response(list)

    # 处理举报信息
    def post(self, request, pk=None):

        result = request.data["result"]
        print(ReportInfo.objects.get(reportid=pk))
        ReportInfo.objects.filter(reportid=pk).update(isdealt=True,result=result)

        return Response({'msg':'处理成功！'})


# 查询已处理书籍举报
class DoneBookReportView(APIView):
    # 查询已处理信息
    def get(self, request):
        reports = ReportInfo.objects.filter(isdealt=True)
        list = []
        for i in reports:
            list.append(BookReportSerializer(i).data)
        list = sorted(list, key=lambda x: x["Reporttime"])
        list.reverse()
        return Response(list)
