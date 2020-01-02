import requests
import re
import json
import time
class wenku_spider(object):
    def __init__(self,url):
        self.passage_url = url
        self.headers_1 = {
                            'Host':'wenku.baidu.com',
                            'Referer':'https://wenku.baidu.com/',
                            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                            }
        self.headers_2 = {
                            'Host':'wkbjcloudbos.bdimg.com',
                            'Referer':self.passage_url,
                            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                            }
        self.times = int((time.time())*1000)
    def find_word(self,reg,text):
        reg = re.compile(reg, re.S)
        target = re.findall(reg, text)
        return target
    def find_json_link(self):
        data = requests.get(self.passage_url, headers=self.headers_1)
        pageLoadUrl = self.find_word('WkInfo.htmlUrls = \'(.*?)\'', data.text)[0].replace(r'\x22', "")
        url_link = self.find_word("pageLoadUrl:(.*?)},", pageLoadUrl)
        url_2 = url_link[0].replace("\\\\\\", "")
        self.find_data(url_2)
    def find_data(self,link):
        data = requests.get(link, headers=self.headers_2)
        json_data = self.find_word("wenku_\d+\((.*?)\)", data.text)[0]
        data_content = ""
        for i in json.loads(json_data)["body"]:
            content = i["c"]
            enter = i["ps"]
            if enter:
                data_content += content
                data_content += "\n"
            else:
                data_content += content
        self.write_data(data_content)
        print(data_content)
    def write_data(self,data_content):
        with open(str(self.times)+".txt","w") as f:
            f.write(data_content)
            f.close()
    def main(self):
        self.find_json_link()
if __name__ == '__main__':
    url = "https://wenku.baidu.com/view/f1e1b912571252d380eb6294dd88d0d233d43cd1.html"
    a = wenku_spider(url)
    a.main()