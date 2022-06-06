from django.urls import path
from user import views
from books.views import BookViews
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

urlpatterns = [
    path('login/', obtain_jwt_token),  # 登录
    path('register/', views.RegisterViews.as_view()),  # 注册
    path('userinfo/', views.UserInfoViews.as_view()),  # 获取用户基本信息和修改用户昵称
    path('userphoto/',views.UserPhotoView.as_view()), # 获取和修改用户头像
    path('commonupdate/', views.CommonUpdateUserView.as_view()),  # 更新连续登录和积分信息
    path('downloads/',views.GetDownloadsView.as_view()), # 获取下载历史
    path('collections/',views.CollectionView.as_view()), # 获取收藏记录
    path('posthistory/', BookViews.as_view()),  # 获取用户上传书籍
]

# routers = routers.DefaultRouter()
# routers.register(r'userphoto', views.UserPhotoView)
# urlpatterns += routers.urls
