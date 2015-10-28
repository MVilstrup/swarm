# -*- coding: utf-8 -*-
#### UNICODE #######################################################################################
# Latin-1 (ISO-8859-1) encoding is identical to Windows-1252 except for the code points 128-159:
# Latin-1 assigns control codes in this range, Windows-1252 has characters, punctuation, symbols
# assigned to these code points.

import unicodedata


GREMLINS = set([
    0x0152, 0x0153, 0x0160, 0x0161, 0x0178, 0x017E, 0x017D, 0x0192, 0x02C6, 
    0x02DC, 0x2013, 0x2014, 0x201A, 0x201C, 0x201D, 0x201E, 0x2018, 0x2019, 
    0x2020, 0x2021, 0x2022, 0x2026, 0x2030, 0x2039, 0x203A, 0x20AC, 0x2122
])

def fix(s, ignore=""):
    """ 
    Returns a Unicode string that fixes common encoding problems (Latin-1, Windows-1252).
        For example: fix("clichÃ©") => u"cliché".
    """
    # http://blog.luminoso.com/2012/08/20/fix-unicode-mistakes-with-python/
    if not isinstance(s, unicode):
        s = s.decode("utf-8")
        # If this doesn't work,
        # copy & paste string in a Unicode .txt, 
        # and then pass open(f).read() to fix().
    u = []
    i = 0
    for j, ch in enumerate(s):
        if ch in ignore:
            continue
        if ord(ch) < 128: # ASCII
            continue
        if ord(ch) in GREMLINS:
            ch = ch.encode("windows-1252")
        else:
            try:
                ch = ch.encode("latin-1")
            except:
                ch = ch.encode("utf-8")
        u.append(s[i:j].encode("utf-8"))
        u.append(ch)
        i = j + 1
    u.append(s[i:].encode("utf-8"))
    u = "".join(u)
    u = u.decode("utf-8", "replace")
    u = u.replace("\n", "\n ")
    u = u.split(" ")
    # Revert words that have the replacement character,
    # i.e., fix("cliché") should not return u"clich�".
    for i, (w1, w2) in enumerate(zip(s.split(" "), u)):
        if u"\ufffd" in w2: # �
            u[i] = w1
    u = " ".join(u)
    u = u.replace("\n ", "\n")
    return u

def latin(s):
    """ Returns True if the string contains only Latin-1 characters
        (no Chinese, Japanese, Arabic, Cyrillic, Hebrew, Greek, ...).
    """
    if not isinstance(s, unicode):
        s = s.decode("utf-8")
    return all(unicodedata.name(ch).startswith("LATIN") for ch in s if ch.isalpha())

def decode_string(v, encoding="utf-8"):
    """ Returns the given value as a Unicode string (if possible).
    """
    if isinstance(encoding, basestring):
        encoding = ((encoding,),) + (("windows-1252",), ("utf-8", "ignore"))
    if isinstance(v, str):
        for e in encoding:
            try: return v.decode(*e)
            except:
                pass
        return v
    return unicode(v)

def encode_string(v, encoding="utf-8"):
    """ Returns the given value as a Python byte string (if possible).
    """
    if isinstance(encoding, basestring):
        encoding = ((encoding,),) + (("windows-1252",), ("utf-8", "ignore"))
    if isinstance(v, unicode):
        for e in encoding:
            try: return v.encode(*e)
            except:
                pass
        return v
    return str(v)

u = decode_utf8 = decode_string
s = encode_utf8 = encode_string
