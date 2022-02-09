# _*_ coding: utf-8 _*_
"""
__project__ = 'BiliBiliVideoToMusic'
__file_name__ = 'flacTool'
__author__ = 'sudoskys'
__time__ = '2022/2/9 下午11:27'
__product_name__ = 'PyCharm'
__version__ = '2月092327'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""

class flacInfo:
    def __init__(self,urls):
        self.netpic = False
        self.header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control':'max-age=0',
            'DNT': '1',
            'Referer': 'https://api.bilibili.com/',
            'Connection': 'keep-alive',
            'Host': 'api.bilibili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Cookie':'1P_JAR=2022-02-09-02;SEARCH_SAMESITE=CgQIv5QB',
        }
        self.getInfo(urls)

    def pict_test(self, audios):
             from mutagen.flac import File
             from mutagen.flac import Picture, FLAC
             try:
                 x = audios.pictures
                 if x:
                     return True
             except Exception:
                 pass
             if 'covr' in audios or 'APIC:' in audios:
                 return True
             return False

    def get_image(self,urls):
        import requests,re
        myfile = requests.get(urls)
        suf = re.search(u'(?P<suf>.\w*$)',urls).groupdict().get("suf")
        name = self.Name + suf
        open(name, 'wb').write(myfile.content)
        if myfile.status_code == 200:
           return name
        else:
           return False

    def set_image(self, filename, albumartx):
          # from mutagen.flac import File
          from mutagen.flac import Picture, FLAC
          import os
          audio = FLAC(filename)
          image = Picture()
          image.type = 3
          path = self.get_image(albumartx)
          if path:
             albumart = path
             self.netpic = True
          else:
             print(99)
             albumart = useTool().filesafer("data/defalut_cover.png")
             self.netpic = False

          # if  os.path.splitext(albumart)[-1][1:]==('png'):
          if  ".png" in albumart:
              mime = 'image/png'
          else:
              mime = 'image/jpeg'
          image.desc = 'front cover'
          with open(albumart, 'rb') as f: # better than open(albumart, 'rb').read() ?
              image.data = f.read()
          audio.add_picture(image)
          audio.save()
          if self.netpic:
            os.remove(useTool().filesafer(albumart))


    def setFlac(self,file_dir):
        """use.mutagen; intro.flac,labled;
        file_dir : file path
        info : a dict contain info
        info = {
                'TITLE': name,
                'ARTIST': u'邓紫棋',
                'ALBUMARIST': u'邓紫棋',
                'ALBUM': u'新的心跳',
                'DATE': '2015',
                'GENRE': 'Pop',
                'TRACKNUMBER': number
            }
        """
        from mutagen.flac import FLAC
        audio = FLAC(file_dir)
        try:
            encoding = audio["ENCODING"]
        except:
            encoding = ""
            audio.delete()
        # add FLAC tag data
        audio["TITLE"] = self.Name
        audio["ARTIST"] = self.userName
        audio["ALBUM"] = self.Name
        audio["COMPOSER"] = self.userTname
        audio["ORGANIZATION"] = "ASOUL二创"
        # audio["CATALOGNUM"] = self.catno
        audio["GENRE"] = self.userTname
        audio["YEAR"] = self.creatYear
        audio["DESCRIPTION"] = '::> Don\'t believe the hype! <::'
        if(len(encoding) != 0):
            audio["ENCODING"] = encoding
        audio.pprint()
        try:
            audio.save()
        except BaseException:
            return False
        try:
            self.set_image(file_dir,self.audioPic)
        except BaseException as e:
            print(e)
            return False

    def getInfo(self, murl):
        import json
        import re
        # macth...
        bvid = re.search(u'(?P<bvid>BV\w*)',murl).groupdict().get("bvid")
        import requests
        turl = "http://api.bilibili.com/x/web-interface/view?bvid=" + bvid
        response = requests.get(turl, headers=self.header, allow_redirects=True)
        if response.status_code == 200:
            content = response.text
            json_dict = json.loads(content)
            # print(json_dict)
            if json_dict['code'] == 0:
                try:
                    json_map = json_dict['data']
                    # 这个人图省事没有做数据直接转化，而是一条条赋值(
                    self.audioPic = json_map['owner'].get("face") #作者
                    self.Name = json_map.get('title') #标题
                    self.userName = json_map['owner'].get("name") #作者
                    self.userTname = json_map.get('tname') #风格
                    import time
                    timeStamp = json_map.get('ctime')
                    timeArray = time.localtime(timeStamp)
                    self.creatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    self.creatYear = time.strftime("%Y", timeArray)
                except LookupError as err:
                    # mLog("err", err).wq()
                    return False
                else:
                    pass
                    return True
            else:
                msg = json_dict['code']
                return False
        else:
            msg = str(response.status_code) + " -" + turl
            return False

