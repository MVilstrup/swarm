# HTTP request method.
GET = "get"  # Data is encoded in the URL.
POST = "post"  # Data is encoded in the message body.

# URL parts.
# protocol://username:password@domain:port/path/page?query_string#anchor
PROTOCOL, USERNAME, PASSWORD, DOMAIN, PORT, PATH, PAGE, QUERY, ANCHOR = \
    "protocol", "username", "password", "domain", "port", "path", "page", "query", "anchor"

# MIME type.
MIMETYPE_WEBPAGE = ["text/html"]
MIMETYPE_STYLESHEET = ["text/css"]
MIMETYPE_PLAINTEXT = ["text/plain"]
MIMETYPE_PDF = ["application/pdf"]
MIMETYPE_NEWSFEED = ["application/rss+xml", "application/atom+xml"]
MIMETYPE_IMAGE = ["image/gif", "image/jpeg", "image/png", "image/tiff"]
MIMETYPE_AUDIO = ["audio/mpeg", "audio/mp4", "audio/x-aiff", "audio/x-wav"]
MIMETYPE_VIDEO = ["video/mpeg", "video/mp4", "video/avi", "video/quicktime",
                  "video/x-flv"]
MIMETYPE_ARCHIVE = ["application/x-stuffit", "application/x-tar",
                    "application/zip"]
MIMETYPE_SCRIPT = ["application/javascript", "application/ecmascript"]


