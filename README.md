## BiliBiliVideoToMusic

This docs from translate.google


![counter](https://count.getloli.com/get/@sudoskys-github-BiliBiliVideoToMusic?theme=moebooru)

[![MIT License](https://img.shields.io/badge/LICENSE-MIT-ff69b4)](http://choosealicense.com/licenses/mit/) ![u](https://img.shields.io/badge/USE-python-green) [![s](https://img.shields.io/badge/Sponsor-Alipay-ff69b4)](https://azz.net/ly233)

![v](https://img.shields.io/badge/Version-220116-9cf)

### [English机翻](README.md) | [中文点这里！](README-CN.md)

## introduce

Bilibili video download and extract audio for wav and flac TG-RSS version video second-pass extraction and push.
This project allows you to synchronize the music of your favorite Erchuang video to the specified TG group, and use RShub to provide data support.


## TODO
- [x] Implement download function
- [x] Implement the function of fetching new entries
- [x] Implement push function
- [ ] Realize multi-source multi-target push

## Features
🛠 MAIN can run on windows system, supports sticking music labels and optionally saving flv and wav files. (modify the file yourself...)

🚧 If you use action deployment, the function is only to extract flac. To configure this action, you need to add keys in the environment, one is token and the other is email. (Apply for github openapi token by yourself https://github.com/settings/tokens/new)

🎤 The sound quality should be the same as the video heard

## Notice
⚠ Execute up to 20 push tasks each time.

⚠ Do not push super long videos (>10min) to avoid risks

⚠ Liunx deploys RSS push see music.yml, the variables need to be configured manually.

## Start
### 1. Installation Requirements

 **Python 3.7 or higher**
````
python -m pip install --upgrade pip

pip install setuptools wheel twine bs4 requests tabulate mutagen pydub you_get moviepy pyTelegramBotAPI feedparser
````
- FFmpeg environment [ffmpeg](https://ffmpeg.org/download.html#get-packages).
(This repository Action uses  https://github.com/marketplace/actions/setup-ffmpeg )
* Install necessary packages locally by running `pip install bs4 requests tabulate mutagen pydub you_get moviepy`
* Push service installation robot API library and RSS parsing library `pip install pyTelegramBotAPI feedparser`

### 2. Preparation

#### select file version
````
linuxdown_git.py --->RSS auto editon
mains.py --->win&linux edition
````

#### RSS feed users
* source (linuxdown_git.py)

You need to build [Rsshub](https://docs.rsshub.app/) to get web sources, or use the services of public projects! See .

* Fork this repository and set secrets

Tips: If you use action deployment, it is recommended to only set extraction flac.
To configure this action, you need to add secrets to the environment, one is github token and the other is email. (Apply for [github openapi token](https://github.com/settings/tokens/new)

**Add Repository secrets**
````
>token
>objectID
>rssurl
````
````
token = ***** # bot token, use tg@BotFather, google by yourself
objectID = ***** # channal id ,please use tg@getidsbot get this value!
rssurl = **** # rssurl, see https://docs.rsshub.app/
````

**Add Environment secrets**
````
>token # github token, use https://github.com/settings/tokens/new
>email # your email address
````

⚠ Be careful to distinguish between two tokens.

* run
Github action runs the process once a day at 6:20, and the repository owner plus stars will also trigger the process.

#### Standalone use
USE mains.py just follow the comments.


## Implementation logic (linuxdown_git.py)

> For the specific code, see linuxdown_git.py (main.py is used in the windows environment)
Pull RSS-->Compare data + input data-->Calculate the updated data-->Incoming download extraction function-->Send file-->Delete file tree


![v](https://github.com/sudoskys/BiliBiliVideoToMusic/raw/main/docs/workflow.png)



### Directory structure description
````
├── Readme.md // help
├── history_name.txt // The title corresponding to the history link
├── history_target.txt // History link
├── log.txt // log
├── linuxdown_git.py // rss push version, github action run target
└── mains.py // Interactive download version available for both linux & win
````

## Contribute
🚧 The OneDrive branch of this project is stuck at [onedrive upload sync function]-->[onedrive_upload implementation]-->[upload failed, no authorization token is empty]


## Quote

| URL | Author |
| --- | ------------- |
| [BV number to AV number](https://www.zhihu.com/question/381784377/answer/1099438784) | mcfx |


## Support me

THIS link: https://azz.net/ly233

[![d](https://img.shields.io/badge/Sponsor-me-ff69b4)](https://azz.net/ly233)







------------------------------

![a](https://tva1.sinaimg.cn/large/87c01ec7gy1fsnqqlbdzjj21kw0w07is.jpg)
