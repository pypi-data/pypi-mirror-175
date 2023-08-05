import os
from rsgz.file.files import get_files
import openpyxl


def rsgz_format(jianju, v_name,jianju_s):
    r"""
    jianju  字符串间距
    v_name  变量名
    jianju_s  批量间距
    """
    len_str = jianju - len(v_name.encode('GBK')) + len(v_name)+jianju_s
    return len_str

excel_list = get_files(r"\\R1\r1\已经完成\Excel\DDD")

# print(excel_list)
for one_file in excel_list:
    wb = openpyxl.load_workbook(one_file)

    n1 = one_file.split(os.sep)[-1]
    n2 = wb.worksheets[0].title
    n3 = wb.worksheets[-1].title
    jianju_s = -5
    print('{n1:<{len1}}'
          '{n2:<{len2}}'
          '{n3:<{len3}}'.format(n1=n1, n2=n2, n3=n3,
                                len1=rsgz_format(22, n1, jianju_s),
                                len2=rsgz_format(22, n2, jianju_s),
                                len3=rsgz_format(22, n3, jianju_s)))