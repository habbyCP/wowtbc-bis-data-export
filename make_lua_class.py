import pandas as pd

from classes import zhiye_tianfu, slot, phase
from jinja2 import Template


def make_tianfu():
    Bistooltip_wh_bislists = {}
    df = pd.read_excel('out_put/item.xlsx')
    unique_zhiye = df['zhiye'].unique()
    for zhiye in unique_zhiye:
        print(zhiye)
        Bistooltip_wh_bislists[zhiye] = {}
        unique_tianfu = df[df['zhiye'] == zhiye]['tianfu'].unique()
        for tianfu in unique_tianfu:
            print(tianfu)
            Bistooltip_wh_bislists[zhiye][tianfu] = {}

    print(Bistooltip_wh_bislists)


def make_phase():
    df = pd.read_excel('out_put/item.xlsx')
    unique_phase = df['phase'].unique()
    print(unique_phase)


def make_slot():
    df = pd.read_excel('out_put/item.xlsx')
    unique_slot = df['slot'].unique()
    print(unique_slot)


def make_data():
    # 读取模板文件内容
    with open('template.txt', 'r') as file:
        template_content = file.read()
    file = open('bis_list.lua', 'w')
    # 创建模板
    template = Template(template_content)
    df = pd.read_excel('out_put/item.xlsx')
    file.write(f'Bistooltip_bislists = {{}};\n')
    for zhiye, value in zhiye_tianfu.items():
        file.write(f'Bistooltip_bislists["{zhiye}"] = {{}};\n')
        for tianfu, _ in value.items():
            file.write(f'Bistooltip_bislists["{zhiye}"]["{tianfu}"] = {{}};\n')
            for p in phase:
                sort = 1
                for s in slot:
                    bis_list = df[(df['zhiye'] == zhiye) & (df['tianfu'] == tianfu) & (df['phase'] == p) & (
                            df['slot'] == s) & (
                                          df['type'] == 'bis')].sort_values(by='value', ascending=False).to_dict(
                        orient='records')
                    enhs_list = df[(df['zhiye'] == zhiye) & (df['tianfu'] == tianfu) & (df['phase'] == p) & (
                            df['slot'] == s) & (
                                           df['type'] == 'gems')].sort_values(by='value', ascending=False).to_dict(
                        orient='records')
                    enhs_string = ''
                    enhs_num = 1
                    for enhs in enhs_list:
                        enhs_string += '[' + str(enhs_num) + '] = {["type"] = "item",["id"] = ' + str(
                            enhs['item_id']) + ' },'
                        enhs_num = enhs_num + 1

                    bis_string = ''
                    bis_num = 1
                    for bis in bis_list:
                        if bis_num > 6: break
                        bis_string += f'[{bis_num}] = {bis["item_id"]},'
                        bis_num = bis_num + 1
                    if len(bis_string) == 0: break
                    data = {
                        'zhiye': zhiye,
                        'tianfu': tianfu,
                        'phase': p,
                        'slot': s,
                        'sort': sort,
                        'enhs': enhs_string.rstrip(','),
                        'bis': bis_string.rstrip(',')
                    }

                    # 渲染模板
                    output = template.render(data)
                    output += '\n'
                    sort += 1
                    file.write(output)
    file.close()

make_data()
