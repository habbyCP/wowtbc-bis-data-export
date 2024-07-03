import pandas as pd

from classes import zhiye_tianfu, slot, phase_list
from jinja2 import Template
from functools import lru_cache


class Item:
    def __init__(self):
        self.main_table = pd.read_excel('out_put/item.xlsx')
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
        for one_item in self.main_table.to_dict(orient='records'): 
            item_id = one_item['item_id']
            zy = one_item['zhiye']
            tf = one_item['tianfu']
            slt = one_item['slot']
            ph = one_item['phase']
            if item_id not in self.bis_list:
                self.bis_list[item_id] = {}
            if zy not in self.bis_list[item_id]:
                self.bis_list[item_id][zy] = {}
            if tf not in self.bis_list[item_id][zy]:
                self.bis_list[item_id][zy][tf] = {}
        print(self.bis_list)



item = Item()
item.make_item()
