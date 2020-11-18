import unittest

from nc_http.utils.sheet.sample import SampleSheet


class SheetTestCase(unittest.TestCase):
    test_data = [
        {
            'admin_unit_official_name': '测试地区 1',
            'count_valid_situation': 34,
            'count_valid_situation_per': 0.32,
            'count_valid_situation_yoy': 0.34,
            'count_valid_situation_mom': 0.88,
        },
        {
            'admin_unit_official_name': '测试地区 2',
            'count_valid_situation': 56,
            'count_valid_situation_per': 0.62,
            'count_valid_situation_yoy': 0.87,
            'count_valid_situation_mom': 0.42,
        },
    ]

    def test_create(self):
        sheet = SampleSheet(self.test_data, year='2018')
        sheet.create('sample.xlsx')


if __name__ == '__main__':
    unittest.main()
