import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def json_dumps(obj):
    return mark_safe(json.dumps(obj))


register.filter('json_dumps', json_dumps)
