import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
# Create your models here.


class SendEmail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)
    def run(self):
        send_mail(self.subject,
                   '',
                  settings.EMAIL_HOST_USER,
                  [self.email],
                  fail_silently=False,
                  html_message=self.text,
                  )  # 是否忽略错误


class Comment(models.Model):
    """
    创建评论模型,
    关联的是任何类型的字段,不是某一篇博客
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  #关联一个类型字段
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()  #评论字段不限字数
    comment_time = models.DateTimeField(auto_now_add=True)    #评论时间  创建评论的时候自己添加
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    #评论人,作为外键关联进来,删除时不要做任何事情(不影响数据)

    # 回复评论功能 #

    # 记录某一条评论是从那一条评论开始的
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)  # 如果不想要方向关系(+)
    # 创建外键对应评论
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)  # self  指向自己   null=True 最顶级为空(类似树形结构的顶端允许他为空)
    # 对应回复的对象  related_name反向解析名称    user   找到相关的回复
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)  # 在获取对象时与上面的user有冲突  然后创建了(related_name)

    def send_email(self):
        # 发送邮件通知
        if self.parent is None:
            # 评论我的博客
            subject = "有人评论你的博客"
            email = self.content_object.get_email()

        else:
            # 回复评论
            subject = "有人回复你的博客"
            email = self.reply_to.email

        if email != '':
            text = "%s\n<a href='%s'>%s</a>" % (self.text, self.content_object.get_url(), '查看')  # 评抡内容加具体评论网址()
            send_mail(subject, text, settings.EMAIL_HOST_USER, [email], fail_silently=False, )  # 是否忽略错误
            send_email = SendEmail(subject, text, email,)
            send_email.start()
    def __str__(self):
        return self.text  # 显示文本

    class Meta:
        ordering = ['comment_time']   # 倒序排序

# class Reply(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)   # 关联外键到Reply
