import requests
import re
import json
import xlwt

class taobao_spider(object):
    def __init__(self,k,param):
        self.url = "https://s.taobao.com/search"
        self.headers = {
                            'cookie':'enc=hQS1paBIDeYNiuHHoz6FbVsdWn16t2%2BFz2yFhdE4qnfm0KkA6RuOFPiXmLs0AiyPznFV3GkgADsIC2qNJ33Bnw%3D%3D; miid=520257131293329594; cna=ebDvFW6xBB0CARstNda8d602; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; t=923f0feff367bce6f711ce5e61f21ad4; __guid=154677242.2257091212342880000.1577959891440.4634; JSESSIONID=B7E27629CB737335BBB38166A0F415E5; monitor_count=2; l=dBMvs78nqFLeHysEBOCii599WbQtsIRAguo1WX3Ji_5Ia6Lsvs7OoXOLmFp6cjWftAYB4IFj7TJ9-etkiKy06Pt-g3fPixDc.; isg=BFNTh7p1CXdQIsbGN9mGYdrg4te9oOeiHB0yewVwpnKphHMmjdpDGm7WurRPJD_C',
                            'referer':'https://s.taobao.com/search/?',
                            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                            }
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.worksheet = self.workbook.add_sheet('dataset')
        self.num = 0
        self.k = k
        self.param = param

    def find_word(self,reg, text):
        reg = re.compile(reg, re.S)
        target = re.findall(reg, text)
        return target

    def taobao_data(self):
        for i in range(self.k):
            params = {
                'q': self.param,
                'imgfile': '',
                'js': '1',
                'stats_click:search_radio_all': '1',
                'initiative_id': 'staobaoz_20200102',
                'ie': 'utf8',
                's':'{0}'.format(i * 44)
            }
            data = requests.get(self.url, headers=self.headers, params=params)
            b = self.find_word("g_page_config = (.*?)};", data.text)[0]
            c = b + "}"
            d = json.loads(c)
            data = d['mods']['itemlist']['data']['auctions']
            self.save_data(data)

    def save_data(self,data):
        for i in data:
            self.worksheet.write(self.num, 0, i["nid"])
            self.worksheet.write(self.num, 1, i["raw_title"])
            self.worksheet.write(self.num, 2, i["title"])
            self.worksheet.write(self.num, 3, i["pic_url"])
            self.worksheet.write(self.num, 4, i["detail_url"])
            self.worksheet.write(self.num, 5, i["view_price"])
            self.worksheet.write(self.num, 6, i["item_loc"])
            self.worksheet.write(self.num, 7, i["nick"])
            self.worksheet.write(self.num, 8, i["user_id"])
            self.num += 1

    def main(self):
        self.taobao_data()
        self.workbook.save("taobao.xls")

if __name__ == '__main__':
    a = taobao_spider(3,"手机")
    a.main()