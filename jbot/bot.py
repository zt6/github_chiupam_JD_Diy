#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-07 20:28
# @Version  : v 2.3
# @Updata   : 1. 下载文件支持更多链接格式，只要是已 raw 后的链接即可；2. 添加 /upbot 指令，可升级此自定义机器人；3. 更新了用户发送仓库链接后开始在 config.sh 中添加仓库的操作
# @Future   : 1. 优化 /checkcookie 指令的工作


from .. import chat_id, jdbot, _ConfigDir, _ScriptsDir, _OwnDir, _LogDir, logger, TOKEN, _JdbotDir
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
    /upbot 升级此自定义机器人
    /help 获取机器人所有快捷命令，可直接发送至botfather
    /checkcookie 检测失效Cookie并临时屏蔽（暂不适用于青龙）
    此外 1、发送已 raw 的链接会下载文件，并让用户做出选择
        2、发送仓库链接会开始添加仓库，用户按要求回复即可
        3、接受到 cookie 过期消息自动开启 /checkcookie 指令

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
upbot - 升级自定义机器人
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
        msg = await jdbot.send_message(chat_id, '正在检测 cookie 过期情况')
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
        expireds = checkCookie1()[0]
        text, o = '检测结果\n\n', '\n\t\t└'
        for Templine in Templines:
            tbcookies = Templines_data[Templines.index(Templine)]
            for expired in expireds:
                tbcookies.append(expired)
            tbcookies = list(set(list(map(int, tbcookies))))
            n = " ".join('%s' % tbcookie for tbcookie in tbcookies)
            configs[Templine] = f'TempBlockCookie="{n}"\n'
            text += f'【屏蔽情况】文件第{Templine + 1}行{o}TempBlockCookie="{n}"\n'
        with open(path, 'w', encoding='utf-8') as f2:
            f2.write(''.join(configs))
        await jdbot.edit_message(msg, text)
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

        
# 升级我的自定义机器人
@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/upbot'))
async def mynoconv(event):
    try:
        msg = await jdbot.send_message(chat_id, '开始下载最新的bot.py文件')
        furl = 'http://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/master/jbot/bot.py'
        fname = 'bot.py'
        resp = requests.get(furl).text
        if resp:
            path = f'{_JdbotDir}/diy/{fname}'
            backfile(path)
            with open(path, 'w+', encoding='utf-8') as f:
                f.write(resp)
            await jdbot.edit_message(msg, '准备重启机器人……')
            os.system('pm2 restart jbot')
        else:
            await jdbot.edit_message(msg, "下载失败，请稍后重试")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))

        
@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://(raw)?.*(github|GitHub)?.*(js|py|sh)$'))
async def mycodes(event):
    """
    用户发送 raw 链接后自动下载链接文件
    :param event:
    :return:
    """
    try:
        SENDER = event.sender_id
        msg = await jdbot.send_message(chat_id, '开启下载文件会话')
        btn = [
            [Button.inline('我确定需要下载此链接文件，请继续', data='confirm')], 
            [Button.inline('我不需要下载，请取消对话', data='cancel')]
            ]
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            await jdbot.delete_messages(chat_id, msg)
            msg = await conv.send_message('检测到你发送了一条链接，请做出你的选择：\n')
            msg = await jdbot.edit_message(msg, '检测到你发送了一条链接，请做出你的选择：', buttons=btn)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                msg = await jdbot.edit_message(msg, '对话已取消')
                conv.cancel()
            else:
                # 以下代码大部分参照原作者：@MaiKaDe666，并作出一定的修改
                await jdbot.delete_messages(chat_id, msg)
                furl = event.raw_text
                if furl.startswith('https://raw.githubusercontent.com'):
                    ufrl = f'http://ghproxy.com/{furl}'
                fname = ufrl.split('/')[-1]
                resp = requests.get(furl).text
                btn = [
                    [Button.inline('仅放入config目录', data=_ConfigDir), Button.inline('放入jbot/diy目录', data=f'{_JdbotDir}/diy')],
                    [Button.inline('仅放入scripts目录', data=_ScriptsDir), Button.inline('放入scripts目录并运行', data='node1')],
                    [Button.inline('仅放入own目录', data=_DiyDir), Button.inline('放入own目录并运行', data='node')],
                    [Button.inline('取消', data='cancel')]
                ]
                if resp:
                    write = True
                    cmdtext = None
                    msg = await conv.send_message('请做出你的选择：')
                    msg = await jdbot.edit_message(msg, '请做出你的选择：', buttons=btn)
                    convdata = await conv.wait_event(press_event(SENDER))
                    res = bytes.decode(convdata.data)
                    if res == 'cancel':
                        write = False
                        msg = await jdbot.edit_message(msg, '对话已取消')
                    elif res == 'node':
                        path, cmdtext = f'{_DiyDir}/{fname}', f'{jdcmd} {_DiyDir}/{fname} now'
                        await jdbot.edit_message(msg, '脚本已保存到DIY文件夹，并成功在后台运行，请稍后自行查看日志')
                    elif res == 'node1':
                        path, cmdtext = f'{_ScriptsDir}/{fname}', f'{jdcmd} {_ScriptsDir}/{fname} now'
                        await jdbot.edit_message(msg, '脚本已保存到scripts文件夹，并成功在后台运行，请稍后自行查看日志')
                    else:
                        path = f'{res}/{fname}'
                        await jdbot.edit_message(msg, f'{fname}已保存到{res}文件夹')
                    conv.cancel()
                    if write:
                        backfile(path)
                        with open(path, 'w+', encoding='utf-8') as f:
                            f.write(resp)
                    if cmdtext:
                        await cmd(cmdtext)
                else:
                    msg = await conv.send_message('下载失败，请稍后重试')
                    await jdbot.edit_message(msg, '下载失败，请稍后重试')
                    conv.cancel()
    except exceptions.TimeoutError:
        msg = await jdbot.send_message(chat_id, '选择已超时，对话已停止')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n'+str(e))
        logger.error('something wrong,I\'m sorry\n'+str(e))

  
