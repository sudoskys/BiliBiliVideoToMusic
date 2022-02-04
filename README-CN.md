## BiliBiliVideoToMusic
![counter](https://count.getloli.com/get/@sudoskys-github-BiliBiliVideoToMusic?theme=moebooru)

[![MIT License](https://img.shields.io/badge/LICENSE-MIT-ff69b4)](http://choosealicense.com/licenses/mit/)   ![u](https://img.shields.io/badge/USE-python-green)   [![s](https://img.shields.io/badge/Sponsor-Alipay-ff69b4)](https://azz.net/ly233)
![v](https://img.shields.io/badge/Version-1.0.2-9cf)  

### [English](README.md)  | [中文](README-CN.md) 

## 介绍

哔哩哔哩视频下载提取音频为wav与flac   TG-RSS版本视频二传提取推送。
此项目可以让你同步收藏夹二创视频的音乐到指定TG群组，使用RSShub提供数据支持。


## TODO
- [x] 实现下载功能
- [x] 实现取新条目功能
- [x] 实现推送功能
- [ ] 实现多源多目标推送

## 特性
🛠 MAIN可以在windows系统上运行，支持贴音乐标签与可选保存flv和wav文件。（自己改动文件.....）

🚧 如果您使用action部署，功能仅有提取flac。配置这个action，需要在环境内加密钥，一个是token，一个是email。（自己申请github openapi token https://github.com/settings/tokens/new）

🎤 音质应该和视频听到的是一样的

## 注意
⚠ 每次最多执行20个推送任务.

⚠ 请勿推送超长视频(>10min)，避免风险

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

#### RSS推送用户
* 源(linuxdown_git.py)
需要自建 [Rsshub](https://docs.rsshub.app/) 来获得网络源，或者使用公开项目的服务！详见  .

* Fork 本仓库并设置secrets
Tips: 如果您使用action部署，建议只设置提取flac。
配置此action，需要在环境内加secrets，一个是githubtoken，一个是email。（自己申请[github openapi token](https://github.com/settings/tokens/new)

**Add Repository secrets**
```
>token
>objectID
>rssurl
```
```
token = ***** # bot token，use tg@BotFather，自行google
objectID = ***** # channal id ,please use tg@getidsbot get this value!
rssurl = ****  # rssurl，详见 https://docs.rsshub.app/
```

**Add Environment secrets**
```
>token # github token，use https://github.com/settings/tokens/new
>email # your email address
```

⚠注意区分两个token.

* 运行
Github action每天6:20运行一次流程，仓库主人加星也会触发流程.

#### 独立使用
USE mains.py  按照注释来即可.


## 实现逻辑(linuxdown_git.py)

>具体代码详见 linuxdown_git.py （windows环境下使用main.py）
拉取RSS-->比对数据+录入数据-->计算出更新后的数据-->传入下载提取函数-->发送文件-->删除文件树





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
├── Readme.md                   // help
├── history_name.txt                         // 历史链接对应的标题
├── history_target.txt                       // 历史链接
├── log.txt                   // log
├── linuxdown_git.py  //  rss推送版本， github action 运行目标
└── mains.py   // linux&win都可以用的交互式下载版本
```

## 贡献
🚧 此项目的OneDrive分支卡死在[onedrive上传同步功能]-->[onedrive_上传实现]-->[上传失败无授权token is empty]


## 引用

| URL | 作者 |
| --- | ----------- | 
| [BV号转AV号](https://www.zhihu.com/question/381784377/answer/1099438784) | mcfx |


## 支持我
THIS link: https://azz.net/ly233
[![](https://static01.imgkr.com/temp/5808cb7e9e6340409bd07afc0e5ca723.png)](https://azz.net/ly233)

------------------------------

![a](https://tva1.sinaimg.cn/large/87c01ec7gy1fsnqqlbdzjj21kw0w07is.jpg)


