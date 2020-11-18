import random
import re
import string

from six.moves.urllib import parse as urlparse

"""
工具函数集
"""


def valid_email(email):
    """
    验证字符串是否为合法电子邮件
    :param email:
    :return:
    """
    email = str(email)
    if len(email) > 7:
        pattern = (
            r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
            r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        )
        if re.match(pattern, email) is not None:
            return True
    return False


def random_ascii_string(length, mask=None):
    """
    生成随机 ascii 字符串
    :param length:
    :param mask:
    :return:
    """
    LETTERS = 0b001
    DIGITS = 0b010
    PUNCTUATION = 0b100

    if mask is None:
        mask = LETTERS | DIGITS

    unicode_ascii_characters = ''
    if mask & LETTERS:
        unicode_ascii_characters += string.ascii_letters
    if mask & DIGITS:
        unicode_ascii_characters += string.digits
    if mask & PUNCTUATION:
        unicode_ascii_characters += string.punctuation

    if not unicode_ascii_characters:
        return ''

    rnd = random.SystemRandom()
    return ''.join([rnd.choice(unicode_ascii_characters) for _ in range(length)])


def url_parse_query(url):
    """
    从 url 提取 query string 字典
    :param url:
    :return:
    """
    return dict(urlparse.parse_qsl(urlparse.urlparse(url).query, True))


def url_without_query(url):
    """
    移除 url 中 query string
    """
    url = urlparse.urlparse(url)
    return urlparse.urlunparse((url.scheme, url.netloc, url.path, url.params, '', url.fragment))


def build_url(base, additional_params=None):
    """
    url 中增加 query string 参数
    :param base:
    :param additional_params:
    :return:
    """
    url = urlparse.urlparse(base)
    query_params = {}
    query_params.update(urlparse.parse_qsl(url.query, True))
    if additional_params is not None:
        query_params.update(additional_params)
        for k, v in additional_params.items():
            if v is None:
                query_params.pop(k)

    return urlparse.urlunparse(
        (url.scheme, url.netloc, url.path, url.params, urlparse.urlencode(query_params), url.fragment)
    )


if __name__ == '__main__':
    s = valid_email('wslstest@sample.com')
    print(s)

    s = random_ascii_string(40)
    print(s)

    s = url_parse_query('http://api_w.qiange.so/hz/shorturl_tongji?short_url=BkPMeb')
    print(s)

    s = url_without_query('http://api_w.qiange.so/hz/shorturl_tongji?short_url=BkPMeb')
    print(s)

    s = build_url('http://www.baidu.com', {'a': 1, 'b': 2})
    print(s)
