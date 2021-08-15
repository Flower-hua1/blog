import threading
from notifications.signals import notify
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from .models import Comment
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Comment)    # 监听保存的信号
def send_notifications(sender, instance,**kwargs):
    # 发送站内通知

    if instance.reply_to is None:
        # 如果 reply_to为空就是评论的消息
        recipient = instance.content_object.get_user()   # 博客的用户
        if instance.content_type.model == "blog":   # 判断是否是博客的评论
            blog = instance.content_object
            verb = "{0} 评论了你的文章《{1}》".format(instance.user.get_username(), blog.title)    # 当前用户
            url = blog.get_url() + "#comment_" + str(instance.pk)   # 因为blog models里面有get_url方法,这里可以直接反向获取链接
        else:
            raise Exception('unkown comment object type')
    else:
        # 不为空就是回复评论的消息
        recipient = instance.reply_to   # 被评论的用户
        parent = strip_tags(instance.parent.text)  # 被回复的评论的内容  (strip_tags   去掉前端的标签)
        verb = "{0} 评论了你的评论《{1}》".format(instance.user.get_username(), parent)
        url = instance.content_object.get_url() \
              + "#comment_" + str(instance.pk)  # 因为comment models里面有get_url方法,这里可以直接反向获取链接(加上贫PK直接定位到具体评论位置)
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)



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


@receiver(post_save, sender=Comment)  # 监听保存的信号
def send_email(sender, instance, **kwargs):
    # 发送邮件通知
    if instance.parent is None:
        # 评论我的博客
        subject = "有人评论你的博客"
        email = instance.content_object.get_email()

    else:
        # 回复评论
        subject = "有人回复你的博客"
        email = instance.reply_to.email

    if email != '':
        text = "%s\n<a href='%s'>%s</a>" % (instance.text, instance.content_object.get_url(), '查看')  # 评抡内容加具体评论网址()
        send_mail(subject, text, settings.EMAIL_HOST_USER, [email], fail_silently=False, )  # 是否忽略错误
        send_email = SendEmail(subject, text, email,)
        send_email.start()