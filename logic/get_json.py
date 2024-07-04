import os

import requests


class WowTbcCurl:
    def __init__(self):
        self.url_list = ['https://wowtbc.gg/page-data/bis-list/beast-mastery-hunter/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/survival-hunter/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/marksmanship-hunter/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/fire-mage/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/arcane-mage/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/frost-mage/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/holy-priest/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/shadow-priest/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/arms-warrior/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/fury-warrior/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/protection-warrior/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/holy-paladin/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/protection-paladin/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/retribution-paladin/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/balance-druid/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/restoration-druid/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/feral-dps-druid/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/feral-tank-druid/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/combat-rogue/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/subtlety-rogue/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/assassination-rogue/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/elemental-shaman/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/enhancement-shaman/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/restoration-shaman/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/affliction-warlock/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/demonology-warlock/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/destruction-warlock/page-data.json',
                         'https://wowtbc.gg/page-data/bis-list/destruction-fire-warlock/page-data.json']

    def get_files(self, path):
        # 下载并保存文件
        for url in self.url_list:
            response = requests.get(url)
            names = url.split('/')
            # 检查请求是否成功
            if response.status_code == 200:
                # 从 URL 中提取文件名
                filename = names[5] + '.json'
                filename = os.path.join(path, filename)
                # 将响应内容写入文件
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print(f"File saved as {filename}")
            else:
                print(f"Request failed with status code: {response.status_code}")
