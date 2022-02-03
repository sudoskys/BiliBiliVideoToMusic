# _*_ coding: utf-8 _*_
"""
__project__ = 'BiliBiliVideoToMusic'
__file_name__ = 'git'
__author__ = 'sudoskys'
__time__ = '2022/2/3 下午10:05'
__product_name__ = 'PyCharm'
__version__ = '2月032205'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""
# _*_ coding: utf-8 _*_
"""
__project__ = 'bili'
__file_name__ = 'main'
__author__ = 'sudoskys'
__time__ = '1/20/22 7:27 PM'
__product_name__ = 'PyCharm'
__version__ = 'Jan201927'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""
'''
info:please check chains between each step
class:
   - caculate_rss  deal the rss
   - url_car  download the file from url
   - video_cat  
   - file_tool
'''

# 数据提取的处理
"""
python -m pip install --upgrade pip
pip install setuptools wheel twine bs4 requests tabulate mutagen pydub you_get moviepy pyTelegramBotAPI feedparser ruamel
"""


## 工具类
class useTool:
    # github：sudoskys
    def __init__(self):
        self.debug = True
        import os
        self.home = os.getcwd()

    def dprint(self, log):
        if self.debug:
            print(log)

    def remove(self, top):
        import os
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def filesafer(self, filename):
        def wr(filename):
            import os
            file_dir = os.path.split(filename)[0]
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if not os.path.exists(filename):
                os.system(r'touch %s' % filename)
            return filename

        try:
            road = wr(filename)
            # droad = os.getcwd() + road
            self.dprint("New+ " + road)
            return road
        except:
            import os
            print("重定向路径中" + str(os.getcwd() + '/' + filename))
            try:
                road = wr(os.getcwd() + '/' + filename)
                return road
            except IOError as err:
                print("err", err)
                print("Error:NOT FOUND FILE 没有找到文件或读取文件失败")
                return False

    def sData(self, file_name, tables):
        self.filesafer(file_name)
        if type(tables) == type({}) or type(tables) == type(["x"]):
            try:
                import ruamel_yaml as YAML
                # from ruamel.yaml import YAML
                yaml = YAML()
                with open(file_name, 'w') as f_obj:
                    yaml.dump(tables, f_obj)
            except IOError as err:
                print("err", err)
                raise Exception("NOT FOUND FILE 没有找到文件或读取文件失败", err)
            else:
                return True
        else:
            print("Type Error:MUST TABLE", tables)
            return False

    def rData(self, file_names):
        import os
        file_name = os.getcwd() + '/' + file_names
        self.filesafer(file_name)
        with open(file_name) as f_obj:
            try:
                import ruamel_yaml as YAML
                data = YAML(typ='safe').load(f_obj)
                # print(data)
                return data
            except Exception as err:
                print("err", err)
                return {}

    def pydubTrans(self, paths, Format):
        from pydub import AudioSegment
        self.dprint(paths + str(os.path.splitext(paths)[-1][1:]))
        song = AudioSegment.from_file(os.getcwd() + '/' + paths, os.path.splitext(paths)[-1][1:])
        target = paths + "." + str(Format)
        if song.export(target, format=str(Format)):
            os.remove(paths)
        return target


# LOG类
class mLog:
    # mLog("log","succes!").wq()
    def __init__(self, roadName, logs):
        if not all([roadName, logs]):  # 当 arg1, arg2, arg3都不为空时all函数返回true
            self.OK = False
            # return jsonify(errno=RET.PARAMERR, errmsg=u"oh ,log function 参数不完整！")
            pass
        else:
            self.OK = True
            self.nowtimes = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.logr = str(useTool().filesafer(os.getcwd() + '/' + roadName + '.txt'))
            self.logC = logs
            # use usetool ,please

    def wq(self):
        if self.OK:
            with open(self.logr, 'a+') as f:
                f.write(str(self.nowtimes) + ' -' + str(self.logC) + "\n")
                useTool().dprint(str(self.nowtimes) + ' -' + str(self.logC))


