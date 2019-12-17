"""
2019-12-17 百度文库爬虫
"""
import requests,json
import re
def find_word(reg,text):
    reg = reg
    reg = re.compile(reg,re.S)
    target = re.findall(reg,text)
    return target

url = input("--------------------------------------------------------------------"+"\n"
            "--------------------------------------------------------------------"+"\n"
            "请输入百度文库的网址： ")
a = requests.get(url)
a.encoding="gbk"
name = find_word(r'<span id="doc-tittle-0">(.*?)</span>',a.text)[0]
print(name)
a = find_word(r'WkInfo.htmlUrls = (.*?);',a.text)[0]
b = find_word(r'pageLoadUrl\\x22:\\x22(.*?)\\x22}',a)
for i in b:
    i = i.replace("\\\\\\","")
    print("----------")
    try:
        b = requests.get(i)
        c = find_word(r'wenku_\d+\((.*?)\}\)', b.text)[0]
        c = c+"}"
        d = json.loads(c)
        data = ""
        e = find_word(r"{'c': '(.*?)',.*?'ps': (.*?),.*?,", str(d))
        for i in e:
            data += str(i[0])
            if str(i[1]) == "None":
                pass
            else:
                data += "\n"
        print(data)
        with open(str(name)+".doc","a")as f:
            f.write(data)
    except:
        pass
print("-----------------下载完成----------------")
a = input("---------please press any key to out------")

