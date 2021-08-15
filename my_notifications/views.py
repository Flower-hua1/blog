from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from notifications.models import Notification



def my_notifications(request):
    context = {}
    return render(request, 'my_notifications/my_notifications.html', context)

def my_notification(request,my_notification_pk):
    my_notification = get_object_or_404(Notification, pk=my_notification_pk)  # 获取当前消息通知的id
    my_notification.unread = False  # 将获取的通知设置为已读
    my_notification.save()    # 保存设置
    return redirect(my_notification.data['url'])   # 将url返回

def delete_my_read_notifications(request):
    notifications = request.user.notifications.read()  # 所有已读消息取出
    notifications.delete()    #删除已读消息
    return redirect(reverse('my_notifications'))   # 重定向到消息页面



