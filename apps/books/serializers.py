from user.models import FileInfo, DailyInfo, UserInfo, Comment

from rest_framework import serializers


# 书籍信息
class BookSerializer(serializers.Serializer):
    fid = serializers.IntegerField(label="文件编号")
    fname = serializers.CharField(max_length=50, label="文件名称")
    writer = serializers.CharField(max_length=30,label="作者")
    # uploader = serializers.IntegerField(label="上传人")
    uploader = serializers.PrimaryKeyRelatedField(label="上传人", queryset=UserInfo.objects.all())
    ave_score = serializers.DecimalField(max_digits=5, decimal_places=2, default=0, label="评分")
    comment_times = serializers.IntegerField(default=0, label="评论次数")
    download_times = serializers.IntegerField(default=0, label="下载次数")
    collection_times = serializers.IntegerField(default=0, label="收藏次数")
    f_fees = serializers.IntegerField(default=0, label="消耗积分")
    #  #文件地址
    file = serializers.FileField(label="文件地址")
    publisher = serializers.CharField(max_length=40, label="出版社")
    ISBN_num = serializers.CharField(max_length=40, label="ISBN码")
    category = serializers.CharField(max_length=40, label="类别")
    content = serializers.CharField(label="简介")
    isvalid = serializers.BooleanField(default=True, label="是否有效")
    # 文件头像
    file_photo = serializers.ImageField(label="书籍头像")

    class Meta:
        model = FileInfo
        fields = '__all__'

    def create(self, validated_data):
        # print(validated_data)
        file = FileInfo(**validated_data)
        file.save()
        return file


# 书籍基本信息
class BasicBookInfo(serializers.Serializer):
    fid = serializers.IntegerField(label="文件编号")
    fname = serializers.CharField(max_length=50, label="文件名称")
    writer = serializers.CharField(max_length=30, label="作者")
    ave_score = serializers.DecimalField(max_digits=5, decimal_places=2, default=0, label="评分")
    file = serializers.FileField(label="文件地址")
    publisher = serializers.CharField(max_length=40, label="出版社")
    ISBN_num = serializers.CharField(max_length=40, label="ISBN码")
    category = serializers.CharField(max_length=40, label="类别")
    content = serializers.CharField(label="简介")
    isvalid = serializers.BooleanField(default=True, label="是否有效")
    f_fees = serializers.IntegerField(default=0, label="消耗积分")
    # 文件头像
    file_photo = serializers.ImageField(label="书籍头像")

    class Meta:
        model = FileInfo
        fields = (
            "fid", "fname", "avg_score", "file", "publisher", "ISBN_num", "category", "content", "isvalid",
            "file_photo", "f_fees")


class BookCommentSerializer(serializers.Serializer):
    fid = serializers.PrimaryKeyRelatedField(label="书籍id", queryset=FileInfo.objects.all())
    userid = serializers.PrimaryKeyRelatedField(label="用户id", queryset=UserInfo.objects.all())
    stime = serializers.DateTimeField(label="评论时间")
    grade = serializers.IntegerField(default=5, label="个人评分")
    evaluation = serializers.CharField(max_length=255, label="个人评价")

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment.save()
        return comment
