from django.test import TestCase

# Create your tests here.


def clean(self):
    if self.request.user.is_authenticated:
        self.cleaned_data['user'] = self.request.user
        print("****1", self.request.user)
    else:
        raise forms.ValidationError('用户尚未登录')
    if self.request.user.email != '':
        raise forms.ValidationError('你已经绑定邮箱')
    code = self.request.session.get('bind_email_code', '')
    verification_code = self.cleaned_data.get('verification_code', '')
    if not (code != '' and code == verification_code):
        raise forms.ValidationError('验证码不正确')
    return self.cleaned_data

def clean(self):
    if self.request.user.is_authenticated:
        self.cleaned_data['user'] = self.request.user
        print("****1", self.request.user)
    else:
        raise forms.ValidationError('用户未登录')
    if self.request.user.email != '':
        raise forms.ValidationError('你邮箱已经被绑定')
    code = self.request.session.get('bind_email_code', '')
    verification_code = self.cleaned_data.get('verification_code', '')
    if not(code == '' and send_code != verification_code):
        raise forms.ValidationError('验证码错误')
    return self.cleaned_data
