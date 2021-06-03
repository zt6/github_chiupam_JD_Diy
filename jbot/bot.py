#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-04 1:14
# @Version  : v 2.0
# @Updata   : 1. 将原来的脚本分开，user.py 需要登录 telegram，但是 bot.py 不需要登录
# @Future   : 1. 继续完善 redrain 红包雨


from .. import chat_id, jdbot, _LogDir, _ConfigDir, logger
from ..bot.utils import cookies, cmd, press_event
from telethon import events, Button
from asyncio import exceptions
import requests, re, os, json, asyncio


with open(f'{_ConfigDir}/bot.json', 'r', encoding='utf-8') as botf:
    bot_id = int(json.load(botf)['bot_token'].split(':')[0])


def press_event(user_id):
    return events.CallbackQuery(func=lambda e: e.sender_id == user_id)


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


# 监测到机器人发送 cookie 失效信息时，自动屏蔽此账号
@jdbot.on(events.NewMessage(from_users=bot_id, pattern=r'.*cookie.*已失效'))
async def myexpiredcookie(event):
    """
    当监测到 Cookie 失效时第一时间屏蔽此账号并发送提醒
    :param event:
    :return:
    """
    try:
        path = f'{_ConfigDir}/config.sh'
        message = event.message.text
        m = message.split('\n')
        for n in m:
            if n.find('京东账号') != -1:
                i = ''.join(re.findall(r'\d', n.split(' ')[0]))
                msg = await jdbot.send_message(chat_id, f'监测到京东账号{i}的 cookie 已过期，正在自动屏蔽')
                break
        with open(path, 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        for config in configs:
            if config.find('TempBlockCookie') != -1 and configs[configs.index(config) + 1].find(
                    ';;\n') == -1 and config.find('举例') == -1:
                z = configs.index(config)
                y = config[config.find('="') + 2:-2].split()
                if y != []:
                    if i in y:
                        await jdbot.edit_message(msg, f'早前就已经屏蔽了京东账号{i}的 cookie ，无需再次屏蔽')
                        break
                    else:
                        y.append(i)
                        i = ' '.join(y)
                        configs[z] = f'TempBlockCookie="{i}"\n'
                else:
                    configs[z] = f'TempBlockCookie="{i}"\n'
                with open(path, 'w', encoding='utf-8') as f2:
                    del (configs[-1])
                    print(''.join(configs), file=f2)
                await jdbot.edit_message(msg, '成功屏蔽')
            elif config.find('AutoDelCron') != -1:
                break
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


# 发送欢迎语
@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/start'))
async def myhello(event):
    """
    发送欢迎语
    :param event:
    :return:
    """
    try:
        diy_hello = """自定义机器人使用方法如下：
    /start 开始使用此自定义机器人
    /restart 重启机器人
    /help 获取机器人所有快捷命令，可直接发送至botfather
    /checkcookie 检测失效Cookie并临时屏蔽（暂不适用于青龙）

    仓库：https://github.com/chiupam/JD_Diy.git
    欢迎🌟Star & 提出🙋[isuss](https://github.com/chiupam/JD_Diy/issues/new) & 请勿🚫Fork
"""
        await asyncio.sleep(0.5)
        await jdbot.send_message(chat_id, diy_hello)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


# 获取自定义机器人的快捷命令
@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/help'))
async def myhelp(event):
    """
    发送快捷命令
    :param event:
    :return:
    """
    try:
        diy_help = """restart - 重启机器人
checkcookie - 检测cookie过期
"""
        await asyncio.sleep(0.5)
        await jdbot.send_message(chat_id, diy_help)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


# 自动检测cookie的过期情况并临时屏蔽此账号
@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/checkcookie'))
async def mycheckcookie(event):
    try:
        expired = checkCookie1()
        msg = await jdbot.send_message(chat_id, '正在自动检测 cookie 过期情况')
        if expired != []:
            n = " ".join('%s' % i for i in expired)
            path = f'{_ConfigDir}/config.sh'
            with open(path, 'r', encoding='utf-8') as f1:
                configs = f1.readlines()
            for config in configs:
                if config.find('TempBlockCookie') != -1 and configs[configs.index(config) + 1].find(
                        ';;\n') == -1 and config.find('举例') == -1:
                    configs[configs.index(config)] = f'TempBlockCookie="{n}"\n'
                    with open(path, 'w', encoding='utf-8') as f2:
                        print(''.join(configs), file=f2)
                    await jdbot.edit_message(msg, f'以下是屏蔽的账号\n{n}')
                    break
                elif config.find('AutoDelCron') != -1:
                    break
        else:
            await jdbot.edit_message(msg, '没有 Cookie 过期，无需临时屏蔽')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


# 重启机器人
@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/restart'))
async def myrestart(event):
    """
    发送 /restart 重启机器人
    :param event:
    :return:
    """
    try:
        await jdbot.send_message(chat_id, '准备重启机器人……')
        os.system('pm2 restart jbot')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))

