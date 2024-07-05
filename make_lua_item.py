import pandas as pd

from classes import zhiye_tianfu, slot, phase_list
from jinja2 import Template
from functools import lru_cache


class Item:
    def __init__(self):
        self.main_table = pd.read_excel('out_put/item_20240705160912.xlsx')
        self.phase_list = phase_list
        self.bis_list = {}

    @lru_cache(maxsize=1000)
    def get_zhiye_tianfu_list(self, zhiye, tianfu, solt):
        return self.main_table[
            (self.main_table['zhiye'] == zhiye)
            & (self.main_table['tianfu'] == tianfu)
            & (self.main_table['solt'] == solt)
            ]

    def make_item(self):
        table = {}
        order_table = {}
        item_list = self.main_table.to_dict(orient='records')
        for order_item in item_list:
            order_table_kay = f'{order_item["zhiye"]}-{order_item["tianfu"]}-{order_item["slot"]}-{order_item["phase"]}'
            if order_table_kay not in order_table:
                order_table[order_table_kay] = []
            order_table[order_table_kay].append(order_item)
        for the_item in item_list:
            if the_item['type'] != 'bis':
                continue
            if the_item['item_id'] not in table:
                table[the_item['item_id']] = {}
            zt = f"{the_item['zhiye']}-{the_item['tianfu']}"
            if zt not in table[the_item['item_id']]:
                table[the_item['item_id']][zt] = {}
            if 'slots' not in table[the_item['item_id']][zt]:
                table[the_item['item_id']][zt]['slots'] = {}
            if the_item['slot'] not in table[the_item['item_id']][zt]['slots']:
                map_phase = {}
                for phase in phase_list:
                    map_phase[phase] = 0
                table[the_item['item_id']][zt]['slots'][the_item['slot']] = map_phase
            order_table_kay = f'{the_item["zhiye"]}-{the_item["tianfu"]}-{the_item["slot"]}-{the_item["phase"]}'
            if order_table_kay not in order_table:
                table[the_item['item_id']][zt]['slots'][the_item['slot']][the_item['phase']] = '-'
            the_rank = table[the_item['item_id']][zt]['slots'][the_item['slot']][the_item['phase']]
            for order_item in order_table[order_table_kay]:
                if order_item['value'] >= the_item['value']:
                    # 最大值到9，再大就没有意义了
                    if the_rank < 9:
                        the_rank = the_rank + 1
            table[the_item['item_id']][zt]['slots'][the_item['slot']][the_item['phase']] = the_rank

        for item_id, value in table.items():
            print(item_id, value)
            break


item = Item()
item.make_item()
