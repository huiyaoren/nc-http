import unittest

from nc_http.tools.validate import DataFormatValidator


class ValidateTestCase(unittest.TestCase):
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

    def test_create(self):
        validator = DataFormatValidator(self.test_rules)
        result = validator.check(self.test_data)
        validator.get_error()
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
