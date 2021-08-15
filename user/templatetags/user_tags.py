from django import template
from urllib.parse import urlencode
from django.conf import settings

register = template.Library()

# @register.simple_tag()
# def get_login_qq_tag():
#     """
#     根据条件筛选出博客的评论数量
#     :param obj:
#     :return: 评论数量
#     """
#     params = {
#         'response_type': 'code',
#         'client_id': settings.QQ_APP_ID,
#         'redirect_uri': settings.QQ_REDIRECT_URL,
#         'state': settings.QQ_STATE,
#     }
#     return "https://openapi.baidu.com/oauth/2.0/authorize"+urlencode(params)



















