from nc_http.core import ResponseMeta


class Meta:
    """
    预设响应描述信息
    """
    OK = ResponseMeta(code=200, http_code=200, description='')
    # 请求已经被实现，而且有一个新的资源已经依据请求的需要而创建。
    CREATED = ResponseMeta(code=201, http_code=201, description='')
    # 资源已经删除。
    NO_CONTENT = ResponseMeta(code=204, http_code=204, description='')
    # 由于包含语法错误，当前请求无法被服务器理解。
    BAD_REQUEST = ResponseMeta(code=400, http_code=400, description='请求数据错误!')
    # 当前请求需要用户验证。
    UNAUTHORIZED = ResponseMeta(code=401, http_code=401, description='授权无效!')
    # 服务器已经理解请求，但是拒绝执行它。
    FORBIDDEN = ResponseMeta(code=403, http_code=403, description='无访问权限,请退出重新登录!')
    # 无权限操作
    OPERATE_FORBIDDEN = ResponseMeta(code=407, http_code=403, description='无操作权限')
    # 请求失败，请求所希望得到的资源未被在服务器上发现。
    NOT_FOUND = ResponseMeta(code=404, http_code=404, description='资源不存在!')
    # 请求行中指定的请求方法不能被用于请求相应的资源。
    METHOD_NOT_ALLOWED = ResponseMeta(code=405, http_code=405, description='方法不存在!')
    # 请求的资源的内容特性无法满足请求头中的条件，因而无法生成响应实体。
    NOT_ACCEPTABLE = ResponseMeta(code=406, http_code=406, description='客户端无效!')
    # 服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理。
    INTERNAL_SERVER_ERROR = ResponseMeta(code=500, http_code=500, description='服务器内部错误!')
    # 作为网关或者代理工作的服务器尝试执行请求时，从上游服务器接收到无效的响应。
    BAD_GATEWAY = ResponseMeta(code=502, http_code=502, description='接口错误!')
    # 由于临时的服务器维护或者过载，服务器当前无法处理请求。
    SERVICE_UNAVAILABLE = ResponseMeta(code=503, http_code=503, description='服务暂时不可用!')
    # 未能及时从上游服务器收到响应。
    GATEWAY_TIMEOUT = ResponseMeta(code=504, http_code=504, description='接口超时!')
