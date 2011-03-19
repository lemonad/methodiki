# -*- coding: utf-8 -*-
from django import template
from markdown import markdown

from ..models import get_flatcontent


register = template.Library()


@register.simple_tag
def flatcontent(name):
    content = get_flatcontent(name)
    return markdown(content, safe_mode=True)
