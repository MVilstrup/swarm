#--- NODE ------------------------------------------------------------------------------------------

NODE = "node"

class Node(object):

    def __init__(self, html, type=NODE, **kwargs):
        """ The base class for Text, Comment and Element.
            All DOM nodes can be navigated in the same way (e.g. Node.parent, Node.children, ...)
        """
        self.type = type
        self._p = not isinstance(html, SOUP) and BeautifulSoup.BeautifulSoup(u(html), **kwargs) or html

    @property
    def _beautifulSoup(self):
        # If you must, access the BeautifulSoup object with Node._beautifulSoup.
        return self._p

    def __eq__(self, other):
        # Two Node objects containing the same BeautifulSoup object, are the same.
        return isinstance(other, Node) and hash(self._p) == hash(other._p)

    def _wrap(self, x):
        # Navigating to other nodes yields either Text, Element or None.
        if isinstance(x, BeautifulSoup.Comment):
            return Comment(x)
        if isinstance(x, BeautifulSoup.Declaration):
            return Text(x)
        if isinstance(x, BeautifulSoup.NavigableString):
            return Text(x)
        if isinstance(x, BeautifulSoup.Tag):
            return Element(x)

    @property
    def parent(self):
        return self._wrap(self._p.parent)
    @property
    def children(self):
        return hasattr(self._p, "contents") and [self._wrap(x) for x in self._p.contents] or []
    @property
    def html(self):
        return self.__unicode__()
    @property
    def source(self):
        return self.__unicode__()
    @property
    def next_sibling(self):
        return self._wrap(self._p.nextSibling)
    @property
    def previous_sibling(self):
        return self._wrap(self._p.previousSibling)

    next, prev, previous = \
        next_sibling, previous_sibling, previous_sibling

    def traverse(self, visit=lambda node: None):
        """ Executes the visit function on this node and each of its child nodes.
        """
        visit(self); [node.traverse(visit) for node in self.children]
        
    def remove(self, child):
        """ Removes the given child node (and all nested nodes).
        """
        child._p.extract()

    def __nonzero__(self):
        return True

    def __len__(self):
        return len(self.children)
    def __iter__(self):
        return iter(self.children)
    def __getitem__(self, index):
        return self.children[index]

    def __repr__(self):
        return "Node(type=%s)" % repr(self.type)
    def __str__(self):
        return bytestring(self.__unicode__())
    def __unicode__(self):
        return u(self._p)
        
    def __call__(self, *args, **kwargs):
        pass
