from flask import g, request
from flask import json
from flask import make_response


class Response(object):
    """
    业务响应类
    """
    def __init__(self, data=None, meta=None, pagination=None, headers=None, code=200):
        result = {}

        pagination = pagination or getattr(g, 'pagination', None)
        if hasattr(pagination, 'present'):
            result['pagination'] = pagination.present()
        elif pagination:
            result['pagination'] = pagination

        if hasattr(meta, 'present'):
            result['meta'] = meta.present()
        elif meta:
            result['meta'] = meta
        else:
            # 默认 meta
            result['meta'] = {
                'code': code,
                'message': '',
            }

        if hasattr(data, 'present'):
            result['data'] = data.present()
        else:
            result['data'] = data

        head = {'Content-Type': 'application/json'}
        if headers:
            head.update(headers)

        if head.get('Content-Type') == 'application/json':
            result = json.dumps(result)

        head.update(cross_domain_headers())

        response = make_response(result)
        response.headers = head

        self.response = response

    def __call__(self, environ, start_response):
        return self.response(environ, start_response)


def cross_domain_headers(is_list=False):
    """
    跨域 headers
    :param is_list:
    :return:
    """
    origin = request.headers.get('Origin')
    headers = {}
    if origin:
        headers['Access-Control-Allow-Origin'] = origin
        headers['Access-Control-Allow-Credentials'] = 'true'
        headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        headers['Access-Control-Allow-Headers'] = ', '.join((
            'Origin', 'No-Cache', 'X-Requested-With', 'If-Modified-Since', 'Pragma',
            'Last-Modified', 'Cache-Control', 'Expires', 'Content-Type',
        ))
    else:
        headers['Access-Control-Allow-Origin'] = '*'

    if is_list:
        return [(key, value) for key, value in headers.items()]
    else:
        return headers
