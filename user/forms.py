from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


# Create your tests here.


class LoginForms(forms.Form):
    """创建form表单
    自动生成前端代码
    """
    # 用户名或者密码登录
    username_or_email = forms.CharField(label="用户名或邮箱",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          "placeholder": '请输入用户名或邮箱'}))  # label用来定义显示   required=True(有些东西必须填写否者提示) 为false就是不是必须的
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', "placeholder": '请输入密码'}))  # widget  定义为密码框

    def clean(self):
        """
        将用户名与密码的验证都放到这里来,功能更加分明
        :return:
        """
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)  # 将用户名 密码做对比
        if user is None:  # 判断是否为空
            if User.objects.filter(email=username_or_email).exists():  # 判断与用户对应的邮箱是否存在
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)  # 将用户名 密码做对比
                if not user is None:  # 如果用户名不为空
                    self.cleaned_data['user'] = user
                    return self.cleaned_data   # 就执行登录操作将cleaned_data传出
                else:
                    raise forms.ValidationError("用户名或密码不正确")
            # Return an 'invalid login' error message.
            raise forms.ValidationError("用户名或密码不正确")
        else:
            self.cleaned_data['user'] = user  # 将清理后的user返回
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=30, min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": '请输入用户名'}))

    email = forms.CharField(label="邮箱",
                            widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder": '请输入邮箱'}))

    verification_code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}
        )
    )

    password = forms.CharField(label="密码",
                               min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', "placeholder": '请输入密码'}))  # widget  定义为密码框

    password_again = forms.CharField(label="请再输入一次密码", min_length=6,
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control', "placeholder": '请再输入一次密码'}))  # widget  定义为密码框

    def __init__(self, *args, **kwargs):
        """
        将request传回
        :param args:
        :param kwargs:
        """
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断验证码正确与否
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']  # 获取username
        if User.objects.filter(username=username).exists():  # 如果用户名存在就返回True
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email已存在')
        return email

    def clean_password_again(self):  # clean_password_again必须使用这个名字,不用这个函数名在做两次密码对比时会报KEYerror
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入密码不一致')
        return password_again

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label="新的昵称",
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}
        )
    )

    def __init__(self, *args, **kwargs):
        """
        实例化方法
        继承CommentForm   #父类
        """
        if 'user' in kwargs:  # 判断传入的用户是否在参数里面
            self.user = kwargs.pop('user')  # 获取user
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user  # 如果是登录的就将user给cleaned_data以供我们使用
        else:
            raise forms.ValidationError('用户未登录')  # 前端不可信原则,前端验证后后端也要验证
        return self.cleaned_data

    def change_nickname_new(self):
        """
        将前端form表单POST请求返回的昵称清洗,判断
        :return: 新的昵称
        """
        nickname_new = self.cleamed_data.get('nickname_new').strip()
        if nickname_new == '':  # 判断新的昵称是否为空
            raise forms.ValidationError('新的昵称不能为空')
        return nickname_new

class BindEmailForm(forms.Form):
    """
    在这里定义的会在前端生成form表单(输入框)
    比如下面生成两个邮箱输入框和验证码输入框
    """
    email = forms.EmailField(
        label="邮箱",
        # required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}
        )
    )

    verification_code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        """
        实例化方法
        继承CommentForm   #父类
        """
        if 'request' in kwargs:  # 判断传入的用户是否在参数里面
            self.request = kwargs.pop('request')  # 获取user
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user  # 如果是登录的就将user给cleaned_data以供我们使用
            print("****1", self.request.user)
        else:
            raise forms.ValidationError('用户未登录')  # 前端不可信原则,前端验证后后端也要验证

        # 判断用户是否已经绑定了邮箱
        if self.request.user.email != '':   # 通过用户名将用户的邮箱取出看是否已经存在邮箱
            raise forms.ValidationError('你邮箱已经被绑定')
        # 判断验证码
        send_code = self.request.session.get('bind_email_code', '')  # 取验证码,如果取不到就取空  这个是发送给邮箱的验证码
        verification_code = self.cleaned_data.get('verification_code', '')
        if not(send_code != '' and send_code == verification_code):
            raise forms.ValidationError('验证码错误')
        return self.cleaned_data

    def clean_email(self):
        """
        判断邮箱是否已经被注册
        :return: email
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已存在')
        return email


    def clean_verification_code(self):
        """
        判断验证码是否为空,如果不为空的就返回 ,为空就报错,
        :return:
        """
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="旧的密码", min_length=6,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', "placeholder": '请输入旧的密码'}))  # widget  定义为密码框

    new_password = forms.CharField(label="新的密码",
                                   min_length=6,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', "placeholder": '请输入新的密码'}))  # widget  定义为密码框

    new_password_again = forms.CharField(label="请再输入一次新的密码", min_length=6,
                                         widget=forms.PasswordInput(
                                             attrs={'class': 'form-control',
                                                    "placeholder": '请再输入一次新的密码'}))  # widget  定义为密码框


    def __init__(self, *args, **kwargs):
        """
        实例化方法
        继承ChangePassWordForm   #父类
        """
        if 'user' in kwargs:  # 判断传入的用户是否在参数里面
            self.user = kwargs.pop('user')  # 获取user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        验证新的密码是否一致
        :return:
        """
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '' :
            raise forms.ValidationError('两次输入的密码不一致')

    def clean_old_password(self):
        """
        验证旧的密码输入是否正确
        :return:
        """
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码输入错误')
        return old_password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="邮箱",
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}
        )
    )

    verification_code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}
        )
    )

    new_password = forms.CharField(label="新的密码",
                                   min_length=6,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', "placeholder": '请输入新的密码'}))  # widget  定义为密码框

    def __init__(self, *args, **kwargs):
        """
        实例化方法
        继承CommentForm   #父类
        """
        if 'request' in kwargs:  # 判断传入的用户是否在参数里面
            self.request = kwargs.pop('request')  # 获取user
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()  # 将前端输入的email取出去除前后空格
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('输入的邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        code = self.request.session.get('forgot_password_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data
