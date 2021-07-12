from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord

# Create your views here.



def ErrorResponse(code, message):
    """
    点赞失败显示处理
    :param code:
    :param message:
    :return: json数据
    """
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(liked_num):
    """
    点赞成功显示处理
    :param liked_num:
    :return: json数据  (包含点赞数量)
    """
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def like_change(request):
    """

    :param request:
    :return:
    """
    # 获取数据  用户博客类型 具体博客
    user = request.user
    if not user.is_authenticated:  # 如果没有登录
        return ErrorResponse(400, 'you were not login')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')

    # 处理数据
    if request.GET.get('is_like') == 'true':
        # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type,
                                                                object_id=object_id, user=user)
        if created:  # 如果用户信息存在
            # 未点赞过，进行点赞
            like_count, _ = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)  # 将点赞数量取出,进行加一
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(402, 'you were liked')
    else:
        # 要取消点赞

        if LikeRecord.objects.filter(content_type=content_type,
                                     object_id=object_id, user=user).exists():  # 查询对应信息是否存在 exists存在
            # 有点赞过，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)  # 将信息提出
            like_record.delete()     # 信息删除
            # 点赞总数减1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type,
                                                                  object_id=object_id)   # 按对应的信息查找出点赞的数量
            # created  返回的是False  True
            if not created:    # 如果创建的点赞信息不存在  就删除点赞数量

                if like_count.liked_num <= 0:
                    like_count.liked_num = 0
                else:
                    like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            # 没有点赞过，不能取消
            return ErrorResponse(403, 'you were not liked')
