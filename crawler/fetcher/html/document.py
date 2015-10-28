from element import Element


class Document(Element):
    def __init__(self, html, **kwargs):
        """ Document is the top-level element in the Document Object Model.
            It contains nested Element, Text and Comment nodes.
        """
        # Aliases for BeautifulSoup optional parameters:
        kwargs["selfClosingTags"
               ] = kwargs.pop("self_closing", kwargs.get("selfClosingTags"))
        Node.__init__(self, u(html).strip(), type=DOCUMENT, **kwargs)

    @property
    def declaration(self):
        """ Yields the <!doctype> declaration, as a TEXT Node or None.
        """
        for child in self.children:
            if isinstance(child._p, BeautifulSoup.Declaration):
                return child

    @property
    def head(self):
        return self._wrap(self._p.head)

    @property
    def body(self):
        return self._wrap(self._p.body)

    @property
    def tagname(self):
        return None

    tag = tagname

    def __repr__(self):
        return "Document()"
