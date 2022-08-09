from django import template
from django.http import HttpRequest, QueryDict
from django.utils.safestring import SafeString

register = template.Library()


@register.simple_tag()
def get_params_as_str(request: HttpRequest) -> str:
    result: str = ''
    params: QueryDict = request.GET or request.POST
    for param in params:
        result += f"{param}={params[param]}&"
    return result


@register.simple_tag()
def get_params_as_list(request: HttpRequest) -> list:
    params: QueryDict = request.GET or request.POST
    return params.lists()


@register.simple_tag()
def get_params_as_dict(request: HttpRequest) -> QueryDict:
    return request.GET or request.POST


def _exclude_params_for_str(params: str, params_for_exclude: list) -> str:
    if not params:
        return ''

    result: str = ''
    for param in params.strip('&').split('&'):
        param, value = param.split('=')
        if param not in params_for_exclude:
            result += f'&{param}={value}'
    return result


def _exclude_params_for_list(params: list, params_for_exclude: list) -> list:
    if not params:
        return []

    for param in params_for_exclude:
        if param in params:
            params.remove(param)

    return params


def _exclude_params_for_dict(params: dict, params_for_exclude: list) -> dict:
    if not params:
        return dict()

    for param in params_for_exclude:
        if param in params.keys():
            params.pop(param)

    return params


@register.filter()
def exclude_params(params: str | list | dict, params_for_exclude: str | list) -> str | list | dict:
    """
    :param params: parameters of request in str, list or dict
    :param params_for_exclude: str or list of params names, that should be excluded
    str example: "page search-target etc"
    :return: fixed params
    """
    handlers: dict = {
        str: _exclude_params_for_str,
        list: _exclude_params_for_list,
        dict: _exclude_params_for_dict,
    }

    if isinstance(params, SafeString):
        params = params.split()

    return handlers[type(params)](params, params_for_exclude)
