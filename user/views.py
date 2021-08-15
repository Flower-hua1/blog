import string
import random
import time
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from urllib.request import urlopen
from urllib.parse import urlencode, parse_qs
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForms, RegForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from .models import Profile
# Create your views here.


# def login_by_qq(request):
#     code = request.GET['code']  # 前端的返回数据    (code)
#     state = request.GET['state']     # 返回的是在登录里自己填写的(lxdblog)
#
#     if state != settings.QQ_STATE:    # 判断是不是一致
#         raise Exception("state error")
#
#     # 获取Access_token
#     params = {
#         'grant_type': 'authorization_code',
#         'client_id': settings.QQ_APP_ID,
#         'client_secret': settings.QQ_APP_KEY,
#         'code': code,
#         'redirect_uri': settings.QQ_REDIRECT_URL,   # qq重定向URL
#
#     }
#     response = urlopen('https://graph.qq.com/oauth2.0/token?' + urlencode(params))
#     data = response.read().decode('utf8')  #将返回的的数据转换成utf-8的格式
#     access_token = parse_qs(data)['access_token'][0]   # 获取access_token   提取token


    # import pdb    # 断点
    # pdb.set_trace()

    # # 获取openid
    # response = urlopen('https://graph.qq.com/oauth2.0/me?access_token=' + access_token)      # 向网址发送请求
    # data = response.read().decode('utf8')   #将返回的的数据转换成utf-8的格式
    # openid = json.loads(data[10:-4])['openid']
# 判断openid是否有关联的用户
#     if OAuthRelationship.objects.filter(openid=openid, oauth_type=0).exists():
#         relationship = OAuthRelationship.objects.get(openid=openid, oauth_type=0)
#         auth.login(request, relationship.user)
#         return redirect(reverse('home'))
#     else:
#         request.session['openid'] = openid
#
#         # 获取QQ用户信息
#         params = {
#             'access_token': access_token,
#             'oauth_consumer_key': settings.QQ_APP_ID,
#             'openid': openid,
#         }
#         response = urlopen('https://graph.qq.com/user/get_user_info?' + urlencode(params))
#         data = json.loads(response.read().decode('utf8'))
#         params = {
#             'nickname': data['nickname'],
#             'avatar': data['figureurl_qq_1'],
#         }
#         return redirect(reverse('bind_qq') + '?' + urlencode(params))


def login(request):
    """
    :param request:
    :return:
    username = request.POST.get("username")  # 使用post方法取出用户名
    password = request.POST.get("password")
    user = auth.authenticate(request, username=username, password=password)   # 将用户名 密码做对比
    referer = request.META.get("HTTP_REFERER", reverse('home'))  # 获取当前的网址用于重定向,如果获取不到就直接到首页   #reverse("home")将home解析成一个可用的网址

    if user is not None:   # 判断是否为空
        auth.login(request, user)    # 不为空就登录
        # Redirect to a success page.
        return redirect(referer)   # 重定向  跳转到首页
    else:
        # Return an 'invalid login' error message.
        return render(request, "error.html", {"message": "用户名或密码不正确", "redirect_to": referer})  # 跳转到错误页面
    """

    if request.method == "POST":  # 判断请求是否为POST的请求
        login_form = LoginForms(request.POST)  # 实例化登录函数  将提交的数据返回
        if login_form.is_valid():  # 判断是否有效
            users = login_form.cleaned_data['user']  # 将forms.py里清理过的用户名取出
            auth.login(request, users)  # 不为空就登录
            # print(auth.login(request, users))# 不为空就登录)
            # Redirect to a success page.
            return redirect(request.GET.get('from', reverse("home")))  # 重定向  通过前端页面返回的信息重定向定位到登录前的链接,如果没有就回到首页
    else:
        login_form = LoginForms()
    # 这里是django  form的使用   所以无论登录与否都要需要(自动生成前端页面代码)
    content = {}
    content["login_form"] = login_form  # 前端页面返回的登录信息(用户名 密码)包括前端代码
    return render(request, "user/login.html", content)

def login_for_modal(request):
    login_form = LoginForms(request.POST)
    data = {}
    if login_form.is_valid():  # 判断是否有效
        users = login_form.cleaned_data['user']  # 将forms.py里清理过的用户名取出
        auth.login(request, users)  # 不为空就登录
        data['status'] = "SUCCESS"
    else:
        data['status'] = "ERROR"
    return JsonResponse(data)

def register(request):
    if request.method == "POST":  # 判断请求是否为POST的请求
        reg_form = RegForm(request.POST, request=request)  # 实例化登录函数  将提交的数据返回
        if reg_form.is_valid():  # 是否验证通过
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 删除session
            del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse("home")))  # 重定向  通过前端页面返回的信息重定向定位到登录前的链接,如果没有就回到首页
    else:
        reg_form = RegForm()
    # 这里是django  form的使用   所以无论登录与否都要需要(自动生成前端页面代码)
    content = {}
    content["reg_form"] = reg_form  # 前端页面返回的登录信息(用户名 密码)包括前端代码
    return render(request, "user/register.html", content)

def logout(request):
    """
    登出
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect(request.GET.get('from', reverse("home")))  # 重定向  通过前端页面返回的信息重定向定位到登录前的链接,如果没有就回到首页

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def change_nickname(request):
    redirect_to = request.GET.get("form", reverse('home'))  # 获取当前的网址用于重定向
    if request.method == "POST":     # 判断请求方式
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():    # 判断提交的内容是否为空
            nickname = form.cleaned_data['nickname_new']   # 将清洗后的新昵称取出
            profile, created = Profile.objects.get_or_create(user=request.user)  # 取出或创建
            profile.nickname = nickname  # 更改昵称
            profile.save()
            return redirect(redirect_to)
    else:   # get请求
        form = ChangeNicknameForm()
    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def bind_email(request):
    redirect_to = request.GET.get("form", reverse('home'))  # 获取当前的网址用于重定向
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 删除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    if request.method == "POST":  # 判断请求方式
        form = BindEmailForm(request.POST, request=request)
        # 实现绑定功能
        if form.is_valid():
            email = form.cleaned_data['email']   # 将验证判断清洗后的email取出
            request.user.email = email  # 写入email
            request.user.save()
            return redirect(redirect_to)
    else:  # get请求
        form = BindEmailForm()
    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    data = {}
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    if email != "":
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))  # 生成字母加数字的四位验证码
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        # 判断发送时长是否大于30秒
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        # 发送邮件
        else:
            request.session[send_for] = code      # 从前端页面将验证码是从绑定页面返回的还是注册页面返回的统一
            request.session['send_code_time'] = now
        send_mail(
            '绑定邮箱',
            '验证码：%s' % code,
            '2972352405@qq.com',
            [email],
            fail_silently=False,  # 是否忽略错误
        )
        data['status'] = "SUCCESS"
    else:
        data['status'] = "ERROR"
    return JsonResponse(data)

def change_password(request):
    redirect_to = reverse('home')
    if request.method == "POST":  # 判断请求方式
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():  # 判断提交的内容是否为空
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)   # 登出
            return redirect(redirect_to)

    else:  # get请求
        form = ChangePasswordForm()
    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def forgot_password(request):
    redirect_to = reverse('home')
    if request.method == "POST":  # 判断请求方式
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():  # 判断提交的内容是否为空
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:  # get请求
        form = ForgotPasswordForm()
    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)
