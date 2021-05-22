"""
Author: Chiupam (https://t.me/chiupam)
version: Test v2
date: 2021-05-22
update: 1. 修复了日志报错的问题
"""


from .. import chat_id, api_hash, api_id, proxystart, proxy, jdbot, _LogDir
from ..bot.utils import cookies
from telethon import events, TelegramClient
import requests, re


'''
1. 存储路径：/jd/jbot/diy/
2. 进入容器：docker exec -it jd bash
3. 停机器人：pm2 stop jbot
4. 开机器人：python3 -m jbot
5. 按 Ctrl + C 退出前台
6. 后台启动：pm2 start jbot
'''


if proxystart:
    client = TelegramClient("diy", api_id, api_hash, proxy=proxy, connection_retries=None).start()
else:
    client = TelegramClient("diy", api_id, api_hash, connection_retries=None).start()


@client.on(events.NewMessage(from_users=chat_id))  # 监控机器人
@client.on(events.NewMessage(chats=[-1001197524983, -1001159808620]))  # 监控频道
async def my_event_handler(event):
    """
    监控消息并做出相应动作
    :param event: 
    """
    message = event.message.text

    # 参考 shopbean.py
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

    # RRA
    if 'RRA' in message:
        RRA = re.findall(r"RRA.*", message)
        input_RRA = '&'.join(RRA)
        start_time = re.findall(re.compile(r"开.*"), message)
        file = '-'.join(start_time[0].split(' ')[1].split(':')[:-1])
        with open(f'{_LogDir}/{file}.txt', 'w', encoding='utf-8') as f:
            print(input_RRA, file=f)


# 参考 shopbean.py
def getbean(i, cookie, url):
    """
    发起 GET 请求
    :param i: 0
    :param cookie: cookie
    :param url: url
    :return: result
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
    return f"\n京东账号{i}{result}\n"

