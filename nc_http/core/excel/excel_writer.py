from io import BytesIO

from xlsxwriter import Workbook

from nc_http.core.excel.excel_format import ExcelFormat


class ExcelWriter(object):
    title_format_setting = ExcelFormat.title
    remark_format_setting = ExcelFormat.remark
    header_format_setting = ExcelFormat.big_header
    body_format_setting = ExcelFormat.big_body

    @classmethod
    def pack_excel(cls, data=None, **options):
        output = BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        cls.write(workbook, data, **options)
        workbook.close()
        output.seek(0)
        return output

    @classmethod
    def create_excel(cls, file, data=None, **options):
        data = data or []
        workbook = Workbook(file)
        cls.write(workbook, data, **options)
        workbook.close()
        return file

    @classmethod
    def write(cls, workbook, data, headers=None, merges=None, row_stretches=None, col_stretches=None,
              paper=None, style_formats=None):
        data = data or []
        headers = headers or []
        if headers:
            data = headers + data
        if not data:
            return

        worksheet = workbook.add_worksheet()
        worksheet.center_horizontally()
        worksheet.set_margins(left=0.2, right=0.2, top=0.4, bottom=0.2)
        # worksheet.set_column('A:Z', 20)
        # worksheet.set_default_row(16)
        if paper:
            worksheet.set_paper(paper)

        style_formats = style_formats or {}

        header_format = style_formats.get('header') or cls.header_format_setting
        body_format = style_formats.get('body') or cls.body_format_setting

        col_style = {}
        if col_stretches:
            '''
            col_stretches = [
                [0, 0, 25, {'text_wrap': True}],
                [1, 1, 10],
            ]
            '''
            for stretch in col_stretches:
                if len(stretch) != 4:
                    continue
                if stretch[0] == stretch[1]:
                    col_style[stretch[0]] = stretch[3]
                elif stretch[0] < stretch[1]:
                    for col in range(stretch[0], stretch[1] + 1):
                        col_style[col] = stretch[3]

        for row_num in range(len(data)):
            row = data[row_num]
            if isinstance(row, list):
                for col_num in range(len(row)):
                    column = row[col_num]
                    if headers and row_num < len(headers):
                        worksheet.write(row_num, col_num, column, workbook.add_format(header_format.copy()))
                    else:
                        # 单元格样式与列样式合并
                        _body_format = body_format.copy()
                        if col_style:
                            _col_style = col_style.get(col_num, {})
                            _body_format.update(_col_style)
                        worksheet.write(row_num, col_num, column, workbook.add_format(_body_format))
        # 单元格合并
        if merges:
            for merge in merges:
                if len(merge) > 5:
                    format_item = workbook.add_format(merge[5])
                else:
                    format_item = workbook.add_format(header_format)
                worksheet.merge_range(*merge[:5], cell_format=format_item)
        # 行高指定
        if row_stretches:
            for stretch in row_stretches:
                worksheet.set_row(*stretch)
        # 列宽指定
        if col_stretches:
            for stretch in col_stretches:
                stretch = stretch.copy()
                if len(stretch) >= 4:
                    stretch[3] = workbook.add_format(stretch[3])
                worksheet.set_column(*stretch)


if __name__ == '__main__':
    ExcelWriter.create_excel(r'E:\test.xlsx', [[1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2]])

    ExcelWriter.pack_excel([[1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2]])
