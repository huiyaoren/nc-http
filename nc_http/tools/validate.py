import re
import time


class DataFormatValidator:
    """
    参数验证类

    示例：
        request_data = {'name': '51zan', 'type': 3，'desc':''}
        validate_rule = {
            'name': 'required|str|max:20',   # 必须、字符串类型、最大20个字符
            'type': 'required|choices:0,1,2'   # 必须、 取值范围【0，1，2】
            'desc': 'str'  # 非必须，字符串
        }

    """

    def __init__(self, rules=None):
        """
        :param rules:  验证规则
        """
        rules = rules or []
        self.rules = rules
        self.error = ''
        self.valid_data = {}

    def check(self, data):
        """
        验证数据格式是否正确
        :param data: dict
        :return: boolean
        """
        is_valid = True
        valid_data = {}
        for key, rule_str in self.rules.items():
            rules = rule_str.split("|")
            field_value = data.get(key)

            # 如果字段不是必需的，没这个参数就不验证其它规则
            if 'required' not in rules and key not in data:
                continue

            item_valid = True
            for rule in rules:
                if not rule:
                    continue

                combination_rule = rule.split(":", 1)

                if len(combination_rule) == 2:
                    field_values = (field_value, *combination_rule[1].split(','))
                else:
                    field_values = (field_value,)

                func = getattr(self, combination_rule[0].strip())
                if not func(*field_values):
                    self.set_error(key, rule)
                    item_valid = is_valid = False
            # 如果当前项所有规则都验证通过，加入有效数据
            if item_valid:
                valid_data[key] = field_value

        self.valid_data = valid_data
        return is_valid

    def get_valid_data(self):
        return self.valid_data

    def get_error(self):
        return self.error

    def set_error(self, key, rule):
        self.error = self.error or "parameter {} is invalid, verified failed by method [{}]".format(key, rule)

    @staticmethod
    def required(value):
        """
        必需，不能为空
        :param value:
        :return:
        """
        if value in (None, ''):
            return False
        return True

    @staticmethod
    def str(value):
        """
        字符串
        :param value:
        :return:
        """
        if type(value) in (str,):
            return True
        return False

    @staticmethod
    def int(value):
        if isinstance(value, int):
            return True
        return False

    @staticmethod
    def number(value):
        """
        数字
        :param value:
        :return:
        """
        try:
            int(value)
        except ValueError:
            try:
                float(value)
            except ValueError:
                return False
            return True
        return True

    @staticmethod
    def phrase(value):
        """
        英文单词，短语
        :param value:
        :return:
        """
        if re.match(r'[a-zA-Z \']+$', value):
            return True
        return False

    @staticmethod
    def float(value):
        """
        浮点型
        :param value:
        :return:
        """
        if isinstance(value, float):
            return True
        return False

    @staticmethod
    def bool(value):
        """
        布尔型
        :param value:
        :return:
        """
        if isinstance(value, bool):
            return True
        return False

    @staticmethod
    def dict(value):
        """
        字典
        :param value:
        :return:
        """
        if type(value) == dict:
            return True
        return False

    @staticmethod
    def ip(value):
        """
        IP v4地址
        :param value:
        :return:
        """
        if re.match(r'^[\d]{1,3}(\.[\d]{1,3}){3}$', value):
            return True
        return False

    def list(self, value, item_type=None):
        """
        列表
        规则 list|list:str|list:int|list:ip|list:url
        :param value:
        :param item_type:
        :return:
        """
        if type(value) not in (list, tuple):
            return False

        if item_type:
            for item in value:
                func = getattr(self, item_type)
                if not func(item):
                    return False
        return True

    @staticmethod
    def max(value, max_value):
        """
        验证字符串最大长度
        规则 max:2|max:10086
        :param value:
        :param max_value:
        :return:
        """
        if len(value) > int(max_value):
            return False
        return True

    @staticmethod
    def min(value, min_length):
        """
        验证字符串最小长度
        规则 min:1|min:1024
        :param value:
        :param min_length:
        :return:
        """
        if len(value) < int(min_length):
            return False
        return True

    @staticmethod
    def length(value, valid_length):
        """
        验证字符串长度
        规则 length:100
        :param value:
        :param valid_length:
        :return:
        """
        if len(value) == int(valid_length):
            return True
        return False

    @staticmethod
    def choices(value, *args):
        """
        选项
        规则 choice:1,2,3|choice:a,b,c
        :param value:
        :param args:
        :return:
        """
        if str(value) in args:
            return True
        return False

    @staticmethod
    def excepts(value, *args):
        """
        排除选项
        规则 choice:1,2,3|choice:a,b,c
        :param value:
        :param args:
        :return:
        """
        if str(value) not in args:
            return True
        return False

    @staticmethod
    def range(value, min_length, max_length):
        """
        数值区间
        规则 range:1,9|range:1,|range:,9
        :param value:
        :param min_length:
        :param max_length:
        :return:
        """
        if min_length and value < int(min_length):
            return False
        if max_length and value > int(max_length):
            return False
        return True

    @staticmethod
    def url(value):
        """
        URL
        :param value:
        :return:
        """
        if re.match(r'^https?:/{2}[\w\-_]+(\.[\w\-_]+)+.*$', value):
            return True
        return False

    @staticmethod
    def email(value):
        """
        邮箱
        :param value:
        :return:
        """
        if re.match(r'^[\w\-_]+@[\w\-_]+(\.[\w\-_]+)+$', value):
            return True
        return False

    @staticmethod
    def mobile(value):
        """
        手机号
        :param value:
        :return:
        """
        if re.match(r'^1\d{10}$', value):
            return True
        return False

    @staticmethod
    def datetime(value, datetime_format):
        """
        验证日期或时间格式
        规则 datetime:%Y-%m-%d %H:%M:%S | datetime:%Y-%m-%d
        :param value:
        :param datetime_format:
        :return:
        """
        try:
            time.strptime(value, datetime_format)
        except ValueError:
            return False
        return True


if __name__ == '__main__':
    test_rules = {
        "id": "int|choices:2,3,4,5",
        "name": "required",
        "create_time": "int|range:,1000000",
        "remark": "required|str|max:5|min:1",
        "tags": "list:url",
        "avatar": "url",
        "email": "email",
        "mobile": "mobile",
        "birthday": "datetime:%Y-%m-%d %H:%M:%S",
        "ip": "ip",
        "department": "dict",
        "code": "number"
    }

    test_data = {
        "id": 4,
        "name": "aaa",
        "create_time": 111111,
        "remark": "中国123",
        "tags": (u'http://baidu.com', 'http://baidu.com'),
        "avatar": "https://aaa111.com/a.php?a=b",
        "email": "ruyi111@sina.com",
        "mobile": "15880445400",
        "birthday": "2018-10-12 12:00:00",
        "ip": "111.1.1.1",
        "department": {"a": "b"},
        "code": '11.111'
    }

    print(DataFormatValidator(test_rules).check(test_data))
