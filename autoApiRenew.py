# _*_ coding: utf-8 _*_
"""
__project__ = 'BiliBiliVideoToMusic'
__file_name__ = 'autoApi'
__author__ = 'sudoskys'
__time__ = '2022/2/10 下午8:58'
__product_name__ = 'PyCharm'
__version__ = '2月102058'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""


# 工具类
# !python -m pip install --upgrade pip
# !pip install requests tabulate mutagen feedparser ruamel.yaml

from mods.apiRenew import apiRenew, logging
data = {"search_type": "video",
        "keyword": "ASOUL 原创曲",
        "order": "pubdate",
        "duration": "1",
        "tids_1": "3",
        "tids_2": "28",
        "page": "1",
        }

RES = apiRenew().apiInit(data)
if RES:
    key = apiRenew().doData(RES)
    if key:
        logging.info(key)
        #apiRenew().cancelTask(key)


'''
#apiRenew().clearTask()
'''

'''
info = useTool().rData("data/autoapi/queue_rank.yaml")
for i,k in enumerate(info):
    print(info)
    for i in useTool().rData(info.get(k)):
        print(i)

'''
