"""
只是用来测试从别处找来的代码的，没有什么实际用途
"""
import xlwt
work_book=xlwt.Workbook(encoding='utf-8')
sheet=work_book.add_sheet('sheet表名')
sheet.write(0,0,'第一行第一列')
sheet.write(0,1,'第一行第二列')
work_book.save('Excel表.xls')

