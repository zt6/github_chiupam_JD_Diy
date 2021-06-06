#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-06 12:34
# @Version  : v 2.2
# @Updata   : 1. 恢复了 /checkcookie 指令的正常工作
# @Future   : 


from .. import chat_id, jdbot, _ConfigDir, _ScriptsDir, _OwnDir, _LogDir, logger, TOKEN
from ..bot.utils import cmd, press_event, backfile, jdcmd, _DiyDir
from telethon import events, Button
from asyncio import exceptions
import requests, re, os, asyncio


bot_id = int(TOKEN.split(':')[0])


# 从 config.sh 中读取最新的 cookies
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


# 监测到机器人发送 cookie 失效信息时，自动屏蔽此账号
# @jdbot.on(events.NewMessage(from_users=bot_id, pattern=r'.*cookie.*已失效'))
# async def myexpiredcookie(event):
#     """
#     当监测到 Cookie 失效时第一时间屏蔽此账号并发送提醒
#     :param event:
#     :return:
#     """
#     try:
#         path = f'{_ConfigDir}/config.sh'
#         message = event.message.text
#         m = message.split('\n')
#         for n in m:
#             if n.find('京东账号') != -1:
#                 expired = ''.join(re.findall(r'\d', n.split(' ')[0]))
#                 msg = await jdbot.send_message(chat_id, f'监测到京东账号{expired}的 cookie 已过期，正在自动屏蔽')
#                 break
#         with open(path, 'r', encoding='utf-8') as f1:
#             configs = f1.readlines()
#         for config in configs:
#             if config.find('TempBlockCookie') != -1 and configs[configs.index(config) + 1].find(';;\n') == -1 and config.find('举例') == -1:
#                 Templine = configs.index(config)
#                 tbcookies = re.findall(r'\d', config)
#                 break
#         edit = False
#         if tbcookies != []:
#             if str(expired) in tbcookies:
#                 del(tbcookies[tbcookies.index(expired)])
#                 edit = True
#         else:
#             tbcookies = [expired]
#             edit = True
#         if edit:
#             n = " ".join('%s' % tbcookie for tbcookie in tbcookies)
#             configs[Templine] = f'TempBlockCookie="{n}"\n'
#             await jdbot.edit_message(msg, f'成功屏蔽，请及时发送/getcookie指令\n当cookie生效后请发送/checkcookie指令')
#             with open(path, 'w', encoding='utf-8') as f2:
#                 f2.write(''.join(configs))
#         else:
#             await jdbot.edit_message(msg, f'早前就已经屏蔽了京东账号{expired}的 cookie ，无需再次屏蔽')
#     except Exception as e:
#         await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
#         logger.error('something wrong,I\'m sorry\n' + str(e))


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
@jdbot.on(events.NewMessage(from_users=[chat_id, bot_id], pattern=r'^/checkcookie|.*cookie已失效'))
async def mycheckcookie(event):
    """
    自动检测cookie的过期情况
    :param event:
    :return:
    """
    try:
        path = f'{_ConfigDir}/config.sh'
        await jdbot.send_message(chat_id, '正在检测 cookie 过期情况')
        with open(path, 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        if configs[-1] == '\n':
            del(configs[-1])
        Templines = []
        Templines_data = []
        for config in configs:
            if config.find('TempBlockCookie') != -1 and config.find('#') == -1:
                Templines.append(configs.index(config))
                Templines_data.append(re.findall(r'\d', config))
        edit = True
        expireds = checkCookie1()[0]
        for Templine in Templines:
            tbcookies = Templines_data[Templines.index(Templine)]
            if tbcookies != [] and expireds != []:
                for expired in expireds:
                    tbcookies.append(expired)
            elif tbcookies != [] and expireds == []:
                tbcookies = []
            elif tbcookies == [] and expireds != []:
                for expired in expireds:
                    tbcookies.append(expired)
            else:
                edit = False
            if edit:
                tbcookies = list(set(list(map(int, tbcookies))))
                n = " ".join('%s' % tbcookie for tbcookie in tbcookies)
                configs[Templine] = f'TempBlockCookie="{n}"\n'
                await jdbot.send_message(chat_id, f'修改后的屏蔽情况变更为：\n文件第{Templine + 1}行 TempBlockCookie="{n}"')
                with open(path, 'w', encoding='utf-8') as f2:
                    f2.write(''.join(configs))
            else:
                await jdbot.send_message(chat_id, f'无需改动 TempBlockCookie 的值\n你目前配置内屏蔽情况为：\n文件第{Templine + 1}行 {configs[Templine]}')
        path = f'{_ConfigDir}/config.sh'
        await jdbot.send_file(chat_id, path)
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


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'https?://raw\S*'))
async def mycodes(event):
    """
    用户发送 raw 链接后自动下载链接文件
    :param event:
    :return:
    """
    try:
        SENDER = event.sender_id
        msg = await jdbot.send_message(chat_id, '请稍后正在下载文件')
        url = event.raw_text
        if url.startswith('https://raw.githubusercontent.com'):
            url = f'http://ghproxy.com/{url}'
        fname = url.split('/')[-1]
        resp = requests.get(url).text
        markup = [
            [Button.inline('放入config', data=_ConfigDir), Button.inline('放入scripts', data=_ScriptsDir), Button.inline('放入OWN文件夹', data=_DiyDir)], 
            [Button.inline('放入scripts并运行', data='node1'), Button.inline('放入OWN并运行', data='node'), Button.inline('取消', data='cancel')]
        ]
        if resp:
            cmdtext = None
            async with jdbot.conversation(SENDER, timeout=30) as conv:
                await jdbot.delete_messages(chat_id, msg)
                msg = await conv.send_message('请选择您要放入的文件夹或操作：\n')
                msg = await jdbot.edit_message(msg, '请选择您要放入的文件夹或操作：', buttons=markup)
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                write = True
                if res == 'cancel':
                    write = False
                    msg = await jdbot.edit_message(msg, '对话已取消')
                    conv.cancel()
                elif res == 'node':
                    path, cmdtext = f'{_DiyDir}/{fname}', f'{jdcmd} {_DiyDir}/{fname} now'
                    await jdbot.edit_message(msg, '脚本已保存到DIY文件夹，并成功在后台运行，请稍后自行查看日志')
                    conv.cancel()
                elif res == 'node1':
                    path, cmdtext = f'{_ScriptsDir}/{fname}', f'{jdcmd} {_ScriptsDir}/{fname} now'
                    await jdbot.edit_message(msg, '脚本已保存到scripts文件夹，并成功在后台运行，请稍后自行查看日志')
                    conv.cancel()
                else:
                    path = f'{res}/{fname}'
                    await jdbot.edit_message(msg, fname+'已保存到'+res+'文件夹')
            if write:
                backfile(path)
                with open(path, 'w+', encoding='utf-8') as f:
                    f.write(resp)
            if cmdtext:
                await cmd(cmdtext)
    except exceptions.TimeoutError:
        msg = await jdbot.send_message(chat_id, '选择已超时，对话已停止')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n'+str(e))
        logger.error('something wrong,I\'m sorry\n'+str(e))
