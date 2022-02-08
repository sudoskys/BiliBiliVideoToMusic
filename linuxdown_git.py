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
pip install setuptools wheel twine bs4 requests tabulate mutagen pydub you_get moviepy pyTelegramBotAPI feedparser ruamel.yaml O365
"""
'''
NOT ruamel IS ruamel.yaml！！
'''


# 工具类
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

    def filesafer(self, filen):
        def wr(filen):
            import os
            file_dir = os.path.split(filen)[0]
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if not os.path.exists(filen):
                os.system(r'touch %s' % filen)
            return filen

        try:
            road = wr(filen)
            # droad = os.getcwd() + road
            self.dprint("New+ " + road)
            return road
        except:
            import os
            print("重定向路径中" + str(os.getcwd() + '/' + filen))
            try:
                road = wr(os.getcwd() + '/' + filen)
                return road
            except IOError as err:
                print("err", err)
                print("Error:NOT FOUND FILE 没有找到文件或读取文件失败")
                return False

    def sData(self, file_name, tables):
        self.filesafer(file_name)
        if type(tables) == type({}) or type(tables) == type(["x"]):
            try:
                from ruamel.yaml import YAML
                yaml = YAML()
                with open(file_name, 'w') as f_obj:
                    yaml.dump(tables, f_obj)
            except IOError as err:
                mLog("err", err).wq()
                raise Exception("NOT FOUND FILE 没有找到文件或读取文件失败", err)
            else:
                return True
        else:
            print("Type Error:MUST TABLE", tables)
            return False

    def rData(self, file_names):
        file_name = os.getcwd() + '/' + file_names
        self.filesafer(file_name)

        with open(file_name) as f_obj:
            try:
                from ruamel.yaml import YAML
                data = YAML(typ='safe').load(f_obj)
                # print(data)
                return data
            except Exception as err:
                mLog("err", err).wq()
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
        import requests
        url = "https://tenapi.cn/bilivideo/?url=" + URLs
        response = requests.get(url)
        # print( response.status_code)
        if response.status_code == 200:
            content = response.text
            json_dict = json.loads(content)
            # print(json_dict)
            if json_dict['code'] == "200":
                if json_dict['url']:
                    try:
                        mUrl = json_dict['url']
                        mName = json_dict['title']
                    except LookupError as err:
                        mLog("err", err).wq()
                        return False
                    else:
                        mes = {'dN': mName, 'dU': mUrl, }
                        return mes
                else:
                    mLog("err", "NO url").wq()
            else:
                pass
                return False

    def succesdo(self, newdict):
        # 记录此次数据
        useTool().sData("data/rssdata.yaml", newdict)
    
    def cleandata(self, desstr, restr='|'):
        # 过滤除中英文及数字以外的其他字符
        res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
        return res.sub(restr, desstr)
    def well(self,name):
        import string
        # remove = string.punctuation
        table = str.maketrans(r'"~!#$'%^&,[]{}\/','________________',"")
        '''
        name = name.replace('/', '_')  # 消除目标对路径的干扰
        name = name.replace('"', '_')  # 消除目标对路径的干扰
        name = name.replace("'", '_')  # 消除目标对路径的干扰
        name = name.replace('/', '_')  # 消除目标对路径的干扰
        name = name.replace('"', '_')  # 消除目标对路径的干扰
        name = name.replace("'", '_')  # 消除目标对路径的干扰
        '''
        return name.translate(table)
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
            name_list.append(self.well(m.title))
            target_list.append(m.links[0].href)
        newdict = dict(zip(name_list, target_list))
        olddict = useTool().rData("data/rssdata.yaml")
        # 计算差值
        if not olddict:
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

    def youGet(self, name, road, url, murl):
        name = name.replace('/', '_')  # 消除目标对路径的干扰
        name = name.replace('"', '_')  # 消除目标对路径的干扰
        name = name.replace("'", '_')  # 消除目标对路径的干扰
        import random, time
        time.sleep(random.randint(7, 9))
        m = road + "" + name + ".flv"
        n = road + "" + name + ".mp4"
        mm = road + "" + name + '.wav'
        print('开始下载--' + m + '---->>>' + murl)

        def change(x):  # BV号转AV号，from 知乎www.zhihu.com/question/381784377/answer/1099438784---WTFPL
            tr = {}
            table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
            s = [11, 10, 3, 8, 4, 6]
            xor = 177451812
            add = 8728348608
            r = 0
            for i in range(58):
                tr[table[i]] = i
            for i in range(6):
                r += tr[x[s[i]]] * 58 ** i
            return (r - add) ^ xor

        def cmurl(url):  # 分类处理（番剧与普通视频）
            # 合并函数--//--//--//
            import re
            try:
                modle_video = r'BV\w{10}'
                match = re.findall(modle_video, url, re.I)
                new = match[0]
                new_url = 'https://www.bilibili.com/video/av' + str(change(new))
            except:
                modle_video = r'ss\d{5}'
                match = re.findall(modle_video, url, re.I)
                new = match[0]
                new_url = 'https://www.bilibili.com/bangumi/play/' + new
            return new_url

        import sys
        import you_get
        sys.argv = ['you-get', '-o', road, '-O', name, cmurl(murl)]  # '--playlist',
        you_get.main()
        from moviepy.editor import AudioFileClip
        if os.path.exists(m):
            my_audio_clip = AudioFileClip(m)
            my_audio_clip.write_audiofile(mm)
            print("//--------------//WAV OK//--------------//")
            return mm
        else:
            if os.path.exists(n):
                my_audio_clip = AudioFileClip(n)
                my_audio_clip.write_audiofile(mm)
                print("//--------------//WAV OK//--------------//")
                return mm
            else:
                print("//--------------//NO flv exists//--------------//")
                mLog("err", "Fail to download " + murl + '  -' + "-//NO flv exists//--------//").wq()
        # mLog("err", "Fail to download " + url + '  -' + name + ' - ' + str(r.status_code)).wq()

    def dealFile(self, name, road, url, murl):
        import random
        import time
        name = name.replace('/', '_')  # 消除目标对路径的干扰
        name = name.replace('"', '_')  # 消除目标对路径的干扰
        name = name.replace("'", '_')  # 消除目标对路径的干扰
        time.sleep(random.randint(7, 9))
        m = road + "" + name + ".flv"
        mm = road + "" + name + '.wav'
        print('开始下载--' + m + '---->>>' + url)
        # from fake_useragent import UserAgent
        # ua=UserAgent()
        fheader = {
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
            def change(x):  # BV号转AV号，from 知乎www.zhihu.com/question/381784377/answer/1099438784---WTFPL
                tr = {}
                table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
                s = [11, 10, 3, 8, 4, 6]
                xor = 177451812
                add = 8728348608
                r = 0
                for i in range(58):
                    tr[table[i]] = i
                for i in range(6):
                    r += tr[x[s[i]]] * 58 ** i
                return (r - add) ^ xor

            def cmurl(url):  # 分类处理（番剧与普通视频）
                # 合并函数--//--//--//
                import re
                try:
                    modle_video = r'BV\w{10}'
                    match = re.findall(modle_video, url, re.I)
                    new = match[0]
                    new_url = 'https://www.bilibili.com/video/av' + str(change(new))
                except:
                    modle_video = r'ss\d{5}'
                    match = re.findall(modle_video, url, re.I)
                    new = match[0]
                    new_url = 'https://www.bilibili.com/bangumi/play/' + new
                return new_url

            import sys
            import you_get
            sys.argv = ['you-get', '-o', road + "" + name, '-O', name, cmurl(murl)]  # '--playlist',
            you_get.main()
            # mLog("err", "Fail to download " + url + '  -' + name + ' - ' + str(r.status_code)).wq()
            # return False
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
            return mm
        else:
            print("//--------------//NO flv exists//--------------//")
            mLog("err", "Fail to download " + url + '  -' + "-//NO flv exists//--------//").wq()


# word on finding audio file url
# return a list of file

# 处理函数
def dealUrl(mtitle, murl, objects, _sync):
    import time
    import random
    from urllib.parse import quote
    def random_sleep(mu=5, sigma=0.7):
        """正态分布随机睡眠
        :param mu: 平均值
        :param sigma: 标准差，决定波动范围
        """
        secs = random.normalvariate(mu, sigma)
        if secs <= 0:
            secs = mu  # 太小则重置为平均值
        time.sleep(secs)

    # mes = dataPull().biliAudio(murl)
    random_sleep()
    mes = True
    if mes:
        # road = dataPull().dealFile(mes.get('dN'), useTool().filesafer("work/music/"), mes.get('dU'), murl)
        road = dataPull().youGet(mtitle, useTool().filesafer("work/music/"), murl, murl)
        if road:
            flacPath = useTool().pydubTrans(road, "flac")
            syncurl = 'https://onedrive-vercel-index-navy-three.vercel.app/Music/' +
                               quote((os.path.basename(flacPath)), 'utf-8')
            shut = objects.postAudio(flacPath, mtitle + '\n' + murl + "\n#音乐提取 #自动化  #R3 " +
                                     '\nSync '+ '<a href="' + syncurl + '">Sync link</a>'  , mtitle)
            # _token_ = onedrive(sys.argv[4]).upload(flacPath, sys.argv[5], sys.argv[6])
            _token_ = _sync.upload(flacPath)
            os.remove(shut)
            # os.remove(_token_)
        else:
            pass
    else:
        # road = dataPull().youGet(mes.get('dN'), useTool().filesafer("work/music/"), mes.get('dU'), murl)
        road = dataPull().youGet(mtitle, useTool().filesafer("work/music/"), murl, murl)
        if road:
            flacPath = useTool().pydubTrans(road, "flac")
            shut = objects.postAudio(flacPath, mtitle + murl + " #音乐提取 #自动化 R1", mtitle)
            os.remove(shut)
        else:
            mLog("err", "Fail to get info " + murl + '  -' + mtitle).wq()
            pass


class onedrive:
    # robotPush(token,groupID).postAudio(fileroad,info,name):
    def __init__(self, token, zuhuid, keyid):
        import base64
        self.token = base64.b64decode(token).decode('utf-8')
        self.zuhuid = zuhuid
        self.keyid = keyid
        import json
        with open(useTool().filesafer("o365_token.txt"), 'w+') as f:
            #f.write(json.dumps(self.token))
            f.write(self.token)

    def upload(self, _path):
        from O365 import Account
        credentials = (self.zuhuid, self.keyid)
        account = Account(credentials=credentials)  # credentials=credentials)
        storage = account.storage()
        my_drive = storage.get_default_drive()
        pro = my_drive.get_item_by_path('/share/Music')
        pro.upload_file(item=_path)
        return useTool().filesafer("o365_token.txt")


# 机器人实例
class robotPush:
    # robotPush(token,groupID).postAudio(fileroad,info,name):
    def __init__(self, token, ID):
        import telebot
        self.BOT = telebot.TeleBot(token, parse_mode="HTML")  # You can set parse_mode by default. HTML or MARKDOWN
        self.objectID = ID

    def sendMessage(self, msg):
        self.BOT.send_message(self.objectID, str(msg))

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
    apptoken = lmain.get('apptoken')
    appid = lmain.get('appid')
    appkey = lmain.get('appkey')
    if not all([token, objectID, rssurl, apptoken, appid, appkey]):
        mLog("err", "  参数不全  ").wq()
        raise Exception("参数不全!", lmain)
    else:
        # 构建机器人实例
        push = robotPush(token, objectID)
        sync = onedrive(apptoken, appid, appkey)
        time.sleep(2)
        srssdata, orginData = dataPull().rssdata(rssurl)
        if not srssdata:
            print("NO New Data")
            mLog("log", "  NO New Data  ").wq()
            useTool().remove(useTool().filesafer("work/music/"))
            # shutil.rmtree(useTool().filesafer("work/music/"), ignore_errors=False, onerror=None)
            shutil.rmtree(os.getcwd() + '/work/', ignore_errors=False, onerror=None)  # 删除
            os.remove(useTool().filesafer("o365_token.txt"))
        else:
            print(srssdata)
            if isinstance(srssdata, dict):
                for n, u in srssdata.items():
                    print("START===" + n)
                    try:
                        dealUrl(n, u, push, sync)
                    except BaseException as arg:
                        push.sendMessage('Failed post ' + n + '\n Url:' + u + '\n Exception:' + str(arg))
                        # mLog("err", "Fail " + n + '  -' + u).wq()
            else:
                for n, u in srssdata:
                    print("START===" + n)
                    try:
                        dealUrl(n, u, push, sync)
                    except BaseException as arg:
                        push.sendMessage('Failed post ' + n + '\n Url:' + u + '\n Exception:' + str(arg))
                        # mLog("err", "Fail " + n + '  -' + u).wq()
            # dataPull().succesdo(orginData)
            mLog("log", "  Renew Data  ").wq()
            print("========OK=========")
            useTool().remove(useTool().filesafer("work/music/"))
            shutil.rmtree(os.getcwd() + '/work/', ignore_errors=False, onerror=None)  # 删除存储的视频文件
            os.remove(useTool().filesafer("o365_token.txt"))





# channal id ,please use @getidsbot get this value!
import os
import shutil
import sys
import time

lme = {'token': sys.argv[1],
       'objectID': sys.argv[2],
       "rssurl": sys.argv[3],
       "apptoken": sys.argv[4],
       "appid": sys.argv[5],
       "appkey": sys.argv[6],
       }

mian(**lme)

'''
import base64
print(base64.b64decode("YWJjcjM0cjM0NHI=").decode('utf-8'))
'''
