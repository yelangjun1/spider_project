import requests
from lxml import etree
import xlwt
import time
from tqdm import trange
class dangdang:
    def __init__(self,data):
        self.url = "http://search.dangdang.com/"
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           # 'Cookie': 'ddscreen=2; dest_area=country_id%3D9000%26province_id%3D111%26city_id%20%3D0%26district_id%3D0%26town_id%3D0; __permanent_id=20200225090854645997713415417480561; __visit_id=20200225090854731218159408050962911; __out_refer=; __rpm=%7Cmix_317715...1582592943105; __trace_id=20200225090903112134763175744867544',
           'Host': 'search.dangdang.com',
           'Referer': 'http://www.dangdang.com/',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        self.params = {
                        'key':data,
                        'act':'input',
                        'page_index':'1'
                        }
        self.k = 1
        self.workbook = xlwt.Workbook()
        self.worksheet = self.workbook.add_sheet("当当网数据表")
    def request_url(self):
        data = requests.get(self.url, params=self.params, headers=self.headers)
        self.deal_data(data)
    def deal_data(self,data):
        html = etree.HTML(data.text)
        title = html.xpath('//ul[@class="bigimg"]/li/p[@class="name"]/a/@title')
        title_link = html.xpath('//ul[@class="bigimg"]/li/p[@class="name"]/a/@href')
        detail = html.xpath('//ul[@class="bigimg"]/li/p[@class="detail"]/text()')
        search_now_price = html.xpath('//ul[@class="bigimg"]/li/p[@class="price"]/span[@class="search_now_price"]/text()')
        search_pre_price = html.xpath('//ul[@class="bigimg"]/li/p[@class="price"]/span[@class="search_pre_price"]/text()')
        search_discount = html.xpath('//ul[@class="bigimg"]/li/p[@class="price"]/span[@class="search_discount"]/text()')
        search_star_line = html.xpath('//ul[@class="bigimg"]/li/p[@class="search_star_line"]/a/text()')
        search_book_author = [i.xpath('string(.)') for i in html.xpath('//ul[@class="bigimg"]/li/p[@class="search_book_author"]')]
        self.write_data(title,title_link,detail,search_now_price,search_pre_price,search_discount,search_star_line,search_book_author)
    def write_data(self,title,title_link,detail,search_now_price,search_pre_price,search_discount,search_star_line,search_book_author):
        for i in range(len(title)):
            self.worksheet.write(self.k, 0,title[i])
            self.worksheet.write(self.k, 1, title_link[i])
            # self.worksheet.write(self.k, 2, detail[i])
            self.worksheet.write(self.k, 2, title[i])
            self.worksheet.write(self.k, 3, search_now_price[i])
            self.worksheet.write(self.k, 4, search_pre_price[i])
            # self.worksheet.write(self.k, 5, search_discount[i])
            self.worksheet.write(self.k, 5, search_star_line[i])
            self.worksheet.write(self.k, 6, search_book_author[i])
            self.k += 1
    def save(self):
        self.workbook.save("当当网数据表.xls")
    def main(self):
        for i in trange(2):
            self.request_url()
            self.params['page_index'] = i+1
            time.sleep(2)
        self.save()
if __name__ == '__main__':
    a = dangdang('python')
    a.main()
