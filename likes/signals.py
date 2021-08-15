
from notifications.signals import notify
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import LikeRecord


@receiver(post_save, sender=LikeRecord)    # 监听保存的信号
def send_notifications(sender, instance, **kwargs):
    # 发送站内通知
    if instance.content_type.model == "blog":     # 如果被点赞的是博客
        blog = instance.content_object
        verb = "{0} 点赞了你的博客《{1}》".format(instance.user.get_username(), blog.title)
        url = blog.get_url()
    elif instance.content_type.model == "comment":  # 如果被点赞的是评论
        comment = instance.content_object
        verb = "{0} 点赞了你的评论《{1}》".format(instance.user.get_username(), strip_tags(comment.text))
        url = comment.get_url()
    recipient = instance.content_object.get_user()
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)



