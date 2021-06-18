#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam
# @Data     : 2021-06-13
# @Version  : v 1.0
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, logger, TOKEN, _JdbotDir, _ConfigDir
from ..bot.utils import press_event, backfile, _DiyDir, V4, QL, split_list, row, mybot
from telethon import events, Button
from asyncio import exceptions
import requests, os, asyncio


bot_id = int(TOKEN.split(':')[0])


if not os.path.isfile(f"{_ConfigDir}/diybotset.json"):
    os.system(f'cd {_ConfigDir} && wget https://raw.githubusercontent.com/chiupam/JD_Diy/master/config/diybotset.json')


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/start$'))
async def myhello(event):
    try:
        hello = [
            "自定义机器人使用方法如下：",
            "\t/start 开始使用此机器人",
            "\t/restart 重启机器人",
            "\t/install 扩展此机器人功能",
            "\t/uninstall 删除此机器人功能",
            "\t/list 列出已拓展的功能"
        ]
        if os.path.isfile(f"{_JdbotDir}/diy/checkcookie.py"):
            hello.append("\t/checkcookie 检查cookie过期情况")
        if os.path.isfile(f"{_JdbotDir}/diy/addrepo.py"):
            hello.append("发送以 .git 结尾的链接开始添加仓库")
        if os.path.isfile(f"{_JdbotDir}/diy/download.py"):
            hello.append("发送以 .js .sh .py结尾的已raw链接开始下载文件")
        if os.path.isfile(f"{_JdbotDir}/diy/addexport.py"):
            hello.append("发送格式为 key=\"value\" 或者 key='value' 的消息开始添加环境变量")
        hello.append("\n频道：[👬和东哥做兄弟](https://t.me/JD_Diy_Channel)")
        await asyncio.sleep(0.5)
        await jdbot.send_message(chat_id, str('\n'.join(hello)))
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/help$'))
async def myhelp(event):
    try:
        diy_help = [
            "restart - 重启机器人",
            "install - 扩展此机器人功能",
            "uninstall - 删除此机器人功能",
            "list - 列出已拓展的功能"
        ]
        if os.path.isfile(f"{_JdbotDir}/diy/checkcookie.py"):
            diy_help.append("checkcookie - 检查cookie过期情况")
        if os.path.isfile(f"{_JdbotDir}/diy/addexport.py"):
            diy_help.append("export - 修改环境变量")
        await asyncio.sleep(0.5)
        await jdbot.send_message(chat_id, str('\n'.join(diy_help)))
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/restart$'))
async def myrestart(event):
    try:
        await restart()
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/install'))
async def myinstall(event):
    try:
        SENDER = event.sender_id
        furl_startswith = "https://raw.githubusercontent.com/chiupam/JD_Diy/master/jbot/"
        btns = [
            Button.inline("升级机器人", data="upbot.py"),
            Button.inline("检查账号过期", data="checkcookie.py"),
            Button.inline("下载文件", data="download.py"),
            Button.inline("添加仓库", data="addrepo.py"),
            Button.inline("添加环境变量", data="addexport.py"),
            Button.inline("修改环境变量", data="editexport.py"),
            Button.inline("我全都要", data="All"),
            Button.inline("帮我取消对话", data='cancel')
        ]
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            msg = await conv.send_message("请问你需要拓展什么功能？", buttons=split_list(btns, row))
            convdata = await conv.wait_event(press_event(SENDER))
            fname = bytes.decode(convdata.data)
            All = False
            if fname == 'cancel':
                await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            elif fname == 'All':
                All = True
            conv.cancel()
        if All:
            dltasks = ["upbot.py", "checkcookie.py", "download.py", "addrepo.py", "addexport.py", "editexport.py"]
        else:
            dltasks = [fname]
        msg = await jdbot.edit_message(msg, "开始下载文件")
        text = ''
        for dltask in dltasks:
            furl = f"{furl_startswith}{dltask}"
            if '下载代理' in mybot.keys() and str(mybot['下载代理']).lower() != 'false':
                furl = f'{str(mybot["下载代理"])}/{furl}'
            try:
                resp = requests.get(furl).text
                text += f"下载{dltask}成功\n"
                botresp = True
            except Exception as e:
                text += f"下载{dltask}失败，请自行拉取文件进/jbot/diy目录\n尝试 /set 更换下载代理"
                botresp = False
            if botresp:
                path = f"{_JdbotDir}/diy/{dltask}"
                backfile(path)
                with open(path, 'w+', encoding='utf-8') as f:
                    f.write(resp)
        await jdbot.edit_message(msg, text)
        await restart()
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/uninstall'))
async def myuninstall(event):
    try:
        SENDER = event.sender_id
        mydiy = {
            "checkcookie.py": "检查账号过期",
            "upbot.py": "升级机器人",
            "download.py": "下载文件",
            "addrepo.py": "添加仓库",
            "addexport.py": "添加环境变量",
            "editexport.py": "修改环境变量",
            "user.py": "user.py"
        }
        btns = []
        dirs = os.listdir(f"{_JdbotDir}/diy")
        for dir in dirs:
            if dir in mydiy:
                btns.append(Button.inline(mydiy[f'{dir}'], data=dir))
        btns.append(Button.inline("帮我取消对话", data='cancel'))
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            msg = await conv.send_message("请问你需要删除哪个功能？", buttons=split_list(btns, row))
            convdata = await conv.wait_event(press_event(SENDER))
            fname = bytes.decode(convdata.data)
            if fname == 'cancel':
                await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            conv.cancel()
        fpath = f"{_JdbotDir}/diy/{fname}"
        msg = await jdbot.edit_message(msg, "开始删除机器人功能")
        os.system(f'rm -rf {fpath}')
        await asyncio.sleep(1.5)
        if not os.path.isfile(fpath):
            await jdbot.edit_message(msg, "删除成功")
        else:
            await jdbot.edit_message(msg, f"删除失败，请手动删除{fpath}文件")
        await restart()
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/list'))
async def mylist(event):
    try:
        lists = []
        mydiy = {
            "checkcookie.py": "检查账号过期",
            "upbot.py": "升级机器人",
            "download.py": "下载文件",
            "addrepo.py": "添加仓库",
            "addexport.py": "添加环境变量",
            "editexport.py": "修改环境变量",
            "user.py": "user.py"
        }
        dirs = os.listdir(f"{_JdbotDir}/diy")
        for dir in dirs:
            if dir in mydiy:
                lists.append(mydiy[f'{dir}'])
        lists = '\n'.join(lists)
        await jdbot.send_message(chat_id, f"目前你拓展的功能有：\n\n{lists}")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/beta$'))
