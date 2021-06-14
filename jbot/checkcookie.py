#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam
# @Data     : 2021-06-13
# @Version  : v 1.0
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, logger, TOKEN
from ..bot.utils import press_event, V4, QL, _ConfigFile, myck
from telethon import events, Button
from asyncio import exceptions
import requests, re, os, asyncio


bot_id = int(TOKEN.split(':')[0])


def checkCookie1():
    expired = []
    cookies = myck(_ConfigFile)
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
        r = requests.get(url, headers=headers).json()
        if r['retcode'] == '1001':
            return True
        else:
            return False
    except:
        return False


@jdbot.on(events.NewMessage(from_users=[chat_id, bot_id], pattern=r'^/checkcookie$|.*cookie已失效'))
async def mycheckcookie(event):
    try:
        msg = await jdbot.send_message(chat_id, '正在检测 cookie 过期情况')
        expireds = checkCookie1()[0]
        text, o = '检测结果\n\n', '\n\t   └ '
        edit = False
        with open(_ConfigFile, 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        if V4:
            for config in configs:
                i = configs.index(config)
                if config.find("TempBlockCookie") != -1 and config.find("##") == -1 and configs[i + 1].find(";") == -1:
                    line = configs.index(config)
                    Temp = configs[line][:-1]
                    configs[line] = f"{Temp}program\n"
                    configs = ''.join(configs)
                    break
                elif config.find("AutoDelCron") != -1:
                    await jdbot.edit_message(msg, "无法寻找到目标行，请使用初始配置")
                    return
            n = " ".join('%s' % expired for expired in expireds)
            configs = re.sub(r'TempBlockCookie=".*"program', f'TempBlockCookie="{n}"', configs, re.M)
            text += f'【屏蔽情况】{o}TempBlockCookie="{n}"\n'
            edit = True
        elif QL:
            with open(_ConfigFile, 'r', encoding='utf-8') as f1:
                configs = f1.readlines()
            if configs[-1] == '\n':
                del (configs[-1])
            for expired in expireds:
                cookie = configs[int(expired) - 1]
                pt_pin = cookie.split(';')[-2]
                del (configs[int(expired) - 1])
                text += f'【删除情况】{pt_pin}{o}已经删除第 {expired} 个用户的Cookie\n'
                edit = True
        else:
            await jdbot.edit_message(msg, '未知环境的用户，无法使用 /checkcookie 指令')
            return
        if V4:
            with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                f2.write(configs)
            await jdbot.edit_message(msg, text)
        elif edit and QL:
            with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                f2.write(''.join(configs))
            await jdbot.edit_message(msg, text)
        else:
            await jdbot.edit_message(msg, '配置无需改动，可用cookie中并没有cookie过期')
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
