from .forms import LoginForms

def login_modal_form(request):
    """
    这里将LoginForms实例化  类似全局都可以使用
    :param request:
    :return:
    """
    return{'login_modal_form':LoginForms()}