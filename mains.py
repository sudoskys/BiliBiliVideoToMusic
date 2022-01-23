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


# 数据提取的处理


## 函数区
import os


def _filesafer(filename):
    import os
    file_dir = os.path.split(filename)[0]
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    if not os.path.exists(filename):
        os.system(r'touch %s' % filename)
    return filename


# TARGET url get
def _data():
    urls = (input('PUT THE LINK:'))
    return urls


def succesdo(name_list, target_list):
    # 记录此次数据
    with open(os.getcwd() + '/history_name.txt', 'w') as f:
        for i in name_list:
            f.write(i + "\n")

    with open(os.getcwd() + '/history_target.txt', 'w') as f:
        for i in target_list:
            f.write(i + "\n")


# succesdo(name_list,target_list)

# print(_rssdata(rssurl))

# succesdo(name_list,target_list) #执行成功后将数据记录便于下一次去重
# print(_rssdata(rssurl))


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


def _flvtowav(r, c):
    # pip install moviepy
    # from moviepy.editor import AudioFileClip
    from moviepy.editor import AudioFileClip
    if os.path.exists(r):
        my_audio_clip = AudioFileClip(r)
        my_audio_clip.write_audiofile(c)
        print("//--------------//WAV OK//--------------//")
        if not savetimev:
            os.remove(r)
    else:
        print("//--------------//NO flv exists//--------------//")


def _wavtoflac(r, c):
    # from pydub import AudioSegment
    from pydub import AudioSegment
    if os.path.exists(r):
        song = AudioSegment.from_wav(r)
        song.export(c, format="flac")
        if not savewav:
            os.remove(r)
        print("//--------------//FLAC OK//--------------//")
        # _postfile(rflacroad,sources,rname) # 返回值：通知
    else:
        print("//--------------//NO wav exists~//--------------//")


def _flacsign(fileroad, c):
    from mutagen.flac import FLAC
    file = fileroad
    if file.split('.')[-1] == 'flac':
        file_name = re.findall(r'[^\/]+(?=\.)', file)[0]
        # file_name = file.split('/')[-1].split('.')[0]
        name = file_name[3:]
        number = file_name[:2]
        names = input('作曲家名字name：')
        datas = input('日期data：')
        ALBUMARISTs = input('专辑ALBUMARIST：')
        genre = input('风格genre：')
        info = {
            'TITLE': name,
            'ARTIST': names,
            'ALBUMARIST': names,
            'ALBUM': ALBUMARISTs,
            'DATE': datas,
            'GENRE': genre,
            'TRACKNUMBER': number}
        print(info)
        # flac_process(file, info)



def mians(road, sources, title):
    PATH: object = road
    # test
    # PATH = r"C:/Users/LUO/Videos/S_T_A_Y___勺.勺宝_STAY_版本一_中文歌词.398855461.flv"
    AVnum = ntpath.basename(PATH)
    folder = os.getcwd() + '/work/' + AVnum
    newflv = folder + '/' + AVnum
    newwav = folder + '/' + AVnum + '.wav'
    # newflac = folder + '/' + AVnum + '.flac' # 以视频号命名
    newflac = folder + '/' + title + '_' + AVnum + '.flac'  # 采用视频加名称并删除work缓存机制
    # new folder
    if os.path.exists(PATH):
        if not os.path.exists(folder):
            os.makedirs(folder)
            print("//-----------//Automatically create new folders//--------------//")
        shutil.copyfile(PATH, newflv)
        print("//--------------//COPY OK//--------------//")
        _flvtowav(newflv, newwav)
        _wavtoflac(newwav, newflac)
    # _postfile(newflac,sources,title) # 返回值：通知
    else:
        print("//--------------//No file exists//--------------//")
        pass
    return sources, newflac, title, newflv


def _download(mtitle, murl):
    mtitle = mtitle.replace('/', '_')  # 消除目标对路径的干扰
    import sys, you_get
    import getpass
    user = getpass.getuser()
    TAIL = ntpath.basename(murl)
    timestamp = str(int(time.time()))
    directory = os.getcwd() + '/work/' + timestamp + "_" + str(TAIL) + '/'  # 设置下载目录
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("//--//NEW DOWN FOLDER//--//" + directory)
    # USE YOUGET
    sys.argv = ['you-get', '--playlist', '-o', directory, '-O', TAIL, murl]
    you_get.main()
    # CHECK ROOT DIR
    for root, dirs, files in os.walk(directory):
        for name in files:
            filepath = root + "" + name
            if not filepath.split('.')[-1] == "xml":
                sources, rflacroad, rname, videoroad = mians(filepath, murl, mtitle)
                print('//--Finish--//--' + murl + '--//--' + rflacroad)
    if not savestorev:
        shutil.rmtree(directory, ignore_errors=False, onerror=None)  # 删除存储的视频文件


# try:
# except:
#   print("Error: unable to start dav")


# 主程序
def _main():
    nowtimes = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logr = _filesafer(os.getcwd() + '/log.txt')
    time.sleep(2)
    datadict = _data()
    if not datadict:
        print("NOnewdata")
        with open(logr, 'a+') as f:
            f.write(nowtimes + "  NO NEW DATA" + "\n")
        pass
    else:
        print(datadict)
        if type(datadict) == type("string"):
            print("STARTing//--//" + ntpath.basename(datadict))
            _download(ntpath.basename(datadict), cmurl(datadict))  # 返回值：road-file

        print("OK---*-*-*-*-*-*-*-*")
        with open(logr, 'a+') as f:
            f.write(nowtimes + "  DONE" + "\n")
        if not savework:
            shutil.rmtree(os.getcwd() + '/work/', ignore_errors=False, onerror=None)  # 删除存储的视频文件
        # 推送至TG，但是不需要hold
        # BOT.polling()


import os, re
import shutil
import ntpath, time, sys

## 输入数据
# BASEDATA
target_list = []
name_list = []

savestorev = False  # 下载数据 不保留
savewav = True  # wav 不保留
savework = True   # 不保留work文件夹
savetimev = True  # flv 不保留
POSTMV = False

# 解决空冲突
if POSTMV and not savetimev:
    savetimev = True
_main()
