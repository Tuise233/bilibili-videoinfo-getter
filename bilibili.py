#Bilibili信息获取
from bs4 import BeautifulSoup
from bv2av import BvConvert
import requests
import json

class Bilibili:

    #获取视频bv号
    def get_bv(self,url):
        return url[31:43]

    #获取视频av号
    def get_av(self,bv):
        bvc = BvConvert()
        return bvc.bv2av(bv)

    #获取视频文件信息
    def get_video_info(self,bv):
        html = requests.get('https://api.bilibili.com/x/player/pagelist?bvid='+bv+'&jsonp=jsonp')
        hhtml = requests.get('https://www.jijidown.com/api/v1/video/get_download_info?id='+str(self.get_av(bv)))
        ddata = json.loads(hhtml.text)
        data = json.loads(html.text)
        jdata = {
            "video_name":ddata['res'][0]['part'],
            "video_length":data['data'][0]['duration'],
            "video_dimension":data['data'][0]['dimension']
        }
        return jdata
    
    #获取视频类型
    def get_video_tag(self,bv):
        html = requests.get("https://api.bilibili.com/x/web-interface/view/detail/tag?aid="+str(self.get_av(bv)))
        data = json.loads(html.text)
        tags=""
        for i in range(len(data['data'])):
            tags+=data['data'][i]['tag_name']
            if i != 9:
                tags+=","
        return tags
    
    def get_video_img(self,bv):
        html = requests.get('https://www.jijidown.com/api/v1/video/get_info?id='+str(self.get_av(bv))+'&refresh=undefined')
        data = json.loads(html.text)
        return data['img']

    def get_video_date(self,bv):
        html = requests.get('https://www.jijidown.com/api/v1/video/get_info?id='+str(self.get_av(bv))+'&refresh=undefined')
        data = json.loads(html.text)
        return data['btime']

    #获取视频观看信息
    def get_video_state(self,bv):
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        }
        html = requests.get('https://api.bilibili.com/x/web-interface/archive/stat?aid='+str(self.get_av(bv)),headers=header)
        hhtml = requests.get('https://search.bilibili.com/all?keyword='+bv)
        soup = BeautifulSoup(hhtml.text,'lxml')
        ul = soup.find_all('ul',class_='video-list clearfix')[0]
        data = json.loads(html.text)
        response = requests.get(self.get_video_img(bv))
        jdata = {
            "av":self.get_av(bv),
            "bv":bv,
            "view":data['data']['view'],
            "bullet":data['data']['danmaku'],
            "like":data['data']['like'],
            "coin":data['data']['coin'],
            "favorite":data['data']['favorite'],
            "share":data['data']['share'],
            "reply":data['data']['reply'],
            "description":ul.find_all('div')[5].get_text().replace(" ","").replace("\n",""),
            "author":ul.find_all('div')[6].find_all('span')[3].get_text().replace(" ","").replace("\n",""),
            "tag":self.get_video_tag(bv),
            "img":response.content,
            "date":self.get_video_date(bv)
        }
        return jdata

    def get_video_all(self,bv):
        jdata = {
            "video_info":self.get_video_info(bv),
            "video_state":self.get_video_state(bv),
        }
        return jdata
