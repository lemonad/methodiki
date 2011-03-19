# -*- coding: utf-8 -*-
import re

from django.contrib.comments.forms import CommentForm
from django.core.validators import URLValidator
from django.forms import BooleanField

from models import CustomComment


class CustomCommentForm(CommentForm):
    lift_method = BooleanField(required=False, initial=True)

    def __init__(self, target_object, data=None, initial=None):
        super(CustomCommentForm, self).__init__(target_object, data, initial)

        # Replace standard URL validation to support local URLs,
        # e.g. without TLDs.
        self.fields['url'].validators = [IntranetURLValidator()]

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return CustomComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CustomCommentForm, self).get_comment_create_data()
        data['lift_method'] = self.cleaned_data['lift_method']
        return data


class IntranetURLValidator(URLValidator):
    """ URL validation that support local URLs, e.g. without TLDs. """

    def __init__(self):
        super(IntranetURLValidator, self).__init__()

        # FIXME: For now, don't assume URLs are reachable
        self.verify_exists = False

        # Pattern that only matches web URLs — http, https, and things like
        # "www.example.com"
        # cf.:
        # http://daringfireball.net/2010/07/improved_regex_for_matching_urls
        self.regex = re.compile(ur"(?i)\b((?:https?://|www\d{0,3}[.]|" \
                                ur"[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|" \
                                ur"\(([^\s()<>]+|" \
                                ur"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|" \
                                ur"(\([^\s()<>]+\)))*\)|" \
                                ur"[^\s`!()\[\]{};:'" \
                                ur'"' \
                                ur".,<>?«»“”‘’]))")
