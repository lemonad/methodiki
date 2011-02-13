# -*- coding: utf-8 -*-
import datetime
import pytz

from django import template
from django.conf import settings
from pytz import timezone


register = template.Library()

@register.filter(name='html5_time')
def html5_time(value):
    """
    Filter for formatting a Django datetime as a html5 compatible
    time string.

    """
    if value and isinstance(value, datetime.datetime):
        tz = timezone(settings.TIME_ZONE)
        # As Django datetimes are not time zone aware, make them so by
        # assigning the TIME_ZONE setting.
        tz_dt = value.replace(tzinfo=tz)
        tz_str = tz_dt.strftime('%Y-%m-%dT%H:%M:%S%z')

        # HTML5 needs time offset with a colon separating hours and minutes
        return tz_str[:-2] + ':' + tz_str[-2:]
    else:
        return value

