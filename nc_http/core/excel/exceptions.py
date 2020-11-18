class InvalidFileError(Exception):
    """无效的 excel 文件"""


class InvalidSuffixError(InvalidFileError):
    """无效的后缀名"""
