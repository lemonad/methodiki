# -*- coding: utf-8 -*-
"""
Autolinks URLs as anchors and images.

Examples:
>>> import markdown
>>> md = markdown.Markdown(extensions=['autolink'])

>>> md.convert("www.example.com/")
u'<p><a href="http://www.example.com/">www.example.com/</a></p>'

>>> md.convert("http://example.com/")
u'<p><a href="http://example.com/">http://example.com/</a></p>'

>>> md.convert("bla bla http://example.com bla bla")
u'<p>bla bla <a href="http://example.com">http://example.com</a> bla bla</p>'

>>> md.convert("(http://www.example.com/subdir/?query=abc#hash)")
u'<p>(<a href="http://www.example.com/subdir/?query=abc#hash">http://www.example.com/subdir/?query=abc#hash</a>)</p>'

>>> md.convert("http://example.com/image.jpg")
u'<p><img src="http://example.com/image.jpg" /></p>'

>>> md.convert("www.example.com/image.GIF")
u'<p><img src="http://www.example.com/image.GIF" /></p>'

Not matching:
>>> md.convert("example.com")
u'<p>example.com</p>'

Matching but not considered an image to autolink as an <img>
>>> md.convert("http://example.com/image.tiff")
u'<p><a href="http://example.com/image.tiff">http://example.com/image.tiff</a></p>'

"""
import re

import markdown


# Pattern that only matches web URLs — http, https, and things like
# "www.example.com"
# See http://daringfireball.net/2010/07/improved_regex_for_matching_urls
AUTOLINK_RE = ur"(?i)\b((?:https?://|www\d{0,3}[.]|" \
              ur"[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|" \
              ur"\(([^\s()<>]+|" \
              ur"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|" \
              ur"(\([^\s()<>]+\)))*\)|" \
              ur"[^\s`!()\[\]{};:'" \
              ur'"' \
              ur".,<>?«»“”‘’]))"


class AutolinkPattern(markdown.inlinepatterns.Pattern):
    """ Return an <a> or <img> given non-markdown URLs
        (`http://example/com`, `www.example.com` or
        `http://example.com/image.gif`).

    """
    def handleMatch(self, m):
        url = m.group(2)

        text = url

        # If no http(s) prefix, assume http
        if re.match("www", url, re.I):
            url = "http://" + url

        if re.search(r"\.(jpg|jpeg|gif|png)$", url, flags=re.I):
            el = markdown.etree.Element("img")
            el.set("src", url)
            el.set("class", "autolink")
        else:
            el = markdown.etree.Element("a")
            el.set("href", url)
            el.set("class", "autolink")
            el.text = markdown.AtomicString(text)
        return el


class AutolinkExtension(markdown.Extension):
    """ Autolink Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Replace autolink with AutolinkPattern. """
        md.inlinePatterns["autolink"] = AutolinkPattern(AUTOLINK_RE, md)


def makeExtension(configs=None):
    return AutolinkExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
