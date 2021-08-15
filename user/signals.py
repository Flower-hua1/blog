from django.urls import reverse
from notifications.signals import notify
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


@receiver(post_save, sender=User)    # 监听保存的信号
def send_notifications(sender, instance, **kwargs):
    # 发送站内通知
    if kwargs['created'] == True:
        verb = '注册成功,更多精彩内容等你发现'
        url = reverse('user_info')
        notify.send(instance, recipient=instance, verb=verb, action_object=instance, url=url)
