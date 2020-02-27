import requests
from lxml import etree
import re
import xlwt
import time

class weixin_passage:
    def __init__(self,search):
        self.url = "https://weixin.sogou.com/weixin?"
        self.params = {'query': search,
                  '_sug_type_': '',
                  'sut': '5820',
                  'lkt': '4,1582529217246,1582529223083',
                  's_from': 'input',
                  '_sug_': 'y',
                  'type': '2',
                  'sst0': '1582529223187',
                  'page': '1',
                  'ie': 'utf8',
                  'w': '01019900',
                  'dr': '1'}
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': 'ABTEST=5|1582529211|v1; IPLOC=CN4407; SUID=936722B7721A910A000000005E537ABB; SUID=936722B71E20910A000000005E537ABC; weixinIndexVisited=1; SUV=007652B8B72267935E537ABD6B990269; sct=1',
            'Host': 'weixin.sogou.com',
            'Referer': 'https://weixin.sogou.com/',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        self.workbook = xlwt.Workbook(encoding="utf-8")
        self.worksheet = self.workbook.add_sheet("微信文章")
        self.k = 1
        self.num = 0
    def request_url(self):
        data = requests.get(self.url, params=self.params, headers=self.headers)
        self.get_num(data)
    def request_url2(self,i):
        self.params['page'] = i
        data = requests.get(self.url, params=self.params, headers=self.headers)
        self.deal_data(data)
    def get_num(self,data):
        html = etree.HTML(data.text)
        search_num = html.xpath('//div[@class="mun"]/text()')[0]
        num = self.find_word('\d+', search_num)
        self.num = int("".join(num))
    def deal_data(self,data):
        html = etree.HTML(data.text)
        title = [i.xpath('string(.)') for i in html.xpath('//div[@class="txt-box"]/h3/a')]
        link = html.xpath('//div[@class="txt-box"]/h3/a/@href')
        txt_info = [i.xpath('string(.)') for i in html.xpath('//div[@class="txt-box"]/p[@class="txt-info"]')]
        gongzong_link = html.xpath('//div[@class="txt-box"]/div[@class="s-p"]/a/@href')
        gongzong_name = html.xpath('//div[@class="txt-box"]/div[@class="s-p"]/a/text()')
        self.write_data(title,link,txt_info,gongzong_link,gongzong_name)
    def write_data(self,title,link,txt_info,gongzong_link,gongzong_name):
        for i in range(len(title)):
            self.worksheet.write(self.k, 0, title[i])
            self.worksheet.write(self.k, 1, link[i])
            self.worksheet.write(self.k, 2, txt_info[i])
            self.worksheet.write(self.k, 3, gongzong_link[i])
            self.worksheet.write(self.k, 4, gongzong_name[i])
            # self.worksheet.write(self.k, 5, fabu_time[i])
            self.k += 1
    def find_word(self,reg,text):
        reg = re.compile(reg, re.S)
        target = re.findall(reg, text)
        return target
    def save(self):
        self.workbook.save("微信文章.xls")
    def main(self):
        self.request_url()
        for i in range(self.num//10):
            self.request_url2(i+1)
            print(i+1)
            print(self.k)
            time.sleep(1)
        self.save()
if __name__ == '__main__':
    a = weixin_passage("爬虫")
    a.main()