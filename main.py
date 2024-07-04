import os

from lib.json_to_excel import ExcelData

if __name__ == '__main__':

    # 下载的 json 文件中的文件信息都保存到 excel 中
    format_data = ExcelData(os.getcwd())
    for file in format_data.files:
        format_data.get_file_count(file)
    format_data.save()
