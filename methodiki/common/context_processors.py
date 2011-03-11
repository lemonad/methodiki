# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site


def site(request):
    """
    Return information about current site.

    No need for caching:
    http://docs.djangoproject.com/en/dev/ref/contrib/sites/
                                            #caching-the-current-site-object

    """
    current_site = Site.objects.get_current()
    return {"site_name": current_site.name,
            "site_domain": current_site.domain}
