#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-13 23:59
# @Version  : v 2.4
# @Updata   : 1.
# @Future   : 1.


from .. import chat_id, jdbot, _ConfigDir, logger, api_id, api_hash, proxystart, proxy, _ScriptsDir, _JdbotDir
from ..bot.utils import cmd, press_event, backfile, jdcmd, _DiyDir, V4, QL, _ConfigFile, myck
from telethon import events, TelegramClient
import re, json, requests, os, asyncio


if proxystart:
    client = TelegramClient("user", api_id, api_hash, proxy=proxy, connection_retries=None).start()
else:
    client = TelegramClient("user", api_id, api_hash, connection_retries=None).start()


with open(f'{_ConfigDir}/bot.json', 'r', encoding='utf-8') as botf:
    bot_id = int(json.load(botf)['bot_token'].split(':')[0])


if not os.path.isfile('/jd/jbot/diy/bot.py') and V4:
    os.system(f'cd /jd/jbot/diy/ && wget https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py')
    if os.path.isfile('/jd/jbot/diy/bot.py'):
        os.system('pm2 restart jbot')
elif not os.path.isfile('/ql/jbot/diy/bot.py') and QL:
    os.system(f'cd /ql/jbot/diy/ && wget https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py')
    if os.path.isfile('/ql/jbot/diy/bot.py'):
        os.system('pm2 restart jbot')


def checkCookie1():
    expired = []
    cookies = myck()
    for cookie in cookies:
        cknum = cookies.index(cookie) + 1
        if checkCookie2(cookie):
            expired.append(cknum)
    return expired, cookies


def checkCookie2(cookie):
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


def getbean(i, cookie, url):
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


# 监控组队瓜分ID
@client.on(events.NewMessage(chats=-1001169232926, pattern=r"^export\s"))
async def myexport(event):
    """
    监控组队瓜分ID
    关注频道：https://t.me/zuduifendou
    """
    try:
        message = event.message.text
        start = await jdbot.send_message(chat_id, "监控到新的 activityId，准备自动替换")
        kv = message.replace("export ", "").replace("*", "")
        kname = kv.split("=")[0]
        vname = re.findall(r"(\".*\"|'.*')", kv)[0][1:-1]
        with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
            configs = f1.read()
        if configs.find(kname) != -1:
            configs = re.sub(f'{kname}=(\"|\').*(\"|\')', kv, configs)
            end = "替换环境变量成功"
        else:
            if V4:
                with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f3:
                    configs = f3.readlines()
                for config in configs:
                    if config.find("第五区域") != -1 and config.find("↑") != -1:
                        end_line = configs.index(config)
                        break
                configs.insert(end_line - 2, f'export {kname}="{vname}"\n')
                configs = ''.join(configs)
            else:
                with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f4:
                    configs = f4.read()
                configs += f'export {kname}="{vname}"\n'
            end = "新增环境变量成功"
        with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f2:
            f2.write(configs)
        await asyncio.sleep(1.5)
        await jdbot.delete_messages(chat_id, start)
        await jdbot.send_message(chat_id, end)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


# 监控并更新文件
@client.on(events.NewMessage(chats=-1001431256850))
async def myupuser(event):
    """
    关注频道：https://t.me/jd_diy_bot_channel
    :param event:
    :return:
    """
    try:
        if event.message.file:
            fname = event.message.file.name
            try:
                if fname.endswith("bot.py") or fname.endswith("user.py"):
                    path = f'{_JdbotDir}/diy/{fname}'
                    backfile(path)
                    await client.download_file(input_location=event.message, file=path)
                    await jdbot.send_file(chat_id, path, caption='已更新，准备重启')
                    os.system('pm2 restart jbot')
            except:
                return
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))

