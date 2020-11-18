import os
import subprocess

from nc_http.core.excel.excel_writer import ExcelWriter
from nc_http.utils.sheet.paper_size import PaperSize


class Sheet:
    origin_data = []  # 源统计数据
    data = []  # 处理后的统计数据
    year = ''  # 表数据代表年份
    title = ''  # 表标题
    headers = []  # 表头指定
    merges = []  # 单元格合并指定
    row_stretches = []  # 行高指定
    col_stretches = []  # 列宽指定
    filename = ''  # 文件名
    pdf_filename = ''  # 文件名
    paper = PaperSize.A3  # 纸张大小

    round_digits = 1  # 小数保留位数
    subtotal_fields = []  # 需要进行小计累加的字段
    all_fields = []  # 所有字段

    style_formats = {}  # 表头、表体样式

    def __init__(self, data, title=None, headers=None, merges=None, row_stretches=None, col_stretches=None, **meta):
        self.meta = {}
        self.origin_data = data
        if title:
            self.title = title
        if headers:
            self.headers = headers
        if merges:
            self.merges = merges
        if row_stretches:
            self.row_stretches = row_stretches
        if col_stretches:
            self.col_stretches = col_stretches
        if meta:
            self.meta = meta

        self.set_sheet()
        self.data = self.clean_data()
        # self.filename = self.create_filename()
        # self.pdf_filename = self.create_filename(suffix='pdf')

    def set_sheet(self):
        """
        处理相关动态配置
        :return:
        """
        pass

    def clean_data(self):
        """
        数据预清洗
        :return:
        """
        return list(self.data)

    def create(self, file_path):
        """
        创建 excel 文件
        :param file_path:
        :return:
        """
        return ExcelWriter.create_excel(
            file_path, self.data,
            headers=self.headers,
            merges=self.merges,
            row_stretches=self.row_stretches,
            col_stretches=self.col_stretches,
            paper=self.paper,
            style_formats=self.style_formats,
        )

    def pack(self):
        """
        创建 excel 文件句柄
        :return:
        """
        return ExcelWriter.pack_excel(
            self.data,
            headers=self.headers,
            merges=self.merges,
            row_stretches=self.row_stretches,
            col_stretches=self.col_stretches,
            paper=self.paper,
            style_formats=self.style_formats,
        )

    @classmethod
    def _init_subtotal(cls, subtotal, fields=None):
        """
        小计初始化
        :param subtotal:
        :param fields:
        :return:
        """
        fields = fields or cls.subtotal_fields
        for field in fields:
            if subtotal.get(field) is None:
                subtotal[field] = 0

    @classmethod
    def _add_subtotal(cls, subtotal, item, fields):
        """
        小计累加
        :param subtotal: dict 小计
        :param item: dict 统计项
        :param fields: list 需要小计字段
        :return:
        """
        for field in fields:
            if subtotal.get(field) is None:
                subtotal[field] = 0
            # subtotal.setdefault(field, 0)
            subtotal[field] += round((item[field] or 0), cls.round_digits)
            # 小计小数点后三位舍入(四舍六入五成双) 若遇到数据舍入错误建议牺牲性能更换为 Decimal 运算
            # subtotal[field] = round(subtotal[field], cls.round_digits)
        return subtotal

    def create_filename(self, suffix='xlsx'):
        """
        创建表格文件名
        :param suffix:
        :return:
        """
        filename = '{}.{}'.format(self.title, suffix)
        return os.sep.join([self.meta['year'], '表', filename])

    def flat_row(self, item):
        return [round(item[k], self.round_digits) if isinstance(item.get(k), float) else item.get(k, '') for k in
                self.all_fields]

    @staticmethod
    def create_pdf(sheet_file, path=None):
        """
        创建 PDF 文件 (依赖 soffice)
        :param sheet_file:
        :param path:
        :return:
        """
        path = path or os.sep.join(sheet_file.split(os.sep)[:-1])
        command = "soffice --headless --convert-to pdf {} --outdir {}".format(sheet_file, path)
        try:
            p = subprocess.call(command, shell=True)
            print(p)
            assert p == 0, '转格式失败...'
        except Exception as e:
            print('create_pdf_file | command: {}'.format(command))
            # Logger.warning('create_pdf_file | command: {}'.format(command))
            raise e
        return sheet_file.replace('.xlsx', '.pdf')
