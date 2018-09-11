# imports - standard imports
import re

_REGEX_ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

def strip_ansi(string):
    string = _REGEX_ANSI_ESCAPE.sub("", string)
    return string

def strip(string):
    string = string.lstrip()
    string = string.rstrip()
    return string

def safe_decode(object_, encoding = "utf-8"):
    decoded = object_
    
    try:
        decoded = object_.decode(encoding)
    except AttributeError:
        pass

    return decoded