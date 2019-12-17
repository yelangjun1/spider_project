# -*- coding: utf-8 -*-
import scrapy

from tieba.items import TiebaItem
class BbbSpider(scrapy.Spider):
    name = 'bbb'
    # allowed_domains = ['web']
    a = 50
    start_urls = ['http://tieba.baidu.com/f?kw=pr&ie=utf-8&pn='+str(a)]
    url = 'http://tieba.baidu.com/f?kw=pr&ie=utf-8&pn='
    def parse(self, response):
        item = TiebaItem()
        item['name'] = response.xpath('//div[@class="threadlist_lz clearfix"]//a[@class="j_th_tit "]/@title').extract()
        item['url'] = response.xpath('//div[@class="threadlist_lz clearfix"]//a[@class="j_th_tit "]/@href').extract()
        item['content'] = response.xpath('//a[@class="j-no-opener-url"]//text()').extract()
        item['url2'] = response.xpath('//div[@class="louzhubiaoshi  j_louzhubiaoshi"]/a/@href').extract()
        for i in item['url']:
            i = "http://tieba.baidu.com"+str(i)
            yield scrapy.Request(i,callback=self.parse)
        yield item

        if self.a<1000:
            self.a += 50
        yield scrapy.Request(self.url+str(self.a),callback=self.parse)

    # def parse_item(self,response):
    #     item = TiebaItem()
    #     item['content'] = response.xpath('//div[@class="d_post_content j_d_post_content "]//text()').extract()
    #     yield item