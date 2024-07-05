import os

from logic.bis_lua import BisLua
from logic.get_json import WowTbcCurl
from logic.json_to_excel import ExcelData


def get_web_content():
    # 下载 json 文件
    content = WowTbcCurl()
    content.get_files(os.getcwd() + '/json')


def json_to_excel():
    # 下载的 json 文件中的文件信息都保存到 excel 中
    format_data = ExcelData(os.getcwd() + '/json')
    for file in format_data.files:
        format_data.get_file_count(file)
    format_data.save()


def make_bis_lua_file():
    the_dir = os.path.join(os.getcwd(), 'out_put')
    if not os.path.exists(the_dir):
        os.mkdir(the_dir)
    print('请选择 bis 清单文件')
    all_files = os.listdir(the_dir)
    for num in range(len(all_files)):
        print('%s. %s' % (num, all_files[num]))
    the_choice = int(input('请输入选择:'))
    if the_choice >= len(all_files):
        print('输入有误')
        exit(1)
    file_path = os.path.join(the_dir, all_files[the_choice])
    bis_dir = os.path.join(os.getcwd(), 'lua_file')
    if not os.path.exists(bis_dir):
        os.mkdir(bis_dir)
    # 生成 lua 的 bis 文件
    bis = BisLua(file_path, bis_dir)
    bis.make_bis_lua()


if __name__ == '__main__':
    print('解析工具')
    print('请选择操作')
    select_list = ['1.下载 json 文件', '2.生成 excel 文件', '3.生成 bis 清单lua文件', '4.生成 item 清单', '5.退出']
    for i in select_list:
        print(f"{i}")
    try:
        choice = int(input('请输入选择:'))
        if choice == 1:
            get_web_content()
        elif choice == 2:
            json_to_excel()
        elif choice == 3:
            make_bis_lua_file()
        elif choice == 4:
            pass
        elif choice == 5:
            exit(1)
        else:
            print('输入有误')
            exit(1)
    except ValueError:
        print('所输入的不是数字')
