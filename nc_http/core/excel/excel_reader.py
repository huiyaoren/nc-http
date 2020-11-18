import os

import xlrd
from werkzeug.datastructures import FileStorage

from nc_http.core.excel.constants import EXCEL_SUFFIX
from nc_http.core.excel.exceptions import InvalidSuffixError


class ExcelReader(object):

    @staticmethod
    def read_excel(file_src=None, row_index=0, file_contents=None, sheet_name=None):
        if file_src:
            data = xlrd.open_workbook(file_src)
        elif file_contents:
            data = xlrd.open_workbook(file_contents=file_contents)
        else:
            return []

        sheets = data.sheets()
        table = sheets[0]
        # 根据 sheet 名来选择 sheet（可选）
        if sheet_name:
            for sheet in sheets:
                if sheet.name == sheet_name:
                    table = sheet

        nrows = table.nrows
        rows = []
        for rownum in range(row_index, nrows):
            row = table.row_values(rownum)
            rows.append(row)
        return rows

    @staticmethod
    def read(file_handler):
        if isinstance(file_handler, FileStorage):
            filename = file_handler.filename.strip(r'"')
            suffix = os.path.splitext(filename)[-1]
            if suffix not in EXCEL_SUFFIX:
                raise InvalidSuffixError
            result = ExcelReader.read_excel(file_contents=file_handler.read())
        else:
            filename = str(file_handler) if not hasattr(file_handler, 'name') else file_handler.name
            suffix = os.path.splitext(filename)[-1]
            if suffix not in EXCEL_SUFFIX:
                raise InvalidSuffixError
            result = ExcelReader.read_excel(filename)
        return result


if __name__ == '__main__':
    s = ExcelReader.read(open(r'D:\test.xlsx'))
    print(s)
