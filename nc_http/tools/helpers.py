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


LETTERS = 0b001
DIGITS = 0b010
PUNCTUATION = 0b100


def random_ascii_string(length, mask=None):
    """
    生成随机 ascii 字符串
    :param length:
    :param mask:
    :return:
    """

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


COUNTRY_ZONE = ('86',)


def parse_mobile(mobile_str):
    """
    解析手机号码
    :param mobile_str:
    :return:
    """
    match = re.findall(r'^(\+({0}))?(\d+)$'.format('|'.join(COUNTRY_ZONE)), mobile_str)
    if match:
        zone, mobile = match[0][-2:]
        if '+' in mobile_str and not zone:
            return None

        if not zone:
            zone = '86'

        if zone == '86' and re.match(r'^1\d{10}$', mobile) is not None:
            return zone, mobile

    return None


def list_to_tree(rows, id_key='id', parent_id_key='parent_id', i=0):
    """
    list转tree的函数
    :param rows:
    :param id_key:
    :param parent_id_key:
    :param i:
    :return:
    """
    data = []
    for row in rows:
        if row[parent_id_key] == i:
            row['children'] = list_to_tree(rows, id_key=id_key, parent_id_key=parent_id_key, i=row[id_key])
            data.append(row)
    return data


def cut_tree(trees, nodes, id_key='id', parent_id_key='parent_id'):
    """
    根据叶结点整理出包含所有叶节点的最小树结构
    :param trees:
    :param nodes: 叶结点
    :param id_key:
    :param parent_id_key:
    :return:
    """
    data = []
    for row in trees:
        children = cut_tree(row['children'], nodes, id_key=id_key, parent_id_key=parent_id_key)
        if children or row['id'] in nodes:
            row['children'] = children
            data.append(row)
    return data


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

    s = parse_mobile('+8615888888888')
    print(s)
