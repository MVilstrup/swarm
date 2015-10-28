class Link(object):

    def __init__(self, url, text="", relation="", referrer=""):
        """ A hyperlink parsed from a HTML document, in the form:
            <a href="url"", title="text", rel="relation">xxx</a>.
        """
        self.url, self.text, self.relation, self.referrer = \
            u(url), u(text), u(relation), u(referrer),

    @property
    def description(self):
        return self.text

    def __repr__(self):
        return "Link(url=%s)" % repr(self.url)

    # Used for sorting in Crawler.links:
    def __eq__(self, link):
        return self.url == link.url
    def __ne__(self, link):
        return self.url != link.url
    def __lt__(self, link):
        return self.url < link.url
    def __gt__(self, link):
        return self.url > link.url
