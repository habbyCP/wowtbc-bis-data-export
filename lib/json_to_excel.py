import datetime
import logging
import os

import json
import pandas as pd


class ExcelData:
    # 类，转换json 数据到 execl
    def __init__(self, base_path):
        directory = base_path + '/json'
        # 获取目录下的所有文件和子目录
        all_files = os.listdir('json')
        self.files = []
        # 需要解析的 json 文件清单
        for f in all_files:
            # 完整的文件路径
            f = os.path.join(directory, f)
            if os.path.isfile(f):
                self.files.append(f)
        # 生成 excel 文件路径
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.excel_name = f'{base_path}/out_put/item_{timestamp}.xlsx'
        self.item_map = {}
        # 获取装备 名字和 id 的清单
        excel = pd.read_excel('item_map.xlsx')
        for row in excel.to_dict(orient='records'):
            # 名字转小写，提高命中率
            try:
                row['name'] = row['name'].lower()
                self.item_map[row['name']] = row['entry']
            except Exception as e:
                logging.error(f'excel {row} error: {e}', exc_info=True)

        # 需要输出的数据清单
        self.out_put_list = []

    def get_item_id(self, name):
        # 这段代码定义了一个get_item_id方法，
        # 接受一个name参数，
        # 并检查name是否在item_map中。
        # 如果找到了name，则返回item_map中对应的值。
        # 如果未找到name，则记录一个警告消息并返回0。
        # 名字转小写，提高命中率
        name = name.lower()
        if name in self.item_map:
            return self.item_map[name]
        else:
            logging.warning("没有找到 %s 的 id" % name)
            return 0

    def get_file_count(self, file_path):
        data = json.load(open(file_path, encoding="utf-8-sig"))
        bis_list = data['result']['pageContext']['bisList']
        main_data = data['result']['pageContext']['spec'].rsplit('-', 1)
        tianfu = main_data[0]
        zhiye = main_data[1]
        for bis in bis_list:
            # 循环阶段
            for phase in bis['phase']:
                if 'name' not in bis:
                    continue
                the_item = {
                    'name': bis['name'],
                    'value': bis['value'],
                    'phase': phase,
                    'slot': bis['slot'],
                    'type': 'bis',
                    'tianfu': tianfu,
                    'zhiye': zhiye
                }
                the_item['item_id'] = self.get_item_id(the_item['name'])
                self.out_put_list.append(the_item)
                # 获取在当前阶段的 bis 信息
                other_bis = bis[phase.lower()]
                # 如果是 bis，责获取宝石和附魔的信息
                if ('bis' in other_bis) and other_bis['bis']:
                    if 'gems' in other_bis:
                        for gems in other_bis['gems']:
                            gems_item = {
                                'name': gems['name'],
                                'value': 0,
                                'phase': phase,
                                'slot': bis['slot'],
                                'type': 'gems',  # 类型宝石
                                'tianfu': tianfu,
                                'zhiye': zhiye,
                                'item_id': self.get_item_id(gems['name']),
                            }
                            self.out_put_list.append(gems_item)

    def save(self):
        df_all = pd.DataFrame(self.out_put_list)
        df_all.to_excel(self.excel_name, index=False)