@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://github\.com/\S+'))
async def myconv(event):
    """
    用户发送仓库链接后开始在 config.sh 中添加仓库
    :param event:
    :return:
    """
    try:
        start = await jdbot.send_message(chat_id, '开始添加仓库，请按提示进行选择或操作')
        SENDER = event.sender_id
        url = event.raw_text
        short_url = url.split('/')[-1].replace(".git", "")
        tips = [
            '正在设置 OwnRepoBranch 的值\n该值为你想使用脚本在[仓库]({url})的哪个分支', '正在设置 OwnRepoPath 的\n该值为你要使用的脚本在分支的哪个路径'
        ]
        tips_2 = [
            f'回复 main 代表使用 [{short_url}]({url}) 仓库的 "main" 分支\n回复 master 代表使用 [{short_url}]({url}) 仓库的 "master" 分支\n具体分支名称以你所发仓库实际为准\n', 
            f'回复 scripts/jd normal 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 scripts/jd 和 normal文件夹下\n回复 root cron 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 根目录 和 cron 文件夹下\n具体目录路径以你所发仓库实际为准\n'
            ]
        btns = [
            [[Button.inline('我使用仓库的 "默认" 分支', data='root')], [Button.inline('我使用仓库的 "main" 分支', data='main'), Button.inline('我使用仓库的 "master" 分支', data='master')], [Button.inline('请让我手动输入', data='input'), Button.inline('请帮我取消对话', data='cancel')]],
            [[Button.inline('我使用的脚本就在仓库根目录下', data='root')], [Button.inline('请让我手动输入', data='input'), Button.inline('请帮我取消对话', data='cancel')]]
        ]
        replies = []
        nums = []
        async with jdbot.conversation(SENDER, timeout=180) as conv:
            for tip in tips:
                i = tips.index(tip)
                msg = await conv.send_message(tip)
                msg = await jdbot.edit_message(msg, tip, buttons=btns[i])
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消')
                    conv.cancel()
                    return
                elif res == 'input':
                    await jdbot.delete_messages(chat_id, msg)
                    msg = await conv.send_message(tips_2[i])
                    reply = await conv.get_response()
                    replies.append(reply.raw_text)
                    await jdbot.delete_messages(chat_id, msg)
                else:
                    await jdbot.delete_messages(chat_id, msg)
                    replies.append(res)
            conv.cancel()
        with open(_ConfigFile, 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        for config in configs:
            if config.find('启用其他开发者的仓库方式一') != -1:
                line = int(configs.index(config))
            elif config.find('OwnRepoUrl') != -1 and config.find('#') == -1:
                num = int(re.findall(r'(?<=OwnRepoUrl)[\d]+(?==")', config)[0])
                content_data = re.findall(r'(?<==")[\S]+(?=")', config)
                if content_data == []:
                    nums.append(num)
                    break
                else:
                    nums.append(num + 1)
        nums.sort()            
        OwnRepoUrl = f'OwnRepoUrl{nums[-1]}="{url}"'
        OwnRepoBranch = f'OwnRepoBranch{nums[-1]}="{replies[0].replace("root", "")}"'
        Path = replies[1].replace("root", "''")
        OwnRepoPath = f'OwnRepoPath{nums[-1]}="{Path}"'
        configs.insert(line + 1, f'\n{OwnRepoUrl}\n{OwnRepoBranch}\n{OwnRepoPath}\n')
        with open(_ConfigFile, 'w', encoding='utf-8') as f2:
            f2.write(''.join(configs))
        await jdbot.delete_messages(chat_id, start)
        await jdbot.send_file(chat_id, _ConfigFile, caption='你可以查阅上面这个文件')
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            btns2 = [
                [Button.inline(f'是的，请帮我拉取{short_url}这个仓库的脚本', data='jup')],
                [Button.inline('谢谢，但我暂时不需要', data='cancel')]
            ]
            msg = await jdbot.send_message(chat_id, '请问你需要拉取仓库里面的脚本吗？', buttons=btns2)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                msg = await jdbot.edit_message(msg, '配置完成，感谢你的使用')
            else:
                msg = await jdbot.edit_message(msg, '正在为你拉取仓库脚本，详情请查阅下一条通知')
                await cmd(res)
            conv.cancel()
    except exceptions.TimeoutError:
        msg = await jdbot.send_message(chat_id, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))

