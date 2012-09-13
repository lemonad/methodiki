from django.conf import settings
from django.contrib.comments.moderation import CommentModerator
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _


class EmailOwner(CommentModerator):
    """
    Subclass of ``CommentModerator`` which emails the "owner" of an
    object whenever a new comment is posted on it.

    Assumes that the 'owner' is specified by a ``ForeignKey`` named
    'user'; edit that if your field is named something else.

    """
    email_notification = True

    def email(self, comment, content_object, request):
        name = comment.user_name
        site_name = Site.objects.get_current().name
        site_domain = Site.objects.get_current().domain

        if comment.user and comment.user.get_profile().name:
            name = comment.user.get_profile().name

        subject = _('%(site_name)s: %(name)s has posted a comment on '
                    'your method "%(title)s"') % \
                  {'site_name': site_name,
                   'name': name,
                   'title': content_object.title}

        t = loader.get_template('comments/comment_email_owner.txt')
        c = Context({'comment': comment,
                     'comment_permalink': "http://" + site_domain +
                                          comment.get_absolute_url("#c%(id)s"),
                     'content_object': content_object,
                     'site_name': site_name})
        text_message = t.render(c)

        t = loader.get_template('comments/comment_email_owner.html')
        c = Context({'comment': comment,
                     'comment_permalink': "http://" + site_domain +
                                          comment.get_absolute_url("#c%(id)s"),
                     'content_object': content_object,
                     'site_name': site_name})
        html_message = t.render(c)

        msg = EmailMultiAlternatives(subject,
                                     text_message,
                                     settings.DEFAULT_FROM_EMAIL,
                                     [content_object.user.email])
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=True)

        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
        #           [content_object.user.email], fail_silently=True)
