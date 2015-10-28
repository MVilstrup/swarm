class Error(Exception):
    """ Base class for pattern.web errors.
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args)
        self.src = kwargs.pop("src", None)
        self.url = kwargs.pop("url", None)

    @property
    def headers(self):
        return dict(self.src.headers.items())


class URLError(Error):
    pass  # URL contains errors (e.g. a missing t in htp://).


class URLTimeout(URLError):
    pass  # URL takes to long to load.


class HTTPError(URLError):
    pass  # URL causes an error on the contacted server.


class HTTP301Redirect(HTTPError):
    pass  # Too many redirects.


    # The site may be trying to set a cookie and waiting for you to return it,
    # or taking other measures to discern a browser from a script.
    # For specific purposes you should build your own urllib2.HTTPRedirectHandler
    # and pass it to urllib2.build_opener() in URL.open()
class HTTP400BadRequest(HTTPError):
    pass  # URL contains an invalid request.


class HTTP401Authentication(HTTPError):
    pass  # URL requires a login and password.


class HTTP403Forbidden(HTTPError):
    pass  # URL is not accessible (user-agent?)


class HTTP404NotFound(HTTPError):
    pass  # URL doesn't exist on the internet.


class HTTP420Error(HTTPError):
    pass  # Used by Twitter for rate limiting.


class HTTP429TooMayRequests(HTTPError):
    pass  # Used by Twitter for rate limiting.


class HTTP500InternalServerError(HTTPError):
    pass  # Generic server error.


class HTTP503ServiceUnavailable(HTTPError):
    pass  # Used by Bing for rate limiting.
