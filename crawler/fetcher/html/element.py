from node import Node

class Element(Node):

    def __init__(self, html):
        """ Element represents an element or tag in the HTML source code.
            For example: "<b>hello</b>" is a "b"-Element containing a child Text("hello").
        """
        Node.__init__(self, html, type=ELEMENT)

    @property
    def tagname(self):
        return self._p.name

    tag = tagName = tagname

    @property
    def attributes(self):
        if "_attributes" not in self.__dict__:
            self._attributes = self._p._getAttrMap()
        return self._attributes

    attr = attrs = attributes

    @property
    def id(self):
        return self.attributes.get("id")

    @property
    def content(self):
        """ Yields the element content as a unicode string.
        """
        return u"".join([u(x) for x in self._p.contents])

    string = content

    @property
    def source(self):
        """ Yields the HTML source as a unicode string (tag + content).
        """
        return u(self._p)

    html = src = source

    def get_elements_by_tagname(self, v):
        """ Returns a list of nested Elements with the given tag name.
            The tag name can include a class (e.g. div.header) or an id (e.g. div#content).
        """
        if isinstance(v, basestring) and "#" in v:
            v1, v2 = v.split("#")
            v1 = v1 in ("*","") or v1.lower()
            return [Element(x) for x in self._p.findAll(v1, id=v2)]
        if isinstance(v, basestring) and "." in v:
            v1, v2 = v.split(".")
            v1 = v1 in ("*","") or v1.lower()
            return [Element(x) for x in self._p.findAll(v1, v2)]
        return [Element(x) for x in self._p.findAll(v in ("*","") or v.lower())]

    by_tag = getElementsByTagname = get_elements_by_tagname

    def get_element_by_id(self, v):
        """ Returns the first nested Element with the given id attribute value.
        """
        return ([Element(x) for x in self._p.findAll(id=v, limit=1) or []]+[None])[0]

    by_id = getElementById = get_element_by_id

    def get_elements_by_classname(self, v):
        """ Returns a list of nested Elements with the given class attribute value.
        """
        return [Element(x) for x in (self._p.findAll(True, v))]

    by_class = getElementsByClassname = get_elements_by_classname

    def get_elements_by_attribute(self, **kwargs):
        """ Returns a list of nested Elements with the given attribute value.
        """
        return [Element(x) for x in (self._p.findAll(True, attrs=kwargs))]

    by_attribute = by_attr = getElementsByAttribute = get_elements_by_attribute

    def __call__(self, selector):
        """ Returns a list of nested Elements that match the given CSS selector.
            For example: Element("div#main p.comment a:first-child") matches:
        """
        return SelectorChain(selector).search(self)

    def __getattr__(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        if k in self.attributes:
            return self.attributes[k]
        raise AttributeError("'Element' object has no attribute '%s'" % k)

    def __contains__(self, v):
        if isinstance(v, Element):
            v = v.content
        return v in self.content

    def __repr__(self):
        return "Element(tag=%s)" % repr(self.tagname)