async def mydiyset(event):
    try:
        SENDER = event.sender_id
        btns = [
            Button.inline("内测功能1", data="install_getcookie.py"),
            Button.inline("内测功能2", data="install_web.py"),
            Button.inline("取消对话", data='cancel')
        ]
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            msg = await conv.send_message("请做出你的选择", buttons=split_list(btns, row))
            convdata = await conv.wait_event(press_event(SENDER))
            fname = bytes.decode(convdata.data)
            if fname == 'cancel':
                await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            conv.cancel()
            await jdbot.edit_message(msg, "正在安装内测功能")
            cmdtext = f"python {_JdbotDir}/diy/{fname}"
            os.system(cmdtext)
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


# 重启函数
async def restart():
    try:
        if V4:
            await jdbot.send_message(chat_id, "v4用户，准备重启机器人")
            os.system("pm2 restart jbot")
        elif QL:
            await jdbot.send_message(chat_id, "青龙用户，准备重启机器人")
            os.system("ql bot")
        else:
            await jdbot.send_message(chat_id, "未知用户，自行重启机器人")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


# 修改原作者的 cronup() 函数便于我继续进行此功能的编写
async def mycronup(jdbot, conv, resp, filename, msg, SENDER, markup, path):
    try:
        cron = mycron(resp)
        msg = await jdbot.edit_message(msg, f"这是我识别的定时\n```{cron}```\n请问是否需要修改？", buttons=markup)
    except:
        msg = await jdbot.edit_message(msg, f"我无法识别定时，将使用默认定时\n```0 0 * * *```\n请问是否需要修改？", buttons=markup)
    convdata3 = await conv.wait_event(press_event(SENDER))
    res3 = bytes.decode(convdata3.data)
    if res3 == 'confirm':
        await jdbot.delete_messages(chat_id, msg)
        msg = await conv.send_message("请回复你需要设置的 cron 表达式，例如：0 0 * * *")
        cron = await conv.get_response()
        cron = cron.raw_text
        msg = await jdbot.edit_message(msg, f"好的，你将使用这个定时\n```{cron}```")
        await asyncio.sleep(1.5)
    await jdbot.delete_messages(chat_id, msg)
    if QL:
        crondata = {"name":f'{filename.split(".")[0]}',"command":f'task {path}/{filename}',"schedule":f'{cron}'}
        with open(_Auth, 'r', encoding='utf-8') as f:
                auth = json.load(f)
        qlcron('add', crondata, auth['token'])
    else:
        upcron(f'{cron} mtask {path}/{filename}')
    await jdbot.send_message(chat_id, '添加定时任务成功')


# 升级 user.py 的函数
async def upuser(fname, msg):
    try:
        furl_startswith = "https://raw.githubusercontent.com/chiupam/JD_Diy/master/jbot/"
        speeds = ["http://ghproxy.com/", "https://mirror.ghproxy.com/", ""]
        msg = await jdbot.edit_message(msg, "开始下载文件")
        for speed in speeds:
            resp = requests.get(f"{speed}{furl_startswith}{fname}").text
            if "#!/usr/bin/env python3" in resp:
                break
        if resp:
            msg = await jdbot.edit_message(msg, f"下载{fname}成功")
            path = f"{_JdbotDir}/diy/user.py"
            backfile(path)
            with open(path, 'w+', encoding='utf-8') as f:
                f.write(resp)
            await restart()
        else:
            await jdbot.edit_message(msg, f"下载{fname}失败，请自行拉取文件进/jbot/diy目录")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))

