# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt
class TiebaPipeline(object):
    def __init__(self):
        # self.workbook = xlwt.Workbook()
        # self.sheet = self.workbook.add_sheet('sheet1')
        # self.a = 0
        # -------------------------------
        self.f = open("a.html","a")
        a = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>'
        self.f.write(a)
    def process_item(self, item, spider):
        for i in item['content']:
            if "pan"in str(i):
                b = "http://tieba.baidu.com"+str(item['url2'][0]).split("?")[0]
                self.f.write('<a href="{0}">{1}</a>'.format(b,i)+"<br>")

        # --------------------------------------
        # for i in item['content']:
        #     if "pan"in str(i):
        #         b = "http://tieba.baidu.com"+str(item['url2'][0]).split("?")[0]
        #         self.sheet.write(self.a,1,str(i))
        #         self.sheet.write(self.a,0,str(b))
        #         self.a+=1
        #     else:
        #         pass
        #
        # self.workbook.save("1.xls")
        return item
    def file_close(self):
        # self.workbook.save("1.xls")
        self.f.close()