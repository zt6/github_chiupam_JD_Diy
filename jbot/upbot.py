#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam
# @Data     : 2021-06-13
# @Version  : v 1.0
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, logger, _JdbotDir
from ..bot.utils import press_event, V4, QL, split_list, row, backfile
from telethon import events, Button
from asyncio import exceptions
import requests, re, os, asyncio


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/upbot$'))
async def myupbot(event):
    try:
        SENDER = event.sender_id
        start = await jdbot.send_message(chat_id, '开始更新机器人文件')
        furl_startswith = "https://raw.githubusercontent.com/chiupam/JD_Diy/master/jbot/"
        mydiy = {
            "bot.py": "更新机器人文件",
            "checkcookie.py": "检查账号过期",
            "upbot.py": "升级机器人",
            "download.py": "下载文件",
            "addrepo.py": "添加仓库",
            "addexport.py": "添加环境变量",
            "editexport.py": "修改环境变量",
        }
        btns = []
        dirs = os.listdir(f"{_JdbotDir}/diy")
        for dir in dirs:
            if dir in mydiy:
                btns.append(Button.inline(mydiy[f'{dir}'], data=dir))
        btns.append(Button.inline("帮我取消对话", data='cancel'))
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            msg = await conv.send_message("请问你需要更新什么功能的机器人文件？", buttons=split_list(btns, row))
            convdata = await conv.wait_event(press_event(SENDER))
            await jdbot.delete_messages(chat_id, msg)
            fname = bytes.decode(convdata.data)
            if fname == 'cancel':
                await jdbot.edit_message(start, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            conv.cancel()
        msg = await jdbot.send_message(chat_id, "开始下载文件")
        speeds, botresp = ["http://ghproxy.com/", "https://mirror.ghproxy.com/", ""], False
        for speed in speeds:
            resp = requests.get(f"{speed}{furl_startswith}{fname}").text
            if "#!/usr/bin/env python3" in resp:
                botresp = resp
                break
        if botresp:
            await jdbot.delete_messages(chat_id, msg)
            path = f"{_JdbotDir}/diy/{fname}"
            backfile(path)
            with open(path, 'w+', encoding='utf-8') as f:
                f.write(resp)
            await restart()
        else:
            await jdbot.delete_messages(chat_id, start)
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, "下载失败，请自行拉取文件进/jbot/diy目录")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


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
