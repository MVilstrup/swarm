"""
This module provides some useful functions for working with Response objects
"""
import re
import weakref

from w3lib import html

_baseurl_cache = weakref.WeakKeyDictionary()


def get_base_url(response):
    """
    Return the base url of the given response, joined with the response url
    """
    if response not in _baseurl_cache:
        text = response.body_as_unicode()[0:4096]
        _baseurl_cache[response] = html.get_base_url(text, response.url,
                                                     response.encoding)
    return _baseurl_cache[response]


_noscript_re = re.compile(u'<noscript>.*?</noscript>',
                          re.IGNORECASE | re.DOTALL)
_script_re = re.compile(u'<script.*?>.*?</script>', re.IGNORECASE | re.DOTALL)
_metaref_cache = weakref.WeakKeyDictionary()


def get_meta_refresh(response):
    """
    Parse the http-equiv refrsh parameter from the given response
    """
    if response not in _metaref_cache:
        text = response.body_as_unicode()[0:4096]
        text = _noscript_re.sub(u'', text)
        text = _script_re.sub(u'', text)
        _metaref_cache[response] = html.get_meta_refresh(text, response.url,
                                                         response.encoding)
    return _metaref_cache[response]
