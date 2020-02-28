import requests
from lxml import etree
import xlwt
class JingDong:
    def __init__(self):
        # self.url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&page={0}&s={1}&click=0"
        self.url = "https://search.jd.com/Search"
        self.params = {
            'keyword':"手机",
            "enc":"utf-8",
            "page":"",
            "s":"",
            "click":"0",
        }
        self.headers = {
            'referer': 'https://www.jd.com/?cu=true&utm_source=haosou-search&utm_medium=cpc&utm_campaign=t_262767352_haosousearch&utm_term=5512151796_0_93eeb39dece24b618db212d99285caef',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        self.workbook = xlwt.Workbook()
        self.worksheet = self.workbook.add_sheet("京东商品数据")
        self.sess = requests.Session()
        self.k = 1
    def jingdong(self,data):
        html = etree.HTML(data)
        title = html.xpath('//div[@class="gl-i-wrap"]/div[@class="p-img"]/a/@title')
        pic_url = html.xpath('//div[@class="gl-i-wrap"]/div[@class="p-img"]/a/@href')
        img_url = html.xpath('//div[@class="gl-i-wrap"]/div[@class="p-img"]/a[@target="_blank"]/img/@source-data-lazy-img')
        price = html.xpath('//div[@class="gl-i-wrap"]/div[@class="p-price"]//i/text()')
        shop = html.xpath('//div[@class="gl-i-wrap"]/div[@class="p-shop"]//a/@title')
        self.write_data(title,pic_url,img_url,price,shop)
        print(price)
    def get_request(self,url,params,headers):
        data = self.sess.get(url,params=params,headers=headers)
        data.encoding = "utf-8"
        self.jingdong(data.text)
    def write_data(self,title,pic_url,img_url,price,shop):
        for i in range(len(title)):
            self.worksheet.write(self.k,0,title[i])
            self.worksheet.write(self.k, 1, pic_url[i])
            self.worksheet.write(self.k, 2, img_url[i])
            # self.worksheet.write(self.k, 3, price[i])
            # self.worksheet.write(self.k, 4, shop[i])
            self.k += 1
    def save(self):
        self.workbook.save("京东商品数据.xls")
    def main(self):
        for i in range(0,3):
            self.params["page"] = 1+2*i
            self.params["s"] = 1+6*i
            self.get_request(self.url,self.params,self.headers)
        self.save()


if __name__ == '__main__':
    b = JingDong()
    b.main()

