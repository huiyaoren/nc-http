import unittest

from nc_http.utils.front_end_sucks import FrontEndSucksUtil


class FrontEndSucksTestCase(unittest.TestCase):

    test_data = [
        {
            "parent_smid": 0, "smid": 1, "smx": None, "smy": 23.6732798415205, "smlibtileid": 1, "smuserid": 0,
            "id": "2", "city": "漳州", "county": "东山", "yhzx": "东山养护管理中心", "area": "6800", "xyjz": "0",
            "zd": 151, "fwxjz": "6800", "fwxjf": "1100", "sbtz": "136.325", "sbjl": "19.475", "sbtzh": "155.8",
            "pfnf": "2013", "ssnf": "2013", "wcqk": "完成", "ssglfj": None, "userKey": None, "fjbm": None
        },
        {
            "parent_smid": 1, "smid": 2, "smx": 117.49294498942, "smy": 23.7292785701706, "smlibtileid": 1,
            "smuserid": 0, "id": "5", "city": "漳州", "county": "东山", "yhzx": "康美养护应急基地", "area": "6800",
            "xyjz": "0", "zd": None, "fwxjz": "1529", "fwxjf": "6800", "sbtz": "0", "sbjl": "0", "sbtzh": "253.9",
            "pfnf": "2018", "ssnf": "2018", "wcqk": "完成", "ssglfj": "东山县分中心", "userKey": "康美", "fjbm": "1011615"
        },
        {
            "parent_smid": 2, "smid": 3, "smx": 117.38910452, "smy": 26.00433034, "smlibtileid": 1,
            "smuserid": 0, "id": "8", "city": "三明", "county": "永安", "yhzx": "下渡养护应急基地", "area": "5737",
            "xyjz": "0", "zd": "58", "fwxjz": "5737", "fwxjf": "158", "sbtz": "79.2365", "sbjl": "11.3195",
            "sbtzh": "90.556", "pfnf": "2015", "ssnf": "2015", "wcqk": "完成", "ssglfj": "三明市公路养护中心永安分中心",
            "userKey": "下渡", "fjbm": "1011813"
        },
        {
            "parent_smid": 3, "smid": 4, "smx": 117.51357599, "smy": 26.72154192, "smlibtileid": 1,
            "smuserid": 0, "id": "6", "city": "三明", "county": "将乐", "yhzx": "下村养护中心", "area": "35148",
            "xyjz": "0", "zd": "53", "fwxjz": "1200", "fwxjf": "35148", "sbtz": "509.09415", "sbjl": "64.15630714",
            "sbtzh": "573.2504571", "pfnf": "2013", "ssnf": "2013", "wcqk": "完成",
            "ssglfj": "三明市公路养护中心将乐分中心", "userKey": "下村", "fjbm": "1011817"
        },
        {
            "parent_smid": 4, "smid": 5, "smx": 119.747903381185, "smy": 25.4961286621859, "smlibtileid": 1,
            "smuserid": 0, "id": "10", "city": "平潭", "county": "平潭", "yhzx": "中湖养护应急基地新建", "area": "6667",
            "xyjz": "0", "zd": "14.33", "fwxjz": "1500", "fwxjf": "6667", "sbtz": "0", "sbjl": "0", "sbtzh": "375.4935",
            "pfnf": "2016", "ssnf": "2016", "wcqk": "完成", "ssglfj": "平潭综合实验区公路事业发展中心", "userKey": "中湖",
            "fjbm": "10120"
        },
    ]

    def test_round(self):
        test_data = self.test_data
        _result = FrontEndSucksUtil.round(test_data, 1)
        self.assertEqual(len(_result), len(test_data))
        _result = FrontEndSucksUtil.round(test_data, 1, keys=['smx', 'smy', 'zd', 'sbjl', 'sbtz', 'sbtzh'])
        self.assertEqual(_result[0]['smy'], 23.7)
        _result = FrontEndSucksUtil.round(test_data[0], 1, keys=['smx', 'smy', 'zd', 'sbjl', 'sbtz', 'sbtzh'])
        self.assertEqual(_result['smy'], 23.7)

    def test_percent(self):
        test_data = self.test_data
        _result = FrontEndSucksUtil.round(test_data[0], 1, keys=['smx', 'smy', 'zd', 'sbjl', 'sbtz', 'sbtzh'])
        _result = FrontEndSucksUtil.percent(_result, keys=['smx', 'smy', 'zd', 'sbjl', 'sbtz', 'sbtzh'])
        self.assertEqual(_result['smy'], '2370.0%')

    def test_mapping(self):
        test_data = self.test_data
        test_field_map = {0: '零', 1: '一', 2: '二', 3: '三', 4: '四'}
        _result = FrontEndSucksUtil.mapping(test_data, test_field_map, test_field_map, key='smid')
        _result = FrontEndSucksUtil.mapping(test_data, test_field_map, key_map={'smid': 'smid_str'})
        self.assertEqual(_result[0]['smid_str'], '一')

    def test_sum(self):
        test_data = self.test_data
        _total = FrontEndSucksUtil.sum(test_data, key='zd')
        _total = FrontEndSucksUtil.sum(test_data, key='smx')
        self.assertEqual(_total, 472.143528880605)

    def test_ratio(self):
        test_data = self.test_data
        _total = FrontEndSucksUtil.sum(test_data, key='smx')
        _result = FrontEndSucksUtil.ratio(test_data, _total, key_map={'zd': 'zd_per'})
        self.assertEqual(_result[0]['zd_per'], 151 / _total)

    def test_list_to_tree(self):
        test_data = self.test_data
        _result = FrontEndSucksUtil.list_to_tree(test_data, id_key='smid', parent_id_key='parent_smid')
        self.assertEqual(_result[0]['children'][0]['children'][0]['children'][0]['children'][0]['children'], [])


if __name__ == '__main__':
    unittest.main()
