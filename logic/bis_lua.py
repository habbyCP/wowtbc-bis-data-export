import pandas as pd
from jinja2 import Template


class BisLua:

    def __init__(self, item_file):
        self.big_array = None
        self.item_file = item_file
        self.class_specs = {}
        self.unique_phase = []
        self.unique_slot = []
        self.excel = pd.read_excel(self.item_file)

    def make_unique_class_specs(self):
        unique_table = self.excel[['zhiye', 'tianfu']].drop_duplicates()
        for unique in unique_table.to_dict(orient='records'):
            if unique['zhiye'] not in self.class_specs:
                self.class_specs[unique['zhiye']] = []
            self.class_specs[unique['zhiye']].append(unique['tianfu'])

    def make_unique_phase(self):
        self.unique_phase = self.excel['phase'].unique()

    def make_unique_slot(self):
        self.unique_slot = self.excel['slot'].unique()

    def make_bis_lua(self):
        self.make_unique_class_specs()
        self.make_unique_phase()
        self.make_unique_slot()
        with open('./template_class.tpl', 'r') as file:
            template_content = file.read()
        # 创建模板
        template = Template(template_content)
        sort = 0
        for the_class, specs_list in self.class_specs.items():
            for specs in specs_list:
                sort = 0
                for phase in self.unique_phase:
                    for solt in self.unique_slot:
                        item_list = (self.excel[
                                         (self.excel['zhiye'] == the_class) &
                                         (self.excel['tianfu'] == specs) &
                                         (self.excel['phase'] == phase) &
                                         (self.excel['slot'] == solt) &
                                         (self.excel['type'] == 'bis')]
                                     .sort_values(by='value', ascending=False)
                                     .to_dict(orient='records'))
                        bis_string = ''
                        enhs_string = ''
                        num = 0
                        enhs_num = 0
                        for item in item_list:
                            if item['type'] == 'enhs':
                                enhs_num = enhs_num + 1
                                enhs_string += '[' + str(enhs_num) + '] = {["type"] = "item",["id"] = ' + str(
                                    item['item_id']) + ' },'
                                enhs_num = enhs_num + 1
                            if item['type'] == 'bis':
                                num = num + 1
                                if num >= 6:
                                    break
                                bis_string += f'[{num + 1}] = {item_list[num]["item_id"]},'
                        data = {
                            'zhiye': the_class,
                            'tianfu': specs,
                            'phase': phase,
                            'slot': solt,
                            'sort': sort+1,
                            'enhs': enhs_string,
                            'bis': bis_string.rstrip(',')
                        }
                        output = template.render(data)
                        print(output)
                        exit(1)
