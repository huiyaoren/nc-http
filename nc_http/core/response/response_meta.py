from werkzeug.wrappers import Response
from flask import json

from nc_http.core.response.response import cross_domain_headers


class ResponseMeta(Exception):
    """
    响应描述信息
    """
    def __init__(self, code=None, description=None, http_code=400, **kwargs):
        Exception.__init__(self)
        self.http_code = http_code
        self.code = code
        self.description = description
        self.extra = kwargs

    def update(self, **kwargs):
        self.extra.update(kwargs)

    def present(self):
        data = {}
        if self.code:
            data['code'] = self.code
        if self.description:
            data['message'] = self.description

        data.update(self.extra)

        return data

    def get_response(self):
        meta = self.present()
        if meta:
            body = json.dumps({'meta': self.present()})
        else:
            body = None

        headers = [('Content-Type', 'application/json')]
        headers += cross_domain_headers(is_list=True)

        return Response(body, self.http_code, headers)

    def __call__(self, environ, start_response):
        response = self.get_response()
        return response(environ, start_response)
