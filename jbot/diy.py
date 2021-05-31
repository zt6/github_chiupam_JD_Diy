"""
Author: unknow & Chiupam (https://t.me/chiupam)
version: v1.2
date: 2021-05-25
update: 1. 添加说明；2. 是否兼容青龙请自行测试
"""

"""
声明：
    此脚本是根据布道场群文件 shopbean.py(v1.1) 改写的，并非完全自创
添加功能：
    1. 解析 GET 请求后的包，以及其推送到 Telegram Bot 的消息会更加美观
    2. 同时监控龙王庙频道，截取RRA，配合 redrain.py 定时使用（但 redrain.py 正在测试，因此未启用）
使用方法：（直链: https://t.me/monk_dust_channel/692）
    1. 存储路径：/jd/jbot/diy/（如果没有需要重新映射此文件夹）
    2. 进入容器：docker exec -it jd bash
    3. 停机器人：pm2 stop jbot
    4. 开机器人：python3 -m jbot
    5. 登陆后按 Ctrl + C 退出前台
    6. 后台启动：pm2 start jbot
报错处理：（直链：https://t.me/monk_dust_channel/714）
    一、 机器人交互没有反应，或者测试没有反应
        1. docker exec -it jd bash
        2. rm shopbean.session
        3. pm2 stop jbot
        4. python -m jbot
        5. 登陆后按 Ctrl + C 退出前台
        6. pm2 start jbot
"""


from .. import chat_id, api_hash, api_id, proxystart, proxy, jdbot, _LogDir
from ..bot.utils import cookies
from telethon import events, TelegramClient
import requests, re


if proxystart:
    client = TelegramClient("shopbean", api_id, api_hash, proxy=proxy, connection_retries=None).start()
else:
    client = TelegramClient("shopbean", api_id, api_hash, connection_retries=None).start()

    
@client.on(events.NewMessage(chats=-1001197524983)) # 监控布道场频道
async def shopbean(event):
    """
    监控布道场
    """
    message = event.message.text
    url = re.findall(re.compile(r"[(](https://api\.m\.jd\.com.*?)[)]", re.S), message)
    if url != [] and len(cookies) > 0:
        i = 0
        info = '关注店铺\n' + message.split("\n")[0] + "\n"
        for cookie in cookies:
            try:
                i += 1
                info += getbean(i, cookie, url[0])
            except Exception as error:
                await jdbot.send_message(chat_id, f'\n京东账号{i}\n\t └【错误】{str(error)}')
                continue
        await jdbot.send_message(chat_id, info)

        
@client.on(events.NewMessage(chats=-1001159808620))  # 监控龙王庙频道
async def redrain(event):
    """
    监控龙王庙
    """
    message = event.message.text
    if 'RRA' in message:
        RRA = re.findall(r"RRA.*", message)
        input_RRA = '&'.join(RRA)
        start_time = re.findall(re.compile(r"开.*"), message)
        file = '-'.join(start_time[0].split(' ')[1].split(':')[:-1])
        with open(f'{_LogDir}/{file}.txt', 'w', encoding='utf-8') as f:
            print(input_RRA, file=f)


def getbean(i, cookie, url):
    """
    发起 GET 请求
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Cookie": cookie,
    }
    res = requests.get(url=url, headers=headers).json()
    if res['code'] == '0':
        followDesc = res['result']['followDesc']
        if followDesc.find('成功') != -1:
            try:
                result = ""
                for n in range(len(res['result']['alreadyReceivedGifts'])):
                    redWord = res['result']['alreadyReceivedGifts'][n]['redWord']
                    rearWord = res['result']['alreadyReceivedGifts'][n]['rearWord']
                    result += f"\n\t\t└领取成功，获得{redWord}{rearWord}"
            except:
                giftsToast = res['result']['giftsToast'].split(" \n ")[1]
                result = f"\n\t\t└{giftsToast}"
        elif followDesc.find('已经') != -1:
            result = f"\n\t\t└{followDesc}"
        else:
            result = res
    return f"\n京东账号{i}{result}\n"

