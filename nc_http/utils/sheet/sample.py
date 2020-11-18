from nc_http.utils.sheet.sheet import Sheet


class SampleSheet(Sheet):
    """
    样例表格
    """

    all_fields = [
        'admin_unit_official_name',
        'count_valid_situation',
        'count_valid_situation_per',
        'count_valid_situation_yoy',
        'count_valid_situation_mom',
    ]
    style_formats = {
        'title': {
            'font': 'Arial Unicode MS', 'font_size': 20, 'bold': False,
            'align': 'center', 'valign': 'vcenter',
        },
        'header': {
            'font': 'Arial Unicode MS', 'font_size': 11, 'bold': False,
            'align': 'center', 'valign': 'vcenter', 'border': True, 'text_wrap': False,
        },
        'body': {
            'font': 'Arial Unicode MS', 'font_size': 11, 'bold': False,
            'align': 'center', 'valign': 'vcenter', 'border': True, 'text_wrap': True,
        },
        'remark': {
            'font': 'Arial Unicode MS', 'font_size': 10, 'bold': False,
            'align': 'center', 'valign': 'vcenter',
            'bottom': 1, 'top_color': 'white', 'top': 1
        },
        'remark_year': {
            'font': 'Arial Unicode MS', 'font_size': 8, 'bold': False,
            'align': 'center', 'valign': 'vcenter',
            'bottom': 1, 'top_color': 'white', 'top': 1,
            'num_format': 'yyyy"年"'
        },
    }
    round_digits = 4
    row_stretches = [
        [0, 30],
    ]
    col_stretches = [
        [0, 0, 29, {'text_wrap': True}],
        [1, 1, 20],
        [2, 2, 20, {'num_format': '0.00%'}],
        [3, 3, 20, {'num_format': '0.00%'}],
        [4, 4, 20, {'num_format': '0.00%'}],
    ]

    def set_sheet(self):
        self.title = '全市管辖单位样例数据统计表'
        self.headers = [
            ['', '', '', ],
            ['', '', '', ],
            ['地区项目', '总数', '占比情况', '同比情况', '环比情况', ],
        ]
        self.merges = [
            [0, 0, 0, 4, self.title, self.style_formats['title']],
            [1, 0, 1, 4, '{} 年'.format(self.meta['year']), self.style_formats['remark']],
        ]

    def clean_data(self):
        return [self.flat_row(item) for item in self.origin_data]


if __name__ == '__main__':
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
    sheet = SampleSheet(test_data, year='2018')
    sheet.create('sample.xlsx')
