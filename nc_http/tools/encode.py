import base64

import six


def ensure_unicode(s):
    """
    :param s:
    :return:
    """
    if isinstance(s, six.binary_type):
        return s.decode('utf-8')
    else:
        return s


def ensure_byte(s):
    """
    :param s:
    :return:
    """
    if isinstance(s, six.text_type):
        return s.encode('utf-8')
    else:
        return s


def string_to_base64(s):
    """
    :param s:
    :return:
    """
    return base64.b64encode(ensure_byte(s))


def base64_to_string(b):
    """
    :param b:
    :return:
    """
    return ensure_unicode(base64.b64decode(b))
