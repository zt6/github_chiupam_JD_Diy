#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-08 00:46
# @Version  : v 2.2
# @Updata   : 1. 监控我的频道，及时更新最新的user.py和bot.py
# @Future   : 1. 


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

    
if not os.path.isfile('/jd/jbot/diy/bot.py'):
    os.system(f'cd /jd/jbot/diy/ && wget https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py')
    if os.path.isfile('/jd/jbot/diy/bot.py'):
        os.system('pm2 restart jbot')

        
# 从 config.sh 中读取 cookies
def readCookies():
    """
    读取 cookie
    :return: 最新的 cookies 列表
    """
    ckreg = re.compile(r'pt_key=\S*;pt_pin=\S*;')
    with open(f'{_ConfigDir}/config.sh', 'r', encoding='utf-8') as f:
        lines = f.read()
    cookies = ckreg.findall(lines)
    for cookie in cookies:
        if cookie == 'pt_key=xxxxxxxxxx;pt_pin=xxxx;':
            cookies.remove(cookie)
            break
    return cookies


# 检查 cookie 是否过期的第一个函数
def checkCookie1():
    """
    检测 Cookie 是否过期
    :return: 返回过期的 Cookie 的账号数字列表
    """
    expired = []
    cookies = readCookies()
    for cookie in cookies:
        cknum = cookies.index(cookie) + 1
        if checkCookie2(cookie):
            expired.append(cknum)
    return expired, cookies


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


def checkCrontab(cron, PL, fname, fpath):
    """
    新旧命令对比，有新命令则写入新命令
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


# @client.on(events.NewMessage(chats=-1001159808620, pattern=r'.*雨'))
# async def myredrain(event):
#     """
#     截取RRA
#     :param event:
#     :return:
#     """
#     RRA = re.findall(r"RRA.*", event.message.text)
#     input_RRA = '&'.join(RRA)
#     start_time = re.findall(re.compile(r"开.*"), event.message.text)
#     file = '-'.join(start_time[0].split(' ')[1].split(':')[:-1])
#     with open(f'{_LogDir}/{file}.txt', 'w', encoding='utf-8') as f:
#         print(input_RRA, file=f)
        
        
# @client.on(events.NewMessage(chats=-1001159808620, pattern=r'.*雨'))
# async def redrain(event):
#     """
#     替换修改 redrain.js 的 RRA
#     :param event:
#     :return:
#     """
#     try:
#         fname = '整点京豆雨'
#         fpath = f'{_ScriptsDir}/redrain_chiupam.js'
#         if not os.path.isfile(fpath):
#             f_url = 'https://raw.githubusercontent.com/chiupam/JD_Diy/main/redrain_chiupam.js'
#             cmdtext = f'cd {_ScriptsDir} && wget -t 3 {f_url}'
#             os.system(cmdtext)
#         checkCrontab("0 0 5 1 *", "otask", fname, fpath)
#         messages = event.raw_text.split('\n')
#         rras = []
#         times = []
#         for message in messages:
#             if "RRA" in message:
#                 rra = re.findall(r'RRA.*', message)[0]
#                 rras.append(rra)
#                 str_time = messages[messages.index(message) + 2].split(' ')[1].split(':')[0]
#                 if str_time.startswith('0'):
#                     str_time = str_time[1:]
#                 times.append(str_time)
#         with open(fpath, 'r', encoding='utf-8') as f1:
#             js = f1.readlines()
#         for line in js:
#             if line.find(f"'{times[0]}': 'RRA") != -1:
#                 js[js.index(line)] = f"  '{times[0]}': '{rras[0]}',\n"
#                 del(times[0])
#                 del(rras[0])
#             if rras == []:
#                 break
#         with open(fpath, 'w', encoding='utf-8') as f2:
#             f2.write(''.join(js))
#         await jdbot.send_message(chat_id, '已完成替换咯')
#     except Exception as e:
#         await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n'+str(e))


# 监控并更新文件
@client.on(events.NewMessage(chats=-1001431256850))
async def myupuser(event):
    """
    关注频道：https://t.me/jd_diy_bot_channel
    """
    try:
        if event.message.file:
            fname = event.message.file.name
            if fname.endswith("bot.py") or fname.endswith("user.py"):
                path = f'{_JdbotDir}/diy/{fname}'
                backfile(path)
                await client.download_file(input_location=event.message, file=path)
                await jdbot.send_file(chat_id, path, caption='已更新，准备重启')
                os.system('pm2 restart jbot')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
