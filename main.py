import datetime
import os

import json
import pandas as pd

from db import Database

directory = 'json'

# 获取目录下的所有文件和子目录
all_files = os.listdir(directory)

# 只保留文件
files = [f for f in all_files if os.path.isfile(os.path.join(directory, f))]

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
print(timestamp)
excel_name = 'out_put/item.xlsx'
out_put_list = []
rank_list = {}
for file in files:
    print('file: ', file)
    data = json.load(open('json/'+file, encoding="utf-8-sig"))

    db = Database()

    bis_list = data['result']['pageContext']['bisList']
    main_data = data['result']['pageContext']['spec'].rsplit('-', 1)
    tianfu = main_data[0]
    zhiye = main_data[1]
    bb = {}
    item_list = {}
    file = open('output.csv', 'w')

    for bis in bis_list:
        print(bis)
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
            the_item['item_id'] = db.get_item_id(the_item['name'])
            out_put_list.append(the_item)
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
                            'item_id': db.get_item_id(gems['name']),

                        }
                        print(gems_item)
                        out_put_list.append(gems_item)
print(len(out_put_list))
df = pd.DataFrame(out_put_list)
db.close()
df.to_excel(excel_name,  index=False)
