"""
cloudflare 反爬流程(part1)
2020.02.01
"""
import requests
import re
import execjs
from requests.compat import urlencode, Morsel,urlparse
import time

# 计时
times = time.time()
print(times)

# 匹配字符
def find_word(reg,text):
    reg = re.compile(reg,re.S)
    target = re.findall(reg,text)
    return target

# 获取必要的请求post参数，分别为r,jschl_vc,passs,jschl_answer == t
def get_post_data(data):
    r = find_word('<input type="hidden" name="r" value="(.*?)">', data.text)[0]
    jschl_vc = find_word('<input type="hidden" name="jschl_vc" value="(.*?)"/>', data.text)[0]
    passs = find_word('<input type="hidden" name="pass" value="(.*?)"/>', data.text)[0]
    pattern = re.compile('setTimeout\(function\(\)\{(.*?)f.action \+= location.hash;', re.S)
    code = pattern.findall(data.text)
    code = re.sub('\s+(t = document.*?);\s+;', '', code[0], flags=re.S)
    code = re.sub('a.value', 'value', code)
    code = re.sub('t.length', '17', code)
    code = 'function test(){' + code.strip() + ';return value;}'
    s1 = execjs.compile(code)
    t = s1.call('test')
    return r,jschl_vc,passs,t

sess = requests.Session()

# 第一个请求网址(必定返回503)
url = "https://www.biovision.com/"
# 获取域名
k = urlparse(url).netloc
# 请求头
headers = {
'authority':k,
'method':'GET',
'path':'/',
'scheme':'https',
'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.9',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests':'1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
# 发起get请求
data = sess.get(url,headers=headers)

r,jschl_vc,passs,t = get_post_data(data)

print("r:  "+str(len(r)))

# 截取第一次请求返回的cookie值
first_cookie = data.headers["Set-Cookie"]
__cfduid = str(first_cookie).split(";")[0]
print(__cfduid)

# 截取第三次请求的请求网址
paths = find_word('<form id="challenge-form" action="(.*?)" method="POST" enctype="application/x-www-form-urlencoded">',data.text)
url2 = "https://www.biovision.com"+paths[0]
print(url2)

params = {
    'r':r,
    'jschl_vc':jschl_vc,
    'pass':passs,
    'jschl_answer':t
}

# 第二次请求网址(必定返回503)且(判定不能越过第二次请求网址请求第三个)
url = url+"favicon.ico"
# 第二次请求头
headers = {
'authority':'www.biovision.com',
'method':'GET',
'path':'/favicon.ico',
'scheme':'https',
'accept':'image/webp,image/apng,image/*,*/*;q=0.8',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.9',
'cookie': first_cookie,
'referer': 'https://www.biovision.com/',
'sec-fetch-mode': 'no-cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
data_2 = sess.get(url,headers=headers)
r2,jschl_vc2,passs2,t2 = get_post_data(data_2)
print("r2:  "+str(len(r2)))

# 第三次请求头
headers = {
'authority': k,
'method': 'POST',
'path': paths[0],
'scheme': 'https',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'max-age=0',
'content-length': '1880',
'content-type': 'application/x-www-form-urlencoded',
'cookie': __cfduid,
'origin': url[:-1],
'referer': url,
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'same-origin',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
# 第三次请求
data3 = requests.post(url2,data=params,headers=headers)

# 第一次一定是503，后面都是200
print(data3.status_code)
print(data3.headers)
# 返回运行时间(3s-7s不等)(可能与网速有关)
print(time.time()-times)

# 获取cookie进行cookie验证
info = data3.headers["Set-Cookie"]
cf_clearance = " cf_clearance="+find_word("cf_clearance=(.*?);",info)[0]+";"
__cfduid = "__cfduid="+find_word("__cfduid=(.*?);",info)[0]+";"
info = __cfduid+cf_clearance
print(info)

# url = "https://www.biovision.com/products/aging.html/"
# headers = {
# 'authority':'www.biovision.com',
# 'method':'GET',
# 'path':'/products/aging.html/',
# 'scheme':'https',
# 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'accept-encoding':'gzip, deflate, br',
# 'accept-language':'zh-CN,zh;q=0.9',
# # 'cookie':'__cfduid=df2b5c51db4974da85db216cbdb69308a1580175742; cf_clearance=aaceaf56080c2e33ba9ffccad672b85f3ff4f3e6-1581174791-0-150;',
# 'cookie':info,
# 'referer':url2,
# # 'referer':'https://www.biovision.com/?__cf_chl_jschl_tk__=3943776cf4c352e0ef5bcbcf9998e9bcacbf9206-1581174767-0-AcZPNv33LjWL7vjYAJs6Ar_l-HdTiAyufAvXAdv7CkL8W3fljSZ06298V7NTcODlPToC0bj9iZIuxcr9MM6hMHcC3LF2shiJr-ee4RRxaiF8llbBHTCHLt4TL6Km52grteOZf0q-XpIBNtGNm4BA8lMoFWKW0VNJgqqrEF5qhTXLKX6ZM8NwBVl1o0n3blE-D044WZ8sZaj-eyK-0xkfX6CprEpPdCshDE9K-A7Dsaetejy4vKsyRIBvoRssN-XH7ywWch4SePcw0hmcwdTRPSM',
# 'upgrade-insecure-requests':'1',
# 'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
# }
#
# import requests
# data = requests.get(url,headers=headers)
# print(data.status_code)




