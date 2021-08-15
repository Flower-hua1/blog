from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User



# Create your models here.
class LikeCount(models.Model):
    """
    创建点赞总数模型
    要对应博客(类型,具体博客)
    """
    # 对应具体博客
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 创建记录点赞数量的字段
    liked_num = models.IntegerField(default=0)
    class Meta:
        verbose_name = '点赞统计'
        verbose_name_plural = verbose_name

class LikeRecord(models.Model):
    """
    记录点赞的数据
    """

    # 具体被点赞的博客
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 被点赞的用户与点赞时间
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '点赞记录'
        verbose_name_plural = verbose_name