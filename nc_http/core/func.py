import json
import zlib

from flask import request, g, send_file
from six import string_types


def strip_value(data):
    """

    :param data:
    :return:
    """
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = strip_value(value)
    elif isinstance(data, list):
        for key, value in enumerate(data):
            data[key] = strip_value(value)
    elif isinstance(data, string_types):
        data = data.strip()

    return data


def get_request_json():
    """
    获取 json 传递参数
    :return:
    """
    if 'request_data' not in g:
        if request.method.lower() == 'get':
            data = request.args.to_dict()
        else:
            if request.content_encoding and 'gzip' in request.content_encoding:
                json_data = zlib.decompress(request.get_data())
                data = json.loads(json_data)
            else:
                data = request.get_json(force=True, silent=True) or {}

        g.request_data = strip_value(data)

    return g.request_data


def get_paging(limit=10):
    """
    获取分页参数
    :param limit:
    :return:
    """
    data = get_request_json()

    return {
        'page': int(data.get('page') or 1),
        'size': int(data.get('size') or limit),
        'offset': int(data.get('offset') or 0),
        'limit': int(data.get('limit') or limit)
    }


def send_excel(file_handler, file_name, suffix='xlsx'):
    """
    发送 excel 文件
    :param file_handler:
    :param file_name:
    :param suffix:
    :return:
    """
    return send_file(
        file_handler,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        attachment_filename='{}.{}'.format(file_name, suffix),
        as_attachment=True
    )


def send_png(img_handler, name='image'):
    """
    发送图片文件（可用于验证码）
    :param img_handler:
    :param name:
    :return:
    """
    return send_file(
        img_handler,
        mimetype='image/png',
        attachment_filename='{}.png'.format(name),
        as_attachment=True
    )


def get_client_ip(request):
    """
    获取客户端 ip
    :param request: flask.Request
    :return:
    """
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ips = x_forwarded_for.split(',')
        return ips[0].strip()
    return request.headers.get('X-Real-Ip', request.remote_addr)
