"""
2019-12-16
"""
import requests
from lxml import etree
class weibo:
    def __init__(self,word):
        self.url = "http://www.baidu.com"
        self.url_3 = "https://s.weibo.com/weibo/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        self.params = {
            "key": word
        }
    def url_creare(self):
        data = requests.get(self.url, params=self.params)
        data = str(data.url).split("=")[1].replace("%", "%25")
        data = requests.get(self.url_3 + data, headers=self.headers)
        self.deal_with_data(data)
    def deal_with_data(self,data):
        data_list = []
        data_dict = {}
        html = etree.HTML(data.text)
        url_link = html.xpath('//div[@class="card-wrap "]/div/div[@class="avator"]/a/@href')
        url_img = html.xpath('//div[@class="card-wrap "]/div/div[@class="avator"]/a/img/@src')
        name = html.xpath('string(//div[@class="card-wrap "]/div/div[@class="info"]/div/a[1])')
        loca = html.xpath('string(//div[@class="card-wrap "]/div/div[@class="info"]/p[1])')
        intro = html.xpath('string(//div[@class="card-wrap "]/div/div[@class="info"]/p[2])')
        num = html.xpath('string(//div[@class="card-wrap "]/div/div[@class="info"]/p[3])')
        introduce = html.xpath('string(//div[@class="card-wrap "]/div/div[@class="info"]/p[4])')
        data_dict['url_link'] = url_link
        data_dict['url_img'] = url_img
        data_dict['name'] = name
        data_dict['loca'] = loca.replace(" ","").replace("\n","")
        data_dict['intro'] = intro
        data_dict['url_link'] = url_link
        data_dict['num'] = num.replace(" ","").replace("\n","")
        data_dict['introduce'] = introduce
        data_list.append(data_dict)
        print(data_list)
    def main(self):
        self.url_creare()
if __name__ == '__main__':
    a = weibo(word="家有大猫")
    a.main()



