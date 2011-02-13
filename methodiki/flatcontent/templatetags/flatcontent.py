# -*- coding: utf-8 -*-
from django import template
from methodiki.flatcontent.models import get_flatcontent


register = template.Library()


class FlatContentNode(template.Node):
    def __init__(self, name):
        self.name = name
    def render(self, context):
        return get_flatcontent(self.name)

@register.tag
def flatcontent(parser, token):
    try:
        tag_name, flat_content_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
              "%r tag requires a single argument" % token.contents.split()[0]

    if not (flat_content_name[0] == flat_content_name[-1]
            and flat_content_name[0] in ('"', "'")):
        raise template.TemplateSyntaxError, \
              "%r tag's argument should be in quotes" % tag_name
    return FlatContentNode(flat_content_name[1:-1])
