#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-04 1:14
# @Version  : v 2.0
# @Updata   : 1. 将原来的脚本分开，user.py 需要登录 telegram，但是 bot.py 不需要登录
# @Future   : 1. 继续完善 redrain 红包雨


from .. import chat_id, jdbot, _ConfigDir, logger, api_id, api_hash, proxystart, proxy, _ScriptsDir
from ..bot.utils import cookies
from telethon import events, TelegramClient
import re, json, requests, os

if proxystart:
    client = TelegramClient("diy", api_id, api_hash, proxy=proxy, connection_retries=None).start()
else:
    client = TelegramClient("diy", api_id, api_hash, connection_retries=None).start()

with open(f'{_ConfigDir}/bot.json', 'r', encoding='utf-8') as botf:
    bot_id = int(json.load(botf)['bot_token'].split(':')[0])


# 检查 cookie 是否过期的第一个函数
def checkCookie1():
    """
    检测 Cookie 是否过期
    :return: 返回过期的 Cookie 的账号数字列表
    """
    expired = []
    for cookie in cookies:
        if checkCookie2(cookie):
            expired.append(cookies.index(cookie) + 1)
    return expired


# 检查 cookie 是否过期的第二个函数
def checkCookie2(cookie):
    """
    检测 Cookie 是否过期
    :param cookiex: 传入 Cookie
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
    try:
        r = requests.get(url, headers=headers)
        if r.ok:
            res = r.json()
            if res['retcode'] == '1001':
                return True
            else:
                return False
        else:
            return False
    except:
        return False


# 新旧命令对比
def checkCrontab(cron, PL, fname, fpath):
    """
    新旧命令对比，有新命令则写入新命令
    :param cron: 传入 cron 表达式
    :param PL: 传入执行方式 python jtask otask
    :param fname: 传入文件名
    :param fpath: 传入文件路径
    :return:
    """
    crontab_list = f'{_ConfigDir}/crontab.list'
    key = f'# {fname}（请勿删除此行）\n'
    new = f'{cron} {PL} {fpath}\n'
    with open(crontab_list, 'r', encoding='utf-8') as f1:
        crontab = f1.readlines()
    if crontab[-1] == '\n':
        del(crontab[-1])
    if key in crontab:
        m = crontab.index(key) + 1
        if crontab[m] != new:
            crontab[m] = new
            with open(crontab_list, 'w', encoding='utf-8') as f2:
                f2.write(''.join(crontab))
    else:
        crontab.append(f'\n{key}{new}')
        with open(crontab_list, 'w', encoding='utf-8') as f2:
            f2.write(''.join(crontab))


# 监控布道场频道，检测到关键事件的触发时执行的函数
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
        else:
            result = f"{o}Cookie 可能已经过期"
    except Exception as e:
        if str(e).find('(char 0)') != -1:
            result = f"{o}访问发生错误：无法解析数据包"
        else:
            result = f"{o}访问发生错误：{e}"
    return f"\n京东账号{i}{result}\n"


# 监控布道场频道
@client.on(events.NewMessage(chats=-1001197524983, pattern=r'.*店'))
async def shopbean(event):
    """
    监控布道场
    :param event:
    :return:
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
            except:
                continue
        await jdbot.send_message(chat_id, info)


