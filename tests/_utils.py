"""Utilities for tests.
"""
import codecs
import re


def strip_ansi(string):
    """Strip ANSI encoding from given string.

    Parameters
    ----------
    string : str
        String from which encoding needs to be removed

    Returns
    -------
    str
        Encoding free string
    """
    pattern = r'(\x1b\[|\x9b)[^@-_]*[@-_]|\x1b[@-_]'
    return re.sub(pattern, '', string, flags=re.I)


def find_colors(string):
    """Find colors from given string

    Parameters
    ----------
    string : str
        String from which colors need to be find

    Returns
    -------
    str
        List of found colors
    """
    return re.findall(r'\[\d\dm', string, flags=re.I)


def decode_utf_8_text(text):
    """Decodes the text from utf-8 format.

    Parameters
    ----------
    text : str
        Text to be decoded

    Returns
    -------
    str
        Decoded text
    """
    try:
        return codecs.decode(text, 'utf-8')
    except (TypeError, ValueError):
        return text


def encode_utf_8_text(text):
    """Encodes the text to utf-8 format

    Parameters
    ----------
    text : str
        Text to be encoded

    Returns
    -------
    str
        Encoded text
    """
    try:
        return codecs.encode(text, 'utf-8')
    except (TypeError, ValueError):
        return text
