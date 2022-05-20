import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import os


# Create your models here.
def file_save_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    return os.path.join("files", instance.uploader.username, filename)


def img1_save_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    return os.path.join("img1", instance.username, filename)


def img2_save_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    return os.path.join("img2", instance.uploader.username, filename)


# #建立表
class UserInfo(AbstractUser):
    username = models.CharField(max_length=20, primary_key=True, verbose_name="用户账户")
    password = models.CharField(max_length=255, null=False, verbose_name="用户密码")
    nickname = models.CharField(max_length=20, blank=True, default="个人账户", verbose_name="用户名称")

    score = models.IntegerField(default=10, verbose_name="个人积分")
    # 参数auto_now_add表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳
    login_time = models.DateField(auto_now_add=True, verbose_name="上次登录时间")
    photo = models.ImageField(upload_to=img1_save_path, default="img1/default.jpg", null=True,
                              verbose_name="个人头像")

    violation = models.IntegerField(default=0, verbose_name="违规次数")
    # 参数auto_now表示每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳
    # last_login = models.DateField(auto_now=True, verbose_name="最近登入")
    continuous = models.IntegerField(default=1, verbose_name="连续登入天数")

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'  # 在admin站点中显示的名称

    def __str__(self):
        return self.username


# token的模型
class UserToken(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, verbose_name='用户')
    token = models.CharField(max_length=255, verbose_name='用户令牌')

    class Meta:
        db_table = 'user_token'


#
# class AdministratorInfo(models.Model):
#     adm_id = models.IntegerField(primary_key=True, verbose_name="管理员账号")
#     admpwd = models.CharField(max_length=20, null=False, verbose_name="管理员密码")
#     admname = models.CharField(max_length=20, blank=True, verbose_name="管理员名称")
#     # 头像设置
#     photo = models.ImageField(upload_to='static/img1/', default="static/img1/default.jpg", verbose_name="管理员头像")
#
#     class Meta:
#         db_table = 'administrator'
#         verbose_name = '管理员表'  # 在admin站点中显示的名称


class FileInfo(models.Model):
    fid = models.IntegerField(primary_key=True, verbose_name="文件编号")
    fname = models.CharField(max_length=50, verbose_name="文件名称")
    uploader = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='userid_0', verbose_name="上传人",
                                 db_column="uploader")
    ave_score = models.DecimalField(default=0, decimal_places=2, max_digits=3, verbose_name="评分")
    comment_times = models.IntegerField(default=0, verbose_name="评论次数")
    sum_score = models.IntegerField(default=0, verbose_name="评分总数")
    download_times = models.IntegerField(default=0, verbose_name="下载次数")
    collection_times = models.IntegerField(default=0, verbose_name="收藏次数")
    f_fees = models.IntegerField(default=0, verbose_name="消耗积分")
    #  #文件地址
    file = models.FileField(upload_to=file_save_path, verbose_name="文件地址")
    publisher = models.CharField(max_length=40, verbose_name="出版社", null=True)
    writer = models.CharField(max_length=30,verbose_name="作者",default="佚名")
    ISBN_num = models.CharField(max_length=40, verbose_name="ISBN码", null=True)
    category = models.CharField(max_length=40, verbose_name="类别")
    content = models.TextField(null=True, verbose_name="简介")
    isvalid = models.BooleanField(default=True, verbose_name="是否有效")
    # 文件头像
    file_photo = models.ImageField(upload_to=img2_save_path, default='img2/default.jpg', verbose_name="书籍头像")

    class Meta:
        db_table = 'myfiles'
        verbose_name = '文件表'  # 在admin站点中显示的名称


class Download(models.Model):
    fid = models.ForeignKey(FileInfo, on_delete=models.CASCADE, related_name='fid_1', db_column="fid")
    userid = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='userid_1', db_column="userid")
    download_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="下载时间")

    class Meta:
        db_table = 'download_history'
        verbose_name = '下载历史'  # 在admin站点中显示的名称


class Collection(models.Model):
    fid = models.ForeignKey(FileInfo, on_delete=models.CASCADE, related_name='fid_2', db_column="fid")
    userid = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='userid_2', db_column="userid")
    collect_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="收藏日期")

    class Meta:
        db_table = 'collections'
        verbose_name = '收藏表'  # 在admin站点中显示的名称


class Comment(models.Model):
    fid = models.ForeignKey(FileInfo, on_delete=models.CASCADE, related_name='fid_3', db_column="fid")
    userid = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='userid_3', db_column="userid")
    stime = models.DateTimeField(default=datetime.datetime.now,verbose_name="评论时间")
    grade = models.IntegerField(default=5, verbose_name="个人评分")
    evaluation = models.CharField(max_length=255, verbose_name="个人评价")

    class Meta:
        db_table = 'comments'
        verbose_name = '评论表'  # 在admin站点中显示的名称


class ReportInfo(models.Model):
    reportid = models.AutoField(primary_key=True, verbose_name="举报编号", db_column="reportid")
    fid = models.ForeignKey(FileInfo, on_delete=models.CASCADE, related_name='fid_4', db_column="fid")
    imformer = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='imformer_id', db_column="imformer")
    reported = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='reported_id', db_column="reported")
    Reporttime = models.DateTimeField(default=datetime.datetime.now, verbose_name="举报时间")
    details = models.TextField()
    range = models.CharField(max_length=20, verbose_name="违规范围")
    isdealt = models.BooleanField(default=False, verbose_name="是否处理1")
    adminstrate = models.IntegerField(null=True, verbose_name="处理人1")

    class Meta:
        db_table = 'report'
        verbose_name = '举报表'  # 在admin站点中显示的名称


# class ComplaintInfo(models.Model):
#     complaint_id = models.AutoField( primary_key=True, verbose_name="申诉编号",db_column="complaint_id")
#     report_id = models.ForeignKey(ReportInfo, on_delete=models.CASCADE, related_name='report1',db_column="report_id")
#     case = models.TextField(verbose_name="原因")
#     isdealt = models.BooleanField(default=False, verbose_name="是否处理2")
#     adminstrate = models.IntegerField(null=True, verbose_name="处理人2")
#
#     class Meta:
#         db_table = 'complaint'
#         verbose_name = '申诉表'  # 在admin站点中显示的名称


class DailyInfo(models.Model):
    did = models.IntegerField(primary_key=True, verbose_name="日常推荐id")
    fid = models.ForeignKey(FileInfo, on_delete=models.CASCADE, related_name='fid_5', db_column="daily_fid")
    daily_time = models.DateField(auto_now=True, verbose_name="推荐时间")
    # daily_time = models.DateTimeField(auto_now=True, verbose_name="推荐时间")

    class Meta:
        db_table = 'daily_recommend'
        verbose_name = "每日推荐"
