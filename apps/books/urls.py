from django.urls import path, re_path
from books import views
from rest_framework import routers

urlpatterns = [
    path('books/', views.BookViews.as_view()),  # post上传书籍
    re_path(r'cancel_collection/(?P<pk>[^/.]+)/', views.CancelCollectionView.as_view()),  # 取消收藏书籍
    re_path(r'ban_book/(?P<pk>[^/.]+)/', views.BanBookView.as_view()),  # 书籍封禁
    re_path(r'collection/(?P<pk>[^/.]+)/', views.BookCollectionView.as_view()),  # 用户收藏书籍
    re_path(r'comment/(?P<pk>[^/.]+)/', views.CommentView.as_view()),  # 书籍评论
    path('daily_book/', views.DailyRecommendView.as_view()),  # 获取每日推荐书籍
    re_path('report/(?P<pk>[^/.]+)/', views.BookReportView.as_view()),  # 提交书籍举报信息
    path('search_undo_msg/', views.UndoBookReportView.as_view()),  # 获取未处理信息
    path('search_msg/', views.DoneBookReportView.as_view()),  # 获取已处理信息
]

# 获取书籍信息
routers = routers.DefaultRouter()
routers.register(r'book_get', views.BookGetView)
urlpatterns += routers.urls