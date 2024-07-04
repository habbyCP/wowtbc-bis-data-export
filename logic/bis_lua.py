import pandas as pd


class BisLua:

    def __init__(self, item_file):
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
        print(self.class_specs)

    def make_unique_phase(self):
        unique_phase = self.excel['phase'].unique()
        print(unique_phase)

    def make_unique_slot(self):
        self.unique_slot = self.excel['slot'].unique()
        print(self.unique_slot)

    def make_bis_lua(self):
        self.make_unique_class_specs()
        self.make_unique_phase()
        self.make_unique_slot()
        for class_key, specs_inner in self.class_specs.items():
            for spec in specs_inner:
                print(class_key, spec)
