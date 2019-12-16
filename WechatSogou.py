"""
2019-12-16 微信文章爬虫
"""
import requests
from lxml import etree

class wechat_passage:
    def __init__(self,type,query,page):
        self.url_1 = "https://weixin.sogou.com/"
        self.url_2 = "https://weixin.sogou.com/weixin"
        self.headers_1 = {
                            'Host':'weixin.sogou.com',
                            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                         }
        self.type = type
        self.sess = requests.Session()
        self.params = {
                        'type':type,
                        'query':query,
                        'page':page
                    }
    def sess_request(self):
        self.sess.get(self.url_1, headers=self.headers_1)
    def data_request(self):
        data_2 = self.sess.get(self.url_2, params=self.params, headers=self.headers_1)
        data_2.encoding = "utf-8"
        html = etree.HTML(data_2.text)
        if(self.type == 1):
            self.deal_with_data(html)
        elif(self.type == 2):
            self.deal_with_data_2(html)
    def deal_with_data(self,html):
        data = html.xpath('//li[contains(@id,"sogou_vr_11002301_box")]')[0]
        img = data.xpath('//div[@class="img-box"]/a[contains(@uigs,"account_image_")]/img/@src')
        title_link = data.xpath('//div[@class="txt-box"]/p[@class="tit"]/a[contains(@uigs,"account_name_")]/@href')
        titles = data.xpath('//div[@class="txt-box"]/p[@class="tit"]/a[contains(@uigs,"account_name_")]')
        title = [title.xpath("string(.)") for title in titles]
        infos = data.xpath('//div[@class="txt-box"]/p[@class="info"]')
        info = [info.xpath("string(.)") for info in infos]
        introduceds = data.xpath('//dl[1]')
        introduced = [introduced.xpath("string(.)") for introduced in introduceds]
        wechat_qrcode = data.xpath('//div[@class="ew-pop"]/span[@class="pop"]/img[1]/@src')
        data_list = []
        data_dict = {}
        for i in range(len(title)):
            data_dict["title"] = title[i]
            data_dict["img"] = "https://weixin.sogou.com" + img[i]
            data_dict["title_link"] = "https://weixin.sogou.com" + title_link[i]
            data_dict["info"] = info[i].replace("\n", "")
            data_dict["introduced"] = introduced[i].replace("\n", "")
            data_dict["wechat_qrcode"] = wechat_qrcode[i]
            data_list.append(data_dict)
            data_dict = {}
        print(data_list)
        return data_list
    def deal_with_data_2(self,html):
        data = html.xpath('//li[contains(@id,"sogou_vr")]')[0]
        img = data.xpath('//div[@class="img-box"]//img/@src')
        title_link = data.xpath('//div[@class="txt-box"]/h3/a/@href')
        titles = data.xpath('//div[@class="txt-box"]/h3/a')
        title = [title.xpath("string(.)") for title in titles]
        infos = data.xpath('//div[@class="txt-box"]/p')
        info = [info.xpath("string(.)") for info in infos]
        gongzong_names_link = data.xpath('//div[@class="txt-box"]/div[@class="s-p"]/a/@href')
        gongzong_names = data.xpath('//div[@class="txt-box"]/div[@class="s-p"]/a/text()')
        time = data.xpath('//div[@class="txt-box"]/div[@class="s-p"]/@t')
        data_list = []
        data_dict = {}
        for i in range(len(title)):
            data_dict["title"] = title[i]
            data_dict["img"] = "https://weixin.sogou.com" + img[i]
            data_dict["title_link"] = "https://weixin.sogou.com" + title_link[i]
            data_dict["info"] = info[i].replace("\n", "")
            data_dict["gongzong_names"] = gongzong_names[i].replace("\n", "")
            data_dict["gongzong_names_link"] = "https://weixin.sogou.com" + gongzong_names_link[i]
            data_dict["time"] = time[i]
            data_list.append(data_dict)
            data_dict = {}
        print(data_list)
        return data_list
    def main(self):
        self.sess_request()
        self.data_request()

if __name__ == '__main__':
    a = wechat_passage(type=1,query="python",page=1)
    a.main()