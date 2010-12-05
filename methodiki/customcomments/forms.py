# -*- coding: utf-8 -*-
import re

from django.contrib.comments.forms import CommentForm
from django.core.validators import URLValidator


class CustomCommentForm(CommentForm):
    def __init__(self, target_object, data=None, initial=None):
        super(CustomCommentForm, self).__init__(target_object, data, initial)
        class_str = "span-7 append-8 last input"
        self.fields['name'].widget.attrs['class'] = class_str
        self.fields['email'].widget.attrs['class'] = class_str
        self.fields['url'].widget.attrs['class'] = class_str
        self.fields['comment'].widget.attrs['class'] = "span-10 append-8 " \
                                                       "last input"
        # Replace standard URL validation to support local URLs,
        # e.g. without TLDs.
        self.fields['url'].validators = [IntranetURLValidator()]


class IntranetURLValidator(URLValidator):
    """ URL validation that support local URLs, e.g. without TLDs. """

    def __init__(self):
        super(IntranetURLValidator, self).__init__()

        # FIXME: For now, don't assume URLs are reachable
        self.verify_exists = False

        # Pattern that only matches web URLs — http, https, and things like
        # "www.example.com"
        # See http://daringfireball.net/2010/07/improved_regex_for_matching_urls
        self.regex = re.compile(ur"(?i)\b((?:https?://|www\d{0,3}[.]|" \
                                ur"[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|" \
                                ur"\(([^\s()<>]+|" \
                                ur"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|" \
                                ur"(\([^\s()<>]+\)))*\)|" \
                                ur"[^\s`!()\[\]{};:'" \
                                ur'"' \
                                ur".,<>?«»“”‘’]))")
