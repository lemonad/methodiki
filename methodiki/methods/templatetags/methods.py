# -*- coding: utf-8 -*-
import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import strip_tags
from django.utils.text import truncate_words


register = template.Library()


@stringfilter
def abstract(value):
    """ Tries to extract the first paragraph of an html string. """

    match = re.search(r"<p>(.+?)</p>", value, re.IGNORECASE | re.DOTALL)
    if match:
        return strip_tags(match.group(1))
    else:
        return truncate_words(strip_tags(value), 40, "...")

register.filter('abstract', abstract)
