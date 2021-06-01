#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-01 16:20
# @Version  : v1.5
# @Updata   : 1. 修改了 getBwan() 函数；
# @Future   : 1. Null


# --------------------------------------------------------------------------------------- #
# 声明：
#     此脚本是根据布道场群文件 shopbean.py(v1.1) 改写的，并非完全自创
# 已有功能：
#     1. 解析 GET 请求后的包，以及其推送到 Telegram Bot 的消息会更加美观
#     2. 同时监控龙王庙频道，截取RRA，配合 redrain.py 定时使用（但 redrain.py 正在测试，因此未启用）
#     3. 给机器人发送 /checkcookie 命令即可临时屏蔽所有失效 cookie
# 使用方法：（直链: https://t.me/monk_dust_channel/692）
#     1. 存储路径：/jd/jbot/diy/（如果没有需要重新映射此文件夹）
#     2. 进入容器：docker exec -it jd bash
#     3. 停机器人：pm2 stop jbot
#     4. 开机器人：python3 -m jbot
#     5. 登陆后按 Ctrl + C 退出前台
#     6. 后台启动：pm2 start jbot
# 报错处理：（直链：https://t.me/monk_dust_channel/714）
#     一、 机器人交互没有反应，或者测试没有反应
#         1. docker exec -it jd bash
#         2. rm shopbean.session
#         3. pm2 stop jbot
#         4. python -m jbot
#         5. 登陆后按 Ctrl + C 退出前台
#         6. pm2 start jbot
# --------------------------------------------------------------------------------------- #


from .. import chat_id, api_hash, api_id, proxystart, proxy, jdbot, _LogDir, _ConfigDir
from ..bot.utils import cookies
from telethon import events, TelegramClient
import requests, re


if proxystart:
    client = TelegramClient("shopbean", api_id, api_hash, proxy=proxy, connection_retries=None).start()
else:
    client = TelegramClient("shopbean", api_id, api_hash, connection_retries=None).start()


def getbean(i, cookie, url):
    """
    发起 GET 请求
    :param i: 账号
    :param cookie: 传入Cookie
    :param url: 传入 GET 所需的 url
    :return: 返回推送的消息主体
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Cookie": cookie,
    }
    result, o = '', '\n\t\t└'
    try:
        r = requests.get(url=url, headers=headers)
        r.encoding = r.apparent_encoding
        res = r.json()
        if res['code'] == '0':
            followDesc = res['result']['followDesc']
            if followDesc.find('成功') != -1:
                try:
                    for n in range(len(res['result']['alreadyReceivedGifts'])):
                        redWord = res['result']['alreadyReceivedGifts'][n]['redWord']
                        rearWord = res['result']['alreadyReceivedGifts'][n]['rearWord']
                        result += f"{o}领取成功，获得{redWord}{rearWord}"
                except:
                    giftsToast = res['result']['giftsToast'].split(' \n ')[1]
                    result = f"{o}{giftsToast}"
            elif followDesc.find('已经') != -1:
                result = f"{o}{followDesc}"
    except Exception as e:
        result = f"{o}访问发生错误：{e}\n返回的包：{r.text}"
    return f"\n京东账号{i}{result}\n"


def checkCookie1():
    """
    检测 Cookie 是否过期
    :return: 返回过期的 Cookie 的账号数字列表
    """
    m = []
    for cookie in cookies:
        Expired = checkCookie2(cookie)
        if Expired:
            m.append(cookies.index(cookie) + 1)
    return m


def checkCookie2(cookie):
    """
    检测 Cookie 是否过期
    :param cookie: 传入 Cookie
    :return: 返回是否过期
    """
    url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    headers = {
        "Host": "me-api.jd.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "User-Agent": "jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
        "Accept-Language": "zh-cn",
        "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
        "Accept-Encoding": "gzip, deflate, br"
    }
    r = requests.get(url, headers=headers, proxies={"http": None, "https": None})
    if r.ok:
        res = r.json()
        if res['retcode'] == '1001':
            return True
        else:
            return False
    else:
        return False


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


@client.on(events.NewMessage(from_users=chat_id, pattern=r'^/checkcookie'))
async def check():
    """
    临时屏蔽某个cookie
    """
    m = checkCookie1()
    msg = await jdbot.send_message(chat_id, '正在自动检测 cookie 过期情况......')
    if m == []:
        await jdbot.edit_message(msg, '没有 Cookie 过期，无需临时屏蔽')
    else:
        n = " ".join('%s' % i for i in m)
        path = f'{_ConfigDir}/config.sh'
        with open(path, 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        for config in configs:
            if config.find('TempBlockCookie=""') != -1:
                i = configs.index(config)
                configs[i] = f'TempBlockCookie="{n}"\n'
                with open(path, 'w', encoding='utf-8') as f2:
                    print(''.join(configs), file=f2)
                await jdbot.edit_message(msg, f'已临时屏蔽Cookie{n}')
                break
            elif config.find('AutoDelCron') != -1:
                break
            elif config.find(f'TempBlockCookie="{n}"') != -1:
                await jdbot.edit_message(msg, f'早时已临时屏蔽Cookie{n}，无需再次屏蔽')
                break


@client.on(events.NewMessage(from_users=chat_id, pattern=r'^/untempblockcookie'))
async def check():
    """
    取消屏蔽某个cookie
    """
    msg = await jdbot.send_message(chat_id, '正在自动检测 cookie 屏蔽情况......')
    path = f'{_ConfigDir}/config.sh'
    with open(path, 'r', encoding='utf-8') as f1:
        configs = f1.readlines()
    del(configs[-1])
    for config in configs:
        if config.find('TempBlockCookie') != -1 and config.find('举例') == -1 and configs[configs.index(config) + 1].find(';;\n') == -1:
            m = re.findall(r'\d', config)
            if m != []:
                for n in m:
                    Expired = checkCookie2(cookies[int(n) - 1])
                    if not Expired:
                        del(m[m.index(n)])
                        await jdbot.edit_message(msg, f'取消临时屏蔽 Cookie{n} 成功')
                if m != []:
                    x = ' '.join(m)
                    configs[configs.index(config)] = f'TempBlockCookie="{x}"\n'
                else:
                    configs[configs.index(config)] = f'TempBlockCookie=""\n'
                    await jdbot.edit_message(msg, '取消屏蔽所有 Cookie 成功')
                with open(path, 'w', encoding='utf-8') as f2:
                        print(''.join(configs), file=f2)
            else:
                print(False)
                await jdbot.edit_message(msg, '没有 Cookie 被临时屏蔽')
        elif config.find('AutoDelCron') != -1:
            break