class URL(object):
    def __init__(self, string=u"", method=GET, query={}, **kwargs):
        """ URL object with the individual parts available as attributes:
            For protocol://username:password@domain:port/path/page?query_string#anchor:
            - URL.protocol: http, https, ftp, ...
            - URL.username: username for restricted domains.
            - URL.password: password for restricted domains.
            - URL.domain  : the domain name, e.g. nodebox.net.
            - URL.port    : the server port to connect to.
            - URL.path    : the server path of folders, as a list, e.g. ['news', '2010']
            - URL.page    : the page name, e.g. page.html.
            - URL.query   : the query string as a dictionary of (name, value)-items.
            - URL.anchor  : the page anchor.
            If method is POST, the query string is sent with HTTP POST.
        """
        self.__dict__[
            "method"
        ] = method  # Use __dict__ directly since __setattr__ is overridden.
        self.__dict__["_string"] = u(string)
        self.__dict__["_parts"] = None
        self.__dict__["_headers"] = None
        self.__dict__["_redirect"] = None
        if isinstance(string, URL):
            self.__dict__["method"] = string.method
            self.query.update(string.query)
        if len(query) > 0:
            # Requires that we parse the string first (see URL.__setattr__).
            self.query.update(query)
        if len(kwargs) > 0:
            # Requires that we parse the string first (see URL.__setattr__).
            self.parts.update(kwargs)

    def _parse(self):
        """ Parses all the parts of the URL string to a dictionary.
            URL format: protocal://username:password@domain:port/path/page?querystring#anchor
            For example: http://user:pass@example.com:992/animal/bird?species=seagull&q#wings
            This is a cached method that is only invoked when necessary, and only once.
        """
        p = urlparse.urlsplit(self._string)
        P = {
            PROTOCOL: p[0],  # http
            USERNAME: u"",  # user
            PASSWORD: u"",  # pass
            DOMAIN: p[1],  # example.com
            PORT: u"",  # 992
            PATH: p[2],  # [animal]
            PAGE: u"",  # bird
            QUERY: urldecode(p[3]),  # {"species": "seagull", "q": None}
            ANCHOR: p[4]  # wings
        }
        # Split the username and password from the domain.
        if "@" in P[DOMAIN]:
            P[USERNAME], \
            P[PASSWORD] = (p[1].split("@")[0].split(":") + [u""])[:2]
            P[DOMAIN] = p[1].split("@")[1]
        # Split the port number from the domain.
        if ":" in P[DOMAIN]:
            P[DOMAIN], \
            P[PORT] = P[DOMAIN].split(":")
            P[PORT] = P[PORT].isdigit() and int(P[PORT]) or P[PORT]
        # Split the base page from the path.
        if "/" in P[PATH]:
            P[PAGE] = p[2].split("/")[-1]
            P[PATH] = p[2][:len(p[2]) - len(P[PAGE])].strip("/").split("/")
            P[PATH] = filter(lambda v: v != "", P[PATH])
        else:
            P[PAGE] = p[2].strip("/")
            P[PATH] = []
        self.__dict__["_parts"] = P

    # URL.string yields unicode(URL) by joining the different parts,
    # if the URL parts have been modified.
    def _get_string(self):
        return unicode(self)

    def _set_string(self, v):
        self.__dict__["_string"] = u(v)
        self.__dict__["_parts"] = None

    string = property(_get_string, _set_string)

    @property
    def parts(self):
        """ Yields a dictionary with the URL parts.
        """
        if not self._parts: self._parse()
        return self._parts

    @property
    def querystring(self):
        """ Yields the URL querystring: "www.example.com?page=1" => "page=1"
        """
        s = self.parts[QUERY].items()
        s = dict((bytestring(k), bytestring(v if v is not None else ""))
                 for k, v in s)
        s = urllib.urlencode(s)
        return s

    def __getattr__(self, k):
        if k in self.__dict__: return self.__dict__[k]
        if k in self.parts: return self.__dict__["_parts"][k]
        raise AttributeError("'URL' object has no attribute '%s'" % k)

    def __setattr__(self, k, v):
        if k in self.__dict__:
            self.__dict__[k] = u(v)
            return
        if k == "string":
            self._set_string(v)
            return
        if k == "query":
            self.parts[k] = v
            return
        if k in self.parts:
            self.__dict__["_parts"][k] = u(v)
            return
        raise AttributeError("'URL' object has no attribute '%s'" % k)

    def open(self,
             timeout=10,
             proxy=None,
             user_agent=USER_AGENT,
             referrer=REFERRER,
             authentication=None):
        """ Returns a connection to the url from which data can be retrieved with connection.read().
            When the timeout amount of seconds is exceeded, raises a URLTimeout.
            When an error occurs, raises a URLError (e.g. HTTP404NotFound).
        """
        url = self.string
        # Handle local files with urllib.urlopen() instead of urllib2.urlopen().
        if os.path.exists(url):
            return urllib.urlopen(url)
        # Handle method=POST with query string as a separate parameter.
        post = self.method == POST and self.querystring or None
        socket.setdefaulttimeout(timeout)
        # Handle proxies and cookies.
        handlers = []
        if proxy:
            handlers.append(urllib2.ProxyHandler({proxy[1]: proxy[0]}))
        handlers.append(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        handlers.append(urllib2.HTTPHandler)
        urllib2.install_opener(urllib2.build_opener(*handlers))
        # Send request.
        try:
            request = urllib2.Request(bytestring(url), post, {
                "User-Agent": user_agent,
                "Referer": referrer
            })
            # Basic authentication is established with authentication=(username, password).
            if authentication is not None:
                request.add_header(
                    "Authorization",
                    "Basic %s" % base64.encodestring('%s:%s' % authentication))
            return urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            if e.code == 301: raise HTTP301Redirect(src=e, url=url)
            if e.code == 400: raise HTTP400BadRequest(src=e, url=url)
            if e.code == 401: raise HTTP401Authentication(src=e, url=url)
            if e.code == 403: raise HTTP403Forbidden(src=e, url=url)
            if e.code == 404: raise HTTP404NotFound(src=e, url=url)
            if e.code == 420: raise HTTP420Error(src=e, url=url)
            if e.code == 429: raise HTTP429TooMayRequests(src=e, url=url)
            if e.code == 500: raise HTTP500InternalServerError(src=e, url=url)
            if e.code == 503: raise HTTP503ServiceUnavailable(src=e, url=url)
            raise HTTPError(str(e), src=e, url=url)
        except httplib.BadStatusLine as e:
            raise HTTPError(str(e), src=e, url=url)
        except socket.timeout as e:
            raise URLTimeout(src=e, url=url)
        except socket.error as e:
            if "timed out" in str((e.args + ("", ""))[0]) \
            or "timed out" in str((e.args + ("", ""))[1]):
                raise URLTimeout(src=e, url=url)
            raise URLError(str(e), src=e, url=url)
        except urllib2.URLError as e:
            if "timed out" in str(e.reason):
                raise URLTimeout(src=e, url=url)
            raise URLError(str(e), src=e, url=url)
        except ValueError as e:
            raise URLError(str(e), src=e, url=url)

    def download(self,
                 timeout=10,
                 cached=True,
                 throttle=0,
                 proxy=None,
                 user_agent=USER_AGENT,
                 referrer=REFERRER,
                 authentication=None,
                 unicode=False, **kwargs):
        """ Downloads the content at the given URL (by default it will be cached locally).
            Unless unicode=False, the content is returned as a unicode string.
        """
        # Filter OAuth parameters from cache id (they will be unique for each request).
        if self._parts is None and self.method == GET and "oauth_" not
        in self._string:
            id = self._string
        else:
            id = repr(self.parts)
            id = re.sub("u{0,1}'oauth_.*?': u{0,1}'.*?', ", "", id)
        # Keep a separate cache of unicode and raw download for same URL.
        if unicode is True:
            id = "u" + id
        if cached and id in cache:
            if isinstance(cache, dict):  # Not a Cache object.
                return cache[id]
            if unicode is True:
                return cache[id]
            if unicode is False:
                return cache.get(id, unicode=False)
        t = time.time()
        # Open a connection with the given settings, read it and (by default) cache the data.
        try:
            data = self.open(timeout, proxy, user_agent, referrer,
                             authentication).read()
        except socket.timeout as e:
            raise URLTimeout(src=e, url=self.string)
        if unicode is True:
            data = u(data)
        if cached:
            cache[id] = data
        if throttle:
            time.sleep(max(throttle - (time.time() - t), 0))
        return data

    def read(self, *args, **kwargs):
        return self.open(**kwargs).read(*args)

    @property
    def exists(self, timeout=10):
        """ Yields False if the URL generates a HTTP404NotFound error.
        """
        try:
            self.open(timeout)
        except HTTP404NotFound:
            return False
        except HTTPError:
            return True
        except URLTimeout:
            return True
        except URLError:
            return False
        except:
            return True
        return True

    @property
    def mimetype(self, timeout=10):
        """ Yields the MIME-type of the document at the URL, or None.
            MIME is more reliable than simply checking the document extension.
            You can then do: URL.mimetype in MIMETYPE_IMAGE.
        """
        try:
            return self.headers["content-type"].split(";")[0]
        except KeyError:
            return None

    @property
    def headers(self, timeout=10):
        """ Yields a dictionary with the HTTP response headers.
        """
        if self.__dict__["_headers"] is None:
            try:
                h = dict(self.open(timeout).info())
            except URLError:
                h = {}
            self.__dict__["_headers"] = h
        return self.__dict__["_headers"]

    @property
    def redirect(self, timeout=10):
        """ Yields the redirected URL, or None.
        """
        if self.__dict__["_redirect"] is None:
            try:
                r = self.open(timeout).geturl()
            except URLError:
                r = None
            self.__dict__["_redirect"] = r != self.string and r or ""
        return self.__dict__["_redirect"] or None

    def __str__(self):
        return bytestring(self.string)

    def __unicode__(self):
        # The string representation includes the query attributes with HTTP GET.
        P = self.parts
        u = []
        if P[PROTOCOL]:
            u.append("%s://" % P[PROTOCOL])
        if P[USERNAME]:
            u.append("%s:%s@" % (P[USERNAME], P[PASSWORD]))
        if P[DOMAIN]:
            u.append(P[DOMAIN])
        if P[PORT]:
            u.append(":%s" % P[PORT])
        if P[PORT] or P[DOMAIN] and not P[PATH] and not P[PAGE]:
            u.append("/")
        if P[PATH]:
            u.append("/%s/" % "/".join(P[PATH]))
        if P[PAGE] and len(u) > 0:
            u[-1] = u[-1].rstrip("/")
        if P[PAGE]:
            u.append("/%s" % P[PAGE])
        if P[QUERY] and self.method == GET:
            u.append("?%s" % self.querystring)
        if P[ANCHOR]:
            u.append("#%s" % P[ANCHOR])
        u = u"".join(u)
        u = u.lstrip("/")
        return u

    def __repr__(self):
        return "URL(%s, method=%s)" % (repr(self.string), repr(self.method))

    def copy(self):
        return URL(self.string, self.method, self.query)
