# _*_ coding: utf-8 _*_
"""
__project__ = 'BiliBiliVideoToMusic'
__file_name__ = 'apiRenew'
__author__ = 'sudoskys'
__time__ = '2022/2/10 下午9:10'
__product_name__ = 'PyCharm'
__version__ = '2月102110'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""


class useTool(object):
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
        def wr(filens):
            import os
            file_dir = os.path.split(filens)[0]
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if not os.path.exists(filens):
                os.system(r'touch %s' % filens)
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
                # mLog("err", err).wq()
                logging.error(err)
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
                from ruamel.yaml import YAML
                data = YAML(typ='safe').load(f_obj)
                # print(data)
                return data
            except Exception as err:
                # mLog("err", err).wq()
                logging.error(err)
                return {}


class apiRenew(object):
    def __init__(self):
        self.END = False
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'https://api.bilibili.com/',
            'Connection': 'keep-alive',
            'Host': 'api.bilibili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Cookie': '1P_JAR=2022-02-09-02;SEARCH_SAMESITE=CgQIv5QB;ID=CgQIsv5QB0',
        }

    def clearTask(self, files):
        if not files:
            files = []
        import os
        file_list = os.listdir(
            os.path.abspath(os.path.dirname(useTool().filesafer("data/autoapi/queue/init.yaml"))))  # 获取当前文件夹内所有文件名
        for file in file_list[::-1]:  # 逆序遍历
            if file.endswith('.yaml'):  # 判断文件的扩展名
                pass
            else:
                file_list.remove(file)  # 过滤文件
        logging.debug(file_list)
        try:
            for i, k in enumerate(file_list):
                ok = useTool().filesafer('data/autoapi/queue/' + k)
                files.append(ok)
                os.remove(ok)
            os.remove(useTool().filesafer("data/autoapi/queue_rank.yaml"))
        except Exception as err:
            logging.error(err)
        else:
            pass

    def raiseTask(self, deal):
        import time
        date = str(time.strftime("%Y%m%d%H%M", time.localtime()))
        useTool().sData("data/autoapi/queue/" + date + ".yaml", deal)
        info = useTool().rData("data/autoapi/queue_rank.yaml")
        if not info:
            info = {}
        info[date] = useTool().filesafer("data/autoapi/queue/" + date + ".yaml")
        useTool().sData("data/autoapi/queue_rank.yaml", info)
        return date

    def cancelTask(self, keys, save=False):
        import os
        info = useTool().rData("data/autoapi/queue_rank.yaml")
        if info:
            path = info.get(keys)
            if os.path.exists(path):
                if not save:
                    os.remove(path)
                if info.pop(keys):
                    useTool().sData("data/autoapi/queue_rank.yaml", info)

    def doData(self, newer):
        import time
        import random

        def random_sleep(mu=4, sigma=1.7):
            """正态分布随机睡眠
            :param mu: 平均值
            :param sigma: 标准差，决定波动范围
            """
            secs = random.normalvariate(mu, sigma)
            if secs <= 0:
                secs = mu  # 太小则重置为平均值
            time.sleep(secs)

        random_sleep()
        # 强制休眠
        older = useTool().rData("data/autoapi/rank.yaml")
        if not older:
            older = {}
        if isinstance(newer, dict):
            # logging.debug(older)
            if len(list(older)) != 0:
                deal = {i: newer.get(i) for i in newer.keys() if i not in older.keys()}
                total = older.update(newer)
                # {**older, **newer}
            else:
                total = newer
                deal = newer
            useTool().sData("data/autoapi/rank.yaml", total)
            logging.debug(deal)
            # 注册任务
            key = self.raiseTask(deal)
            return key
        else:
            logger.info("NEED DICT")
            return False

    def apiInit(self, datas):
        import json
        import requests
        URLs = "http://api.bilibili.com/x/web-interface/search/type"
        # data = {"key":"value"}
        response = requests.get(url=URLs, params=datas, headers=self.header)
        if response.status_code == 200:
            content = response.text
            json_dict = json.loads(content)
            # logger.debug(json_dict)
            if json_dict['message'] == "0":
                if json_dict['data'].get("result"):
                    try:
                        res = json_dict['data'].get("result")
                        """
                        投币>20
                        &点赞>1000
                        &投币*2>收藏
                        &投币/点赞>0.3
                        or 
                        播放>2w
                        """
                        # logging.debug(res)
                        result = {}
                        for index, item in enumerate(res):
                            video_object = {}
                            title = item.get("title")
                            titles = title.replace('<em class="keyword">', '').replace('</em>', '')
                            char = '\:*?"<>|/'
                            for acao in char:
                                titles = titles.replace(acao, "_")
                            # logging.debug(titles)
                            video_object['title'] = titles
                            video_object['bvid'] = item.get("bvid")
                            video_object['review'] = item.get("review")
                            video_object['favorites'] = item.get("favorites")
                            video_object['play'] = item.get("play")
                            video_object['like'] = item.get("like")
                            video_object['tag'] = item.get("tag")
                            if video_object['title'].find("原创曲") != -1 or video_object['tag'].find("原创歌曲") != -1 or \
                                    video_object['tag'].find("原创曲") != -1 or video_object['play'] > 20000 or \
                                    video_object['favorites'] * 5 > video_object['like']:
                                result[video_object['bvid']] = video_object
                                # return result
                            else:
                                if video_object['favorites'] > 1000:
                                    result[video_object['bvid']] = video_object
                        logger.debug(result)
                        return result
                    except LookupError as err:
                        logger.error(err)
                        return False
                else:
                    logger.info("NO data" + str(json_dict))
                    self.END = True
                    return False
            else:
                logger.debug("NO Data Code" + str(json_dict))
                return False
        else:
            logger.debug("NET CODE  " + str(response.status_code))
            return False


import logging.config

logging.config.fileConfig("logger/pull.conf")
logger = logging.getLogger('justConsole')
