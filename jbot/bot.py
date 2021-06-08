#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-08 19:29
# @Version  : v 2.4
# @Updata   : 1. 下载 raw 链接后可以识别 cron 表达式并询问是否需要添加；2. 支持 v4-bot 用户在给 /checkcookie 屏蔽后的 cookie可以给面板扫码自动替换；3. 修改完配置后不发送配置文件
# @Future   :


from .. import chat_id, jdbot, _ConfigDir, _ScriptsDir, _OwnDir, _LogDir, logger, TOKEN, _JdbotDir
from ..bot.utils import cmd, press_event, backfile, jdcmd, _DiyDir, V4, QL, _ConfigFile
from telethon import events, Button
from asyncio import exceptions
import requests, re, os, asyncio


bot_id = int(TOKEN.split(':')[0])


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


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/start$'))
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
    /checkcookie 检测失效Cookie并把它屏蔽
    此外 1、发送已 raw 的链接会下载文件，并让用户做出选择（可能不支持青龙）
        2、发送仓库链接会开始添加仓库，用户按要求回复即可（不支持青龙）
        3、接受到 cookie 过期消息自动开启 /checkcookie 指令

    仓库：https://github.com/chiupam/JD_Diy.git
    欢迎🌟Star & 提出🙋[isuss](https://github.com/chiupam/JD_Diy/issues/new) & 请勿🚫Fork
    频道：[👬和东哥做兄弟](https://t.me/jd_diy_bot_channel) （不开放闲聊，仅讨论脚本）
"""
        await asyncio.sleep(0.5)
        await jdbot.send_message(chat_id, diy_hello)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/help$'))
async def myhelp(event):
    """
    获取自定义机器人的快捷命令
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


@jdbot.on(events.NewMessage(from_users=[chat_id, bot_id], pattern=r'^/checkcookie$|.*cookie已失效'))
async def mycheckcookie(event):
    """
    自动检测cookie的过期情况
    :param event:
    :return:
    """
    try:
        msg = await jdbot.send_message(chat_id, '正在检测 cookie 过期情况')
        check = checkCookie1()
        expireds = check[0]
        text, o = '检测结果\n\n', '\n\t   └ '
        edit = False
        if V4:
            web = '/jd/panel/server.js'
            if os.path.isfile(web):
                web = True
                with open(_ConfigFile, 'r', encoding='utf-8') as f1:
                    configs = f1.read()
                n = " ".join('%s' % expired for expired in expireds)
                configs = re.sub(r'TempBlockCookie=""', f'TempBlockCookie="{n}"', configs, re.M)
                text += f'【屏蔽情况】{o}TempBlockCookie="{n}"\n\n使用修改 TempBlockCookie 策略'
                edit = True
            else:
                web = False
                with open(_ConfigFile, 'r', encoding='utf-8') as f1:
                    configs = f1.readlines()
                if configs[-1] == '\n':
                    del (configs[-1])
                tip = '此账号的cookie已经失效'
                for expired in expireds:
                    for config in configs:
                        if config.find(f'Cookie{expired}') != -1 and config.find('# Cookie') == -1:
                            pt_pin = config.split(';')[-2].split('=')[-1]
                            configs[configs.index(config)] = f'Cookie{expired}="{pt_pin}{tip}"\n'
                            edit = True
                            text += f'【屏蔽情况】 {pt_pin}{o}临时替换第 {expired} 个用户的cookie\n'
                        elif config.find('第二区域') != -1:
                            break
        elif QL:
            web = False
            with open(_ConfigFile, 'r', encoding='utf-8') as f1:
                configs = f1.readlines()
            if configs[-1] == '\n':
                del (configs[-1])
            for expired in expireds:
                cookie = configs[int(expired) - 1]
                pt_pin = cookie.split(';')[-2]
                del (configs[int(expired) - 1])
                edit = True
                text += f'【删除情况】{pt_pin}{o}已经删除第 {expired} 个用户的Cookie\n'
        else:
            await jdbot.edit_message(msg, '未知环境的用户，无法使用 /checkcookie 指令')
            return
        if edit:
            if web:
                with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                    f2.write(configs)
            else:
                with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                    f2.write(''.join(configs))
            await jdbot.edit_message(msg, text)
        else:
            await jdbot.edit_message(msg, '配置无需改动，可用cookie中并没有cookie过期')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/restart$'))
async def myrestart(event):
    """
    发送 /restart 重启机器人
    :param event:
    :return:
    """
    try:
        await jdbot.send_message(chat_id, '准备重启机器人')
        os.system('pm2 restart jbot')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/upbot$'))
async def myupbot(event):
    """
    发送 /upbot 升级我的自定义机器人
    :param event:
    :return:
    """
    try:
        msg = await jdbot.send_message(chat_id, '开始下载最新的bot.py文件')
        furl = 'https://raw.githubusercontent.com/chiupam/JD_Diy/master/jbot/bot.py'
        resp = requests.get(f'http://ghproxy.com/{furl}').text
        if resp:
            path = f'{_JdbotDir}/diy/bot.py'
            backfile(path)
            with open(path, 'w+', encoding='utf-8') as f:
                f.write(resp)
            await jdbot.edit_message(msg, '准备重启机器人')
            os.system('pm2 restart jbot')
        else:
            await jdbot.edit_message(msg, "下载失败，请稍后重试")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://(raw)?.*(github|GitHub)?.*(js|py|sh)$'))
async def mydownload(event):
    """
    用户发送 raw 链接后自动下载链接文件
    :param event:
    :return:
    """
    try:
        SENDER = event.sender_id
        msg = await jdbot.send_message(chat_id, '开启下载文件会话')
        btn = [
            [Button.inline('我需要下载此链接文件，请继续', data='confirm')],
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
                cron = re.findall(r'(?<=cron\s").*(?=")', resp) # 截取 Loon 的 cron 表达式
                fname_cn = re.findall(r"(?<=new\sEnv\(').*(?=')", resp)
                if fname_cn != []:
                    fname_cn = fname_cn[0]
                else:
                    fname_cn = ''
                btn = [
                    [Button.inline('放入config目录', data=_ConfigDir),Button.inline('放入jbot/diy目录', data=f'{_JdbotDir}/diy')],
                    [Button.inline('放入own目录', data=_DiyDir), Button.inline('放入own并运行', data='run_own')],
                    [Button.inline('放入scripts目录', data=_ScriptsDir), Button.inline('放入scripts并运行', data='run_scripts')],
                    [Button.inline('请帮我取消对话', data='cancel')]
                ]
                if resp:
                    write = True
                    cmdtext = None
                    addcron = None
                    if cron != []:
                        addcron = cron[0]
                    msg = await conv.send_message(f'成功下载{fname_cn}脚本\n现在，请做出你的选择：')
                    msg = await jdbot.edit_message(msg, f'成功下载{fname_cn}脚本\n现在，请做出你的选择：', buttons=btn)
                    convdata = await conv.wait_event(press_event(SENDER))
                    res = bytes.decode(convdata.data)
                    if res == 'cancel':
                        write = False
                        msg = await jdbot.edit_message(msg, '对话已取消')
                    elif res == 'run_own':
                        path, cmdtext = f'{_DiyDir}/{fname}', f'{jdcmd} {_DiyDir}/{fname} now'
                        await jdbot.edit_message(msg, f'{fname_cn}脚本已保存到own文件夹，并成功在后台运行，请稍后自行查看日志')
                    elif res == 'run_scripts':
                        path, cmdtext = f'{_ScriptsDir}/{fname}', f'{jdcmd} {_ScriptsDir}/{fname} now'
                        await jdbot.edit_message(msg, f'{fname_cn}脚本已保存到scripts文件夹，并成功在后台运行，请稍后自行查看日志')
                    else:
                        path = f'{res}/{fname}'
                        await jdbot.edit_message(msg, f'{fname_cn}脚本已保存到{res}文件夹')
                    if addcron:
                        btn = [
                            [Button.inline('是的，请帮我添加定时任务', data='add')],
                            [Button.inline('谢谢，但我暂时不需要', data='cancel')],
                        ]
                        msg = await conv.send_message(f"这是我识别出来的 cron 表达式\n{addcron}\n请问需要把它添加进定时任务中吗？")
                        await jdbot.edit_message(msg, f"这是我识别出来的 cron 表达式\n{addcron}\n请问需要把它添加进定时任务中吗？", buttons=btn)
                        convdata = await conv.wait_event(press_event(SENDER))
                        res2 = bytes.decode(convdata.data)
                        if res2 == 'add':
                            cronfpath = f'{_ConfigDir}/crontab.list'
                            with open(cronfpath, 'a', encoding='utf-8') as f:
                                f.write(f'{addcron} mtask {path}\n')
                            await jdbot.edit_message(msg, '我已经把它添加进定时任务中了')
                        else:
                            await  jdbot.edit_message(msg, '那好吧，会话结束，感谢你的使用')
                    else:
                        msg = await conv.send_message(f"我无法识别到脚本内的 cron 表达式，请手动添加进定时任务中")
                        await jdbot.edit_message(msg, f"我无法识别到脚本内的 cron 表达式，请手动添加进定时任务中")
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
        msg = await jdbot.send_message(chat_id, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://github\.com/\S+'))
async def myaddrepo(event):
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
            f'正在设置 OwnRepoBranch 的值\n该值为你想使用脚本在[仓库]({url})的哪个分支', '正在设置 OwnRepoPath 的\n该值为你要使用的脚本在分支的哪个路径'
        ]
        tips_2 = [
            f'回复 main 代表使用 [{short_url}]({url}) 仓库的 "main" 分支\n回复 master 代表使用 [{short_url}]({url}) 仓库的 "master" 分支\n具体分支名称以你所发仓库实际为准\n',
            f'回复 scripts/jd normal 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 scripts/jd 和 normal文件夹下\n回复 root cron 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 根目录 和 cron 文件夹下\n具体目录路径以你所发仓库实际为准\n'
        ]
        btns = [
            [
                [Button.inline('我使用仓库的 "默认" 分支', data='root')],
                [Button.inline('我使用仓库的 "main" 分支', data='main'), Button.inline('我使用仓库的 "master" 分支', data='master')],
                [Button.inline('请让我手动输入', data='input'), Button.inline('请帮我取消对话', data='cancel')]
            ],
            [
                [Button.inline('我使用的脚本就在仓库根目录下', data='root')],
                [Button.inline('请让我手动输入', data='input'), Button.inline('请帮我取消对话', data='cancel')]
            ]
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

