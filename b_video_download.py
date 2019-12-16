"""
2019-12-16 bilibili视频下载链接爬虫
"""

import requests
import re
import json
import time
import os

class BiliBili:
    def __init__(self,url):
        self.url = url
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        self.sess = requests.Session()
    def find_word(self,reg,text):
        reg = re.compile(reg,re.S)
        target = re.findall(reg,text)
        return target
    def time_name(self):
        times = str(time.ctime()).replace(" ", "_").replace(":", "_")
        return times
    def video_audio(self):
        headers = self.headers
        headers.update({'Referer':'{0}'.format(self.url)})
        data = self.sess.get(self.url,headers=headers).text
        b = json.loads(self.find_word(r'window.__playinfo__=(.*?)</script>',data)[0])
        # video
        video_url = [(i["id"], i['baseUrl'])for i in b['data']['dash']['video']]
        print(video_url[0][1])
        video_file = open("video_file.mp4","wb")
        data =[video_file.write(i)for i in self.sess.get(video_url[0][1],headers=headers,stream=True).iter_content(1024)if i]
        audio_url = [(i["id"],i['baseUrl'])for i in b['data']['dash']['audio']]
        print(audio_url[0][1])
        audio_file = open("audio_file.mp3","wb")
        data = [audio_file.write(i) for i in self.sess.get(audio_url[0][1], headers=headers, stream=True).iter_content(1024) if i]
        time.sleep(1)
        os.system('{0} -i video_file.mp4 -i audio_file.mp3 -vcodec copy -acodec copy {1}.mp4'.format(os.getcwd()+r"\ffmpeg.exe",self.time_name))
    def flv_video(self):
        headers = self.headers
        headers.update({'Cookie':"_uuid=FA6C7BFD-50D8-1956-93D2-6BA00805707417048infoc; LIVE_BUVID=AUTO4415439013167240; sid=9yyz3sl7; CURRENT_FNVAL=16; fts=1544535664; stardustvideo=1; buvid3=F17E09B6-3C4F-4274-8495-E6D54EA5932687960infoc; im_notify_type_298921868=0; rpdid=|(RllmR~~||0J'ullYum~kkk; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1561467751; UM_distinctid=16bc4f48cd42e7-069220d1cb5c53-3c604504-1fa400-16bc4f48cd53bc; DedeUserID=298921868; DedeUserID__ckMd5=805a300175018db9; SESSDATA=cd47419a%2C1566559536%2Cc9e91271; bili_jct=7236ce07b684ea062f6fa45b005db335; finger=edc6ecda; _uuid=4A413E6F-CF3A-B939-D24F-B4066148ED4230102infoc; CURRENT_QUALITY=64; bp_t_offset_298921868=286819028428856980"})
        data = self.sess.get(self.url,headers=headers).text
        a = json.loads(self.find_word(r'window.__playinfo__=(.*?)</script>',data)[0])
        data_url = [i["url"]for i in a["data"]['durl']][0]
        print(data_url)
        video_file = open("{0}.mp4".format(self.time_name()), "wb")
        data = [video_file.write(i) for i in self.sess.get(data_url, headers=headers, stream=True).iter_content(1024) if i]
        print('完成')
    def dongman(self):
        headers = self.headers
        headers.update({'Cookie': "_uuid=FA6C7BFD-50D8-1956-93D2-6BA00805707417048infoc; LIVE_BUVID=AUTO4415439013167240; sid=9yyz3sl7; CURRENT_FNVAL=16; fts=1544535664; stardustvideo=1; buvid3=F17E09B6-3C4F-4274-8495-E6D54EA5932687960infoc; im_notify_type_298921868=0; rpdid=|(RllmR~~||0J'ullYum~kkk; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1561467751; UM_distinctid=16bc4f48cd42e7-069220d1cb5c53-3c604504-1fa400-16bc4f48cd53bc; DedeUserID=298921868; DedeUserID__ckMd5=805a300175018db9; SESSDATA=cd47419a%2C1566559536%2Cc9e91271; bili_jct=7236ce07b684ea062f6fa45b005db335; finger=edc6ecda; _uuid=4A413E6F-CF3A-B939-D24F-B4066148ED4230102infoc; CURRENT_QUALITY=64; bp_t_offset_298921868=286819028428856980"})
        a = self.sess.get(self.url,headers=headers).text
        a = json.loads(self.find_word(r'window.__playinfo__=(.*?)</script>',a)[0])
        headers.update({'Referer': '{0}'.format(self.url)})
        # video
        video_url = [(i["id"], i['baseUrl'])for i in a['data']['dash']['video']]
        print(video_url[0][1])
        video_file = open("video_file.mp4", "wb")
        data = [video_file.write(i) for i in self.sess.get(video_url[0][1], headers=headers, stream=True).iter_content(1024) if i]
        # audio
        audio_url = [(i["id"], i['baseUrl'])for i in a['data']['dash']['audio']]
        print(audio_url[0][1])
        audio_file = open("audio_file.mp3", "wb")
        data = [audio_file.write(i) for i in self.sess.get(audio_url[0][1], headers=headers, stream=True).iter_content(1024) if i]
        time.sleep(1)
        os.system('{0} -i video_file.mp4 -i audio_file.mp3 -vcodec copy -acodec copy {1}.mp4'.format(os.getcwd() + r"\ffmpeg.exe", self.time_name))
    def zhibo(self):
        data = self.sess.get(self.url, headers=self.headers)
        a = json.loads(self.find_word(r'<script>window.__NEPTUNE_IS_MY_WAIFU__=(.*?)</script>', data.text)[0])
        url2 = [i['url'] for i in a['playUrlRes']['data']['durl']]
        data = self.sess.get(url2[0], headers=self.headers, stream=True)
        f = open("{0}.flv".format(self.time_name()), "wb")
        for i in data.iter_content(chunk_size=2048):
            print('\r {0}'.format(time.ctime()), end="")
            if i:
                f.write(i)
    def main(self):
        if 'av' in self.url:
            try:
                self.video_audio()
            except:
                self.flv_video()
        elif 'ss'or'ep' in self.url:
            try:
                self.dongman()
            except:
                print("error")
        else:
            try:
                self.zhibo()
            except:
                print("error")
if __name__ == '__main__':
    print(
    """
    =======================================================================================
    B站视频下载器
    下载器支持以下下载内容：
    普通视频：例子：https://www.bilibili.com/video/av47027321
    番剧：例子：https://www.bilibili.com/bangumi/play/ep267868/
    直播录屏(正在直播的也可以):例子：https://live.bilibili.com/10282650?visit_id=7ya4iegmc0g0
    ctrl+c可以随时关闭进程
    =======================================================================================
    """)
    c = input("请输入网址： ").strip()
    b = BiliBili(c)
    b.main()


