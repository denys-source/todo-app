from django import template


register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs) -> str:
    params = request.GET.copy()
    for param, value in kwargs.items():
        if value:
            params[param] = value
        else:
            params.pop(param, 0)
    return params.urlencode()
