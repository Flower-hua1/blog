import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
# Create your models here.





class Comment(models.Model):
    """
    创建评论模型,
    关联的是任何类型的字段,不是某一篇博客
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  #关联一个类型字段
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name="评论内容")  #评论字段不限字数
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")    #评论时间  创建评论的时候自己添加
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, verbose_name="用户")
    #评论人,作为外键关联进来,删除时不要做任何事情(不影响数据)

    # 回复评论功能 #

    # 记录某一条评论是从那一条评论开始的
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)  # 如果不想要方向关系(+)
    # 创建外键对应评论
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)  # self  指向自己   null=True 最顶级为空(类似树形结构的顶端允许他为空)
    # 对应回复的对象  related_name反向解析名称    user   找到相关的回复
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)  # 在获取对象时与上面的user有冲突  然后创建了(related_name)

    def __str__(self):
        return self.text  # 显示文本

    def get_user(self):
        return self.user

    def get_url(self):
        return self.content_object.get_url()

    class Meta:
        ordering = ['comment_time']   # 倒序排序
        verbose_name = '评论'
        verbose_name_plural = verbose_name


# class Reply(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)   # 关联外键到Reply
