from decimal import Decimal
from types import SimpleNamespace


class HandleType:
    SWITCH = 1
    UPDATE = 2
    STAT = 3


class FrontEndSucksUtil:
    """
    Don't blame me, we have a terrible Front-End coder.
    """

    @classmethod
    def round(cls, data, digits, **kwargs):
        """
        结果处理 小数保留
        :param data: list<dict> / dict
        :param digits: number
        :param keys: list<str>
        :param key: str
        :return:
        """
        def _round(field):
            if not field:
                return None

            if isinstance(field, str):
                field = float(field)

            return round(field, digits)

        return cls.handle(data, _round, **kwargs)

    @classmethod
    def percent(cls, data, **kwargs):
        """
        结果处理 浮点型 转百分比
        :param data:
        :param kwargs:
        :return:
        """
        def _percent(field):
            if not field:
                return None

            field = str(field)
            _field = '{}%'.format(Decimal(field) * 100)
            return _field

        return cls.handle(data, _percent, **kwargs)

    @classmethod
    def mapping(cls, data, field_map, key_map=None, **kwargs):
        """
        结果处理 字段映射
        :param data:
        :param field_map:
        :param key_map:
        :param kwargs:
        :return:
        """
        field_map = field_map or {}
        if key_map:
            kwargs['keys'] = list(key_map.keys())

        # 存在 keymap 参数时 将映射结果放入映射后的 key 中 否则放入原 key 中
        def _mapping(key, field):
            value = field_map.get(field)
            if key_map:
                key = key_map.get(key)

            if not key:
                return {}

            return {key: value}

        return cls.handle(data, _mapping, handle_type=HandleType.UPDATE, **kwargs)

    @classmethod
    def sum(cls, data, **kwargs):
        """
        结果处理 对象列表求和
        :param data:
        :param kwargs:
        :return:
        """
        obj = SimpleNamespace(sum=0)

        def _sum(field):
            if isinstance(field, str):
                field = float(field)
            elif isinstance(field, int) or isinstance(field, float):
                field = field
            else:
                return
            obj.sum += field

        cls.handle(data, _sum, handle_type=HandleType.STAT, **kwargs)

        return obj.sum

    @classmethod
    def ratio(cls, data, total, key_map=None, **kwargs):
        """
        结果处理 对象列表占比
        :param data:
        :param total:
        :param key_map:
        :param kwargs:
        :return:
        """
        if key_map:
            kwargs['keys'] = list(key_map.keys())

        def _ratio(key, field):
            if isinstance(field, str):
                _field = float(field) / total
            elif isinstance(field, int) or isinstance(field, float):
                _field = field / total
            else:
                _field = 0

            if key_map:
                key = key_map.get(key)

            return {key: _field}

        return cls.handle(data, _ratio, handle_type=HandleType.UPDATE, **kwargs)

    @classmethod
    def handle(cls, data, func, key=None, keys=None, handle_type=HandleType.SWITCH):
        """
        结果处理 自定义函数处理
        :param data:
        :param func:
        :param key:
        :param keys:
        :param handle_type:
        :return:
        """
        keys = cls._parse_keys(key, keys)
        if not keys:
            return data

        data_is_dict = False
        if isinstance(data, dict):
            data_is_dict = True
            data = [data]

        rs = []
        for item in data:
            _item = item.copy()
            for key in keys:
                field = _item.get(key)
                # 值的替换
                if handle_type == HandleType.SWITCH:
                    _item[key] = func(field)
                # 值的新增
                elif handle_type == HandleType.UPDATE:
                    _item.update(func(key, field))
                # 值的统计
                elif handle_type == HandleType.STAT:
                    func(field)
            rs.append(_item)

        if data_is_dict:
            return rs[0]

        return rs

    @classmethod
    def _parse_keys(cls, key, keys):
        keys = keys or []
        if key:
            keys.append(key)
        return keys

    @staticmethod
    def list_to_tree(rows, id_key='id', parent_id_key='parent_id', i=0):
        """
        结果处理 列表转树
        :param rows:
        :param id_key:
        :param parent_id_key:
        :param i:
        :return:
        """
        data = []
        for row in rows:
            if row[parent_id_key] == i:
                row['children'] = FrontEndSucksUtil.list_to_tree(rows, id_key, parent_id_key, row[id_key])
                data.append(row)
        return data


'''
# 结果处理 树转列表 todo
# 输入处理 字符型日期转时间戳 todo
'''
