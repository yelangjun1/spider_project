import requests
from lxml import etree
import xlwt

class zhonghua:
    def __init__(self,data):
        self.url = "http://campus.chinahr.com/qz/"
        self.post_data = {
            'keyword': data
        }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'campus.chinahr.com',
            'Referer': 'http://campus.chinahr.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        self.workbook = xlwt.Workbook(encoding="utf-8")
        self.worksheet = self.workbook.add_sheet("中华英才网")
        self.k = 1
    def request_url(self):
        data = requests.get(self.url, params=self.post_data, headers=self.headers)
        self.deal_data(data)
    def deal_data(self,data):
        html = etree.HTML(data.text)
        job_link = html.xpath('//dd[@class="item"]/div[@class="top-area"]/a/@href')
        job_name = html.xpath('//dd[@class="item"]/div[@class="top-area"]/a/text()')
        company = html.xpath('//dd[@class="item"]/div[@class="top-area"]/span/text()')
        job_salary = html.xpath('//dd[@class="item"]/div[@class="center-area"]/div[@class="job-info"]/strong/text()')
        job_place = html.xpath(
            '//dd[@class="item"]/div[@class="center-area"]/div[@class="job-info"]/span[@class="job-city Fellip"]/text()')
        job_info = html.xpath('//dd[@class="item"]/div[@class="center-area"]/div[@class="job-info"]/text()')
        industry_name = html.xpath('//dd[@class="item"]/div[@class="center-area"]/span[@class="industry-name"]/text()')
        span_time = html.xpath('//dd[@class="item"]/div[@class="bottom-area"]/span[@class="slant"]/text()')
        self.write_data(job_link,job_name,company,job_salary,job_place,job_info,industry_name,span_time)
    def write_data(self,job_link,job_name,company,job_salary,job_place,job_info,industry_name,span_time):
        for i in range(len(job_name)):
            self.worksheet.write(self.k, 0, job_link[i])
            self.worksheet.write(self.k, 1, job_name[i])
            self.worksheet.write(self.k, 2, company[i])
            self.worksheet.write(self.k, 3, job_salary[i])
            self.worksheet.write(self.k, 4, job_place[i])
            self.worksheet.write(self.k, 5, job_info[i])
            self.worksheet.write(self.k, 6, industry_name[i])
            self.worksheet.write(self.k, 7, span_time[i])
            self.k += 1
    def save(self):
        self.workbook.save("中华英才网.xls")
    def main(self):
        self.request_url()
        self.save()
if __name__ == '__main__':
    a = zhonghua("爬虫")
    a.main()