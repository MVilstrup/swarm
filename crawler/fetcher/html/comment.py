from text import Text
from node import Node

COMMENT = "comment"


class Comment(Text):
    """ Comment represents a comment in the HTML source code.
        For example: "<!-- comment -->".
    """

    def __init__(self, string):
        Node.__init__(self, string, type=COMMENT)

    def __repr__(self):
        return "Comment(%s)" % repr(self._p)
