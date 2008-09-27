import re

from django import template
from account.models import OtherServiceInfo

register = template.Library()

class OtherServiceNode(template.Node):
    def __init__(self, user, key, asvar):
        self.user = user
        self.key = key
        self.asvar = asvar
    
    def render(self, context):
        user = self.user.resolve(context)
        key = self.key
        try:
            value = OtherServiceInfo.objects.get(user=user, key=key).value
        except OtherServiceInfo.DoesNotExist:
            value = ''
                    
        if self.asvar:
            context[self.asvar] = value
            return ''
        else:
            return value


@register.tag
def other_service(parser, token):
    bits = token.contents.split(' ')
    if len(bits) == 3: # {% other_service user key %}
        user = parser.compile_filter(bits[1])
        key = bits[2]
        asvar = None
    elif len(bits) == 5: # {% other_service user key as var %}
        if bits[3] != "as":
            raise template.TemplateSyntaxError("3rd argument to %s should be 'as'" % bits[0])
        user = parser.compile_filter(bits[1])
        key = bits[2]
        asvar = bits[4]
    else:
        raise template.TemplateSyntaxError("wrong number of arguments to %s" % bits[0])
    
    return OtherServiceNode(user, key, asvar)