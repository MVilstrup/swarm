from node import Node

TEXT = "text"


class Text(Node):
    """ Text represents a chunk of text without formatting in a HTML document.
        For example: "the <b>cat</b>" is parsed to
        [Text("the"), Element("cat")].
    """

    def __init__(self, string):
        Node.__init__(self, string, type=TEXT)

    def __repr__(self):
        return "Text(%s)" % repr(self._p)
