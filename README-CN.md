## BiliBiliVideoToMusic
![counter](https://count.getloli.com/get/@sudoskys-github-BiliBiliVideoToMusic?theme=moebooru)

[![MIT License](https://img.shields.io/badge/LICENSE-MIT-ff69b4)](http://choosealicense.com/licenses/mit/)   ![u](https://img.shields.io/badge/USE-python-green)   [![s](https://img.shields.io/badge/Sponsor-Alipay-ff69b4)](https://azz.net/ly233)
![v](https://img.shields.io/badge/Version-220209-9cf)  

### [English](README.md)  | [中文](README-CN.md) 

## 介绍

哔哩哔哩视频下载提取音频为wav与flac   TG-RSS版本视频二传提取推送。
此项目可以让你同步收藏夹二创视频的音乐到指定TG群组并且还有onedrive bussines，使用RSShub提供数据支持。



## 特性
🛠 MAIN可以在windows系统上运行，支持贴音乐标签与可选保存flv和wav文件。（自己改动文件.....）

🚧 如果您使用action部署，功能仅有提取flac。配置这个action，需要在环境内加密钥，一个是token，一个是email。（自己申请github openapi token https://github.com/settings/tokens/new）

🎤 音质应该和视频听到的是一样的

## 注意
⚠ 每次最多执行20个推送任务.

⚠ 请勿推送超长视频(>10min)，避免风险

⚠ 请不要直接部署在Github Action服务上，本仓库的yml用作任务流可用性测试  https://www.blueskyxn.com/202107/4731.html

⚠ Liunx部署RSS推送  see music.yml，变量需要手动配置.

## 开始
### 1. 安装要求

 **Python 3.7 或更高版本** 
```
python -m pip install --upgrade pip

pip install setuptools wheel twine bs4 requests tabulate mutagen pydub you_get moviepy pyTelegramBotAPI feedparser
```
- FFmpeg环境 [ffmpeg](https://ffmpeg.org/download.html#get-packages)。
（本仓库Action使用 https://github.com/marketplace/actions/setup-ffmpeg ）
* 本地使用运行`pip install bs4 requests tabulate mutagen pydub you_get moviepy` 来安装必要包
* 推送服务安装机器人API库和RSS解析库 `pip install pyTelegramBotAPI feedparser`

### 2. 准备

#### 选择文件版本
```
linuxdown_git.py --->RSS auto editon
mains.py --->win&linux editon
```
⚠ 自220209版本后加入了ONEdrive同步功能，如果Rss部署不需要此功能，请注释lmain的参数与其中有关onedrive的类.


#### RSS推送用户
* 源(gitPush.py)
需要自建 [Rsshub](https://docs.rsshub.app/) 来获得网络源，或者使用公开项目的服务！详见  .

* Fork 本仓库并设置secrets
Tips: 如果您使用action部署，建议只设置提取flac。
配置此action，需要在环境内加secrets，一个是githubtoken，一个是email。（自己申请[github openapi token](https://github.com/settings/tokens/new)

**Add Repository secrets**
```
>token
>objectID
>rssurl
>apptoken
>appid
>appkey
```
```
token = ***** # bot token，use tg@BotFather，自行google
objectID = ***** # channal id ,please use tg@getidsbot get this value!
rssurl = ****  # rssurl，详见 https://docs.rsshub.app/

----
appid，appkey，apptoken 是 微软云盘同步使用，这些量需要您去azure获取，而token请通过运行test/tokensetup自动生成！
不需要此功能请注释掉！
```

**Add Environment secrets**
```
>token # github token，use https://github.com/settings/tokens/new
>email # your email address
```

⚠ 注意区分两个token.

* 运行
Github action每天6:20运行一次流程，仓库主人加星也会触发流程.

#### 独立使用
USE mains.py  

填写 data/userdata.yaml，运行即可.


## 实现逻辑(gitPush.py)

>具体代码详见 gitPush.py （windows环境下使用main.py）
拉取RSS-->比对数据+录入数据-->计算出更新后的数据-->传入下载提取函数-->发送文件-->删除文件树

RSSdata是独立的存储工作员，与主程序之间以rssdata.yaml关联


![v](https://github.com/sudoskys/BiliBiliVideoToMusic/raw/main/docs/workflow.png)


```
mermaid
graph TB

A(拉取RSS) ---比对录入--> B[数据]

B[数据] --> C{计算更新的条目?}

C{计算更新的条目?} -- NEW --> D[下载提取]

C{计算更新的条目?} -- NO new --> S

D[下载提取] --推送--> E[TG]
E --成功则删除数据--> B

E[TG] --> S[写入报告]
```

### 目录结构描述
```
.
├── data
│  ├── public.cer    //公钥
│  ├── rssdata.yaml   //自动化填入的
│  └── userdata.yaml   //手动填入的
├── docs   //文档
│  └── workflow.png
├── err.txt   //本地调试报错日志
├── LICENSE   //协议
├── LICENSE.txt
├── linuxdown_audio.py   //  rss测试版本， 歌单下载，因为api受限
├── gitPush.py    //  rss推送版本， github action 运行目标
├── log.txt
├── main.py  // linux&win都可以用的交互式下载版本
├── mods
│  
│  │ 
│  └── rsatool.py  //rsa支持
├── o365_token.txt   //加密后的token ，运行时解密
├── README-CN.md
├── README.md
├── requirements.txt
├── targets.txt
└── test
    ├── err.txt
    ├── log.txt
    ├── tokensetup.py  //token 设置自动生成
    └── t_video.py

```

## TODO
- [x] 实现下载功能
- [x] 实现取新条目功能
- [x] 实现推送功能
- [ ] 实现多源多目标推送


## 贡献
🚧 详见TODO

## 鸣谢

- [BV号转AV号](https://www.zhihu.com/question/381784377/answer/1099438784)|Youget修复算法实现|
- [O365](https://github.com/O365/python-o365) |微软云盘同步实现|
- [RSShub](https://docs.rsshub.app/) |数据源RSS|


## 支持
THIS link: https://azz.net/ly233
[![](https://static01.imgkr.com/temp/5808cb7e9e6340409bd07afc0e5ca723.png)](https://azz.net/ly233)

------------------------------

![a](https://tva1.sinaimg.cn/large/87c01ec7gy1fsnqqlbdzjj21kw0w07is.jpg)


