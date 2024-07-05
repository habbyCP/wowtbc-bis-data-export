import datetime
import logging
import os

import pandas as pd
from jinja2 import Template


class BisLua:

    def __init__(self, item_file, the_dir):
        self.big_array = None
        self.item_file = item_file
        self.class_specs = {}
        self.unique_phase = []
        self.unique_slot = []
        logging.warning(f'读取 excel 文件 {self.item_file}')
        self.excel = pd.read_excel(self.item_file)
        bis_file = os.path.join(the_dir, f'bis_{datetime.datetime.now().strftime("%Y%m%d%H%M")}.lua')
        self.bis_file = open(bis_file, 'w')

    def __del__(self):
        logging.warning(f'关闭 lua 文件 {self.bis_file.name}')
        self.bis_file.close()

    def write_file(self, content):
        self.bis_file.write(content)

    def make_unique_class_specs(self):
        logging.warning(f'生成唯一的职业和天赋清单')
        unique_table = self.excel[['zhiye', 'tianfu']].drop_duplicates()
        for unique in unique_table.to_dict(orient='records'):
            if unique['zhiye'] not in self.class_specs:
                self.class_specs[unique['zhiye']] = []
            self.class_specs[unique['zhiye']].append(unique['tianfu'])

    def make_unique_phase(self):
        logging.warning(f'生成唯一的阶段清单')
        self.unique_phase = self.excel['phase'].unique()

    def make_unique_slot(self):
        logging.warning(f'生成唯一的插槽清单')
        self.unique_slot = self.excel['slot'].unique()

    def make_bis_lua(self):
        self.make_unique_class_specs()
        self.make_unique_phase()
        self.make_unique_slot()
        with open('./template_class.tpl', 'r') as file:
            template_content = file.read()
        # 创建模板
        template = Template(template_content)
        for the_class, specs_list in self.class_specs.items():
            self.write_file(f'Bistooltip_wh_bislists["{the_class}"] = {{}};\n')
            for specs in specs_list:
                logging.warning(f'生成 {the_class} {specs} 的 bis lua')
                self.write_file(f'Bistooltip_wh_bislists["{the_class}"]["{specs}"] = {{}};\n')
                for phase in self.unique_phase:
                    self.write_file(f'Bistooltip_wh_bislists["{the_class}"]["{specs}"]["{phase}"] = {{}};\n')
                    sort = 0
                    for solt in self.unique_slot:
                        item_list = (self.excel[
                                         (self.excel['zhiye'] == the_class) &
                                         (self.excel['tianfu'] == specs) &
                                         (self.excel['phase'] == phase) &
                                         (self.excel['slot'] == solt)]
                                     .sort_values(by='value', ascending=False)
                                     .to_dict(orient='records'))
                        bis_string = ''
                        enhs_string = ''
                        num = 0
                        enhs_num = 0
                        for item in item_list:
                            if item['type'] == 'gems':
                                enhs_num = enhs_num + 1
                                enhs_string += '[' + str(enhs_num) + '] = {["type"] = "item",["id"] = ' + str(
                                    item['item_id']) + ' },'
                            if item['type'] == 'bis':
                                if num >= 6:
                                    continue
                                num = num + 1
                                bis_string += f'[{num}] = {item["item_id"]},'
                        if bis_string == '':
                            continue
                        sort = sort + 1
                        data = {
                            'zhiye': the_class,
                            'tianfu': specs,
                            'phase': phase,
                            'slot': solt,
                            'sort': sort,
                            'enhs': enhs_string,
                            'bis': bis_string.rstrip(',')
                        }
                        output = template.render(data)
                        self.write_file(output+"\n")