# 数据类
class dataPull:
    def __init__(self):
        self.header = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'DNT': '1',
            'Referer': 'https://api.bilibili.com/',
            'Connection': 'keep-alive',
            'Host': 'api.bilibili.com',
            'Upgrade - Insecure - Requests': '1',
            'User-Agent': "us",
        }
        # 初始化类
        pass
        # TARGET url get

    def biliAudio(self, URLs):
        import json
        # import re
        import requests
        url = "https://tenapi.cn/bilivideo/?url=" + URLs
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            content = response.text
            json_dict = json.loads(content)
            # print(json_dict)
            if json_dict['code'] == 200:
                if json_dict['url']:
                    try:
                        mUrl = json_dict['url']
                        mName = json_dict.get('title')
                    except LookupError as err:
                        mLog("err", err).wq()
                        return False
                    else:
                        mes = {'dN': mName, 'dU': mUrl, }
                        return mes
            else:
                pass
                return False

    def succesdo(self, newdict):
        # 记录此次数据
        useTool().sData("data/rssdata.yaml", newdict)

    def rssdata(self, url):
        # succesdo(["begin"],["begin"])
        # RSS解析器
        import feedparser
        # 取新
        fp = feedparser.parse(url)
        name_list = []
        target_list = []
        for m in fp.entries:
            # print('T:',m.title)
            # print('U:',m.links[0].href)
            name_list.append(m.title)
            target_list.append(m.links[0].href)
        newdict = dict(zip(name_list, target_list))
        olddict = useTool().rData("data/rssdata.yaml")
        # 计算差值
        if len(olddict) == 0:
            childdict = newdict
        else:
            if not olddict == newdict:
                childdict = newdict.items() - olddict.items()
                if len(childdict) == 0:
                    childdict = False
            else:
                childdict = False
        # 存储dict
        # print(childdict)

        # 存入
        self.succesdo(newdict)
        return childdict, newdict

    def dealFile(self, name, road, url):
        import random, time
        time.sleep(random.randint(7, 9))
        m = road + "" + name + ".flv"
        mm = road + "" + name + ".flac"
        print(m + '---->>>' + url)
        print(useTool().dURL(url))
        # from fake_useragent import UserAgent
        # ua=UserAgent()
        fheader = {
            'Host': useTool().dURL(url),
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',  # ua.chrome,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers',
        }
        import requests
        r = requests.get(url, headers=fheader, stream=True, allow_redirects=True)
        if r.status_code == 403:
            mLog("err", "Fail to download " + url + '  -' + name + ' - ' + str(r.status_code)).wq()
            return False
        else:
            print("Begin Down ----")
            with open(m, "wb") as music:
                for chunk in r.iter_content(chunk_size=1024):  # 1024 bytes
                    if chunk:
                        music.write(chunk)

                from moviepy.editor import AudioFileClip
                if os.path.exists(m):
                    my_audio_clip = AudioFileClip(m)
                    my_audio_clip.write_audiofile(mm)
                    print("//--------------//WAV OK//--------------//")
                else:
                    print("//--------------//NO flv exists//--------------//")
                    mLog("err", "Fail to download " + url + '  -' + "-//NO flv exists//--------//").wq()
                return m


# word on finding audio file url
# return a list of file

def dealUrl(mtitle, murl, objects):
    mes = dataPull().biliAudio(murl)
    if mes:
        road = dataPull().dealFile(mes.get('dN'), useTool().filesafer("work/music/"), mes.get('dU'))
        if road:
            flacPath = useTool().pydubTrans(road, "flac")
            shut = objects.postAudio(flacPath, mtitle + murl + " #音乐提取 #自动化2.0 ", mtitle)
            os.remove(shut)
        else:
            pass
    else:
        mLog("err", "Fail to get info " + murl + '  -' + mtitle).wq()
        pass


class robotPush:
    # robotPush(token,groupID).postAudio(fileroad,info,name):
    def __init__(self, token, ID):
        import telebot
        self.BOT = telebot.TeleBot(token)  # You can set parse_mode by default. HTML or MARKDOWN
        self.objectID = ID

    def postVideo(self, file, source, name):
        import os
        if os.path.exists(file):
            video = open(file, 'rb')
            self.BOT.send_video(self.objectID, video, source, name, name)
            # '#音乐MV #AUTOrunning '+str(source)+"   "+name
            # 显示要求为MP4--https://mlog.club/article/5018822
            print("============Already upload this video============")
            video.close()
            return file

    def postAudio(self, file, source, name):

        if os.path.exists(file):
            audio = open(file, 'rb')
            self.BOT.send_audio(self.objectID, audio, source, name, name)
            # '#音乐提取 #AUTOrunning '+str(source)+"   "+name
            print("============ALready upload this flac============")
            audio.close()
            return file


def mian(**lmain):
    token = lmain.get('token')
    objectID = lmain.get('objectID')
    rssurl = lmain.get('rssurl')
    if not all([token, objectID, rssurl]):
        mLog("err", "  参数不全  ").wq()
        raise Exception("参数不全!", lmain)
    else:
        push = robotPush(token, objectID)
        time.sleep(2)
        srssdata, orginData = dataPull().rssdata(rssurl)
        if not srssdata:
            print("NO New Data")
            mLog("log", "  NO New Data  ").wq()
            useTool().remove(useTool().filesafer("work/music/"))
            # shutil.rmtree(useTool().filesafer("work/music/"), ignore_errors=False, onerror=None)
            shutil.rmtree(os.getcwd() + '/work/', ignore_errors=False, onerror=None)  # 删除存储的视频文件
        else:
            print(srssdata)
            if type(srssdata) == type({"key": "114"}):
                for n, u in srssdata.items():
                    print("START===" + n)
                    dealUrl(n, u, push)
            else:
                for n, u in srssdata:
                    print("START===" + n)
                    dealUrl(n, u, push)
            # dataPull().succesdo(orginData)
            mLog("log", "  Renew Data  ").wq()
            print("========OK=========")
            useTool().remove(useTool().filesafer("work/music/"))
            shutil.rmtree(os.getcwd() + '/work/', ignore_errors=False, onerror=None)  # 删除存储的视频文件


# channal id ,please use @getidsbot get this value!
import sys, os, shutil, time

lme = {'token': sys.argv[1],
       'objectID': sys.argv[2],
       "rssurl": sys.argv[3]}
mian(**lme)
