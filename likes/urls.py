from django.urls import path
from . import views


urlpatterns = [
    path('like_change', views.like_change, name="like_change"),      #form  表单返回的评论url
]