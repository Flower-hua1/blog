from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()

@register.simple_tag()
def get_comment_count(obj):
    """
    根据条件筛选出博客的评论数量
    :param obj:
    :return: 评论数量
    """
    content_type = ContentType.objects.get_for_model(obj)  # 获取博客类型
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()  # 筛选出来统计评论数

@register.simple_tag()
def get_comment_form(obj):
    """
    将被回复的评论取出
    :param obj:
    :return:
    """
    content_type = ContentType.objects.get_for_model(obj)  # 获取博客类型
    form = CommentForm(  # (reply_comment_id) 如果是顶级评论将评论ID设置为0
        initial={'content_type': content_type.model, 'object_id': obj.pk,
                 'reply_comment_id': 0})  # 实例化form里面的CommentForm方法,通过博客类型以及ID对应到博客
    return form

@register.simple_tag()
def get_comment_list(obj):
    """
    返回评论列表
    :param obj:
    :return:
    """
    content_type = ContentType.objects.get_for_model(obj)  # 获取博客类型
    comments = Comment.objects.filter(content_type=content_type,
                                      object_id=obj.pk, parent=None)  # 通过博客类型以及博客的主键值筛选得出这条博客的评论
    return comments.order_by('-comment_time')