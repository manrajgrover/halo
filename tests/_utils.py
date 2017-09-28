"""Summary
"""
import os
import errno
import re
import codecs

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

def remove_file(filename):
    """Summary
    
    Parameters
    ----------
    filename : TYPE
        Description
    
    Raises
    ------
    Exception
        Description
    """
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise Exception(e)

def decode_utf_8_text(text):
    try:
        return codecs.decode(text, 'utf-8')
    except:
        return text

def encode_utf_8_text(text):
    try:
        return codecs.encode(text, 'utf-8')
    except:
        return text
