class ExcelFormat:

    title = {
        'font': '黑体', 'font_size': 18, 'bold': True, 'align': 'center', 'valign': 'vcenter',
    }
    remark = {
        'font': '黑体', 'font_size': 8, 'bold': False, 'align': 'right', 'valign': 'vcenter',
        'bottom': 1, 'top_color': 'white', 'top': 1,
    }
    header = {
        'font': '宋体', 'font_size': 8, 'bold': True, 'align': 'center', 'valign': 'vcenter',
        'border': 1, 'text_wrap': True,
    }
    body = {
        'font': '宋体', 'font_size': 6, 'bold': False, 'align': 'center', 'valign': 'vcenter',
        'border': 1, 'text_wrap': True,
    }
    big_header = {
        'font': '宋体', 'font_size': 10, 'bold': False, 'align': 'left', 'valign': 'vcenter',
        'border': True, 'text_wrap': False,
    }
    big_body = {
        'font': '宋体', 'font_size': 10, 'bold': False, 'align': 'left', 'valign': 'vcenter',
        'border': False, 'text_wrap': False,
    }
