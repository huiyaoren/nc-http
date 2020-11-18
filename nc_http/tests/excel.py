import unittest

from nc_http.core.excel.excel_reader import ExcelReader
from nc_http.core.excel.excel_writer import ExcelWriter


class ExcelTestCase(unittest.TestCase):
    filename = r'D:\test.xlsx'

    def test_writer(self):
        ExcelWriter.create_excel(self.filename, [[1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2]])
        ExcelWriter.pack_excel([[1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2]])

    def test_reader(self):
        ExcelReader.read(open(self.filename))


if __name__ == '__main__':
    unittest.main()
