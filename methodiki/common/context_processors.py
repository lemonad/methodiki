# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site


def site(request):
    """
    Return information about current site.

    No need for caching:
    http://docs.djangoproject.com/en/dev/ref/contrib/sites/
                                            #caching-the-current-site-object

    """
    return {"site_name": Site.objects.get_current().name}
