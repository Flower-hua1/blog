from django.urls import reverse
from django.http import JsonResponse

from .models import Comment
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm



# Create your views here.

#
def update_comment(request):

    referer = request.META.get("HTTP_REFERER",
                               reverse('home'))  # 获取当前的网址用于重定向,如果获取不到就直接到首页   #reverse("home")将home解析成一个可用的网址
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        # 检查通过保存数据
        comment = Comment()  # 实例化评论函数
        comment.user = comment_form.cleaned_data['user']  # 将取到的user返回
        comment.text = comment_form.cleaned_data['text']  # 将取到的text返回
        comment.content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            # 前端取到的 如果是顶级回复就写入parent(如果为空就是顶级)如果不是就写入parent里的root
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user  # 上一级对应的数据(被回复的)
        comment.save()




        # # 发送邮件通知
        # comment.send_email()

        # 将前端评论数据打包成json数据(与字典类型数据相识)  返回给前端ajax处理
        data['status'] = "SUCCESS"  # 这里只是个状态
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model  #


        if not parent is None:   # 如果parent不为空  指定回复人
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''# 如果为空认为是顶级回复
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''  # 将root_pk传回,如果没有root_pk就返回一个空
    else:
        # return render(request, "error.html", {"message": comment_form.errors, "redirect_to": referer})  # 跳转到错误页面
        data['status'] = "ERROR"
        data['message'] = list(comment_form.errors.values())[0]  # 将错误信息转换成列表取出第一个返回给前端页面显示

    return JsonResponse(data)  # 返回一个字典




# def update_comment(request):
#     referer = request.META.get('HTTP_REFERER', reverse('home'))
#     comment_form = CommentForm(request.POST, user=request.user)
#     data = {}
#
#     if comment_form.is_valid():
#         # 检查通过，保存数据
#         comment = Comment()
#         comment.user = comment_form.cleaned_data['user']
#         comment.text = comment_form.cleaned_data['text']
#         comment.content_object = comment_form.cleaned_data['content_object']
#
#         parent = comment_form.cleaned_data['parent']
#         if not parent is None:
#             comment.root = parent.root if not parent.root is None else parent
#             comment.parent = parent
#             comment.reply_to = parent.user
#         comment.save()
#
#
#
#
#
#
#         # 返回数据
#         data['status'] = 'SUCCESS'
#         data['username'] = comment.user.get_nickname_or_username()
#         data['comment_time'] = comment.comment_time.timestamp()
#         data['text'] = comment.text
#         data['content_type'] = ContentType.objects.get_for_model(comment).model
#         if not parent is None:
#             data['reply_to'] = comment.reply_to.get_nickname_or_username()
#         else:
#             data['reply_to'] = ''
#         data['pk'] = comment.pk
#         data['root_pk'] = comment.root.pk if not comment.root is None else ''
#     else:
#         #return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
#         data['status'] = 'ERROR'
#         data['message'] = list(comment_form.errors.values())[0][0]
#     return JsonResponse(data)
