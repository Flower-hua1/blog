from django.db import models


from django.contrib.auth.models import User
# Create your models here.


# class OAuthRelationship(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     openid = models.CharField(max_length=128)
#
#     OAUTH_TYPE_CHOICES = (
#             (0, "QQ"),
#             (1, "WeChat"),
#             (2, "Sina"),
#             (3, "Github"),
#         )
#     oauth_type = models.IntegerField(default=0, choices=OAUTH_TYPE_CHOICES)
#
#     def __str__(self):
#         return "<OAuthRelationship: %s>" % self.user.username



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')   # 一对一字段
    nickname = models.CharField(max_length=20, verbose_name='昵称')   # 昵称

    def __str__(self):
        return "<Profile: %s for %s>" % (self.user.username, self.nickname)
    class Meta:
        verbose_name = '用户描述'
        verbose_name_plural = verbose_name

def get_nickname(self):

    if Profile.objects.filter(user=self).exists():  # 判断是否有昵称的存在
        profile = Profile.objects.get(user=self)  # 取出返回
        return profile.nickname
    else:
        return ''

def get_nickname_or_username(self):
    """
    有昵称就返回昵称没昵称就返回用户名
    """
    if Profile.objects.filter(user=self).exists():  # 判断是否有昵称的存在
        profile = Profile.objects.get(user=self)  # 取出返回
        return profile.nickname
    else:
        return self.username


def has_nickname(self):

    return Profile.objects.filter(user=self).exists()  # 判断是否有昵称的存在

User.get_nickname = get_nickname    # 动态绑定
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username    # 动态绑定

