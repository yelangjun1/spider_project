import requests
from lxml import etree
import xlwt

class YaMaXun:
    def __init__(self,data):
        self.url = "https://www.amazon.cn/s"
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Connection': 'keep-alive',
                       'Host': 'www.amazon.cn',
                       'Sec-Fetch-Mode': 'navigate',
                       'Sec-Fetch-Site': 'same-origin',
                       'Sec-Fetch-User': '?1',
                       'Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        self.params = {
                        'k': data,
                        'page': '2',
                        '__mk_zh_CN': '亚马逊网站',
                        'qid': '1582851469',
                        'ref': 'sr_pg_2'
                        }
        self.workbook = xlwt.Workbook()
        self.worksheet = self.workbook.add_sheet("亚马逊商品数据")
        self.k = 1

    def request_url(self):
        data = requests.get(self.url, params=self.params, headers=self.headers)
        self.deal_data(data)

    def deal_data(self,data):
        html = etree.HTML(data.text)
        title = html.xpath('//div/div[@class="sg-col-inner"]/span/div/div/div[@class="a-section a-spacing-none a-spacing-top-small"]/h2/a/span/text()')
        title_link = html.xpath('//div/div[@class="sg-col-inner"]/span/div/div/div[@class="a-section a-spacing-none a-spacing-top-small"]/h2/a/@href')
        price = html.xpath('//div/div[@class="sg-col-inner"]/span/div/div/div[@class="a-section a-spacing-none a-spacing-top-small"]/div/div/a/span/span/text()')
        img_link = html.xpath('//div[@class="a-section a-spacing-medium"]/span[@class="rush-component"]/a/div/img/@src')
        self.write_data(title,title_link,price,img_link)

    def write_data(self,title,title_link,price,img_link):
        for i in range(len(title)):
            self.worksheet.write(self.k,0,title[i])
            self.worksheet.write(self.k, 1, title_link[i])
            self.worksheet.write(self.k, 2, price[i])
            self.worksheet.write(self.k, 3, img_link[i])
            self.k += 1

    def save_data(self):
        self.workbook.save("亚马逊商品数据爬虫.xls")


    def main(self):
        for i in range(3):
            self.params["page"] = i+1
            self.params["ref"] = 'sr_pg_'+str(i+1)
            self.request_url()
            print(i)
        self.save_data()


if __name__ == '__main__':
    a = YaMaXun("手机")
    a.main()
