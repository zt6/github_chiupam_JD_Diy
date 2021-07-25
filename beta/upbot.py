#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .. import chat_id, jdbot, logger, _JdDir, _JdbotDir, chname, mybot
from ..bot.utils import press_event, split_list, row
from telethon import events, Button
from asyncio import exceptions
import requests, os


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/upbot$'))
async def myupbot(event):
    try:
        msg = await jdbot.send_message(chat_id, "【前瞻计划】\n\n准备更新程序")
        SENDER = event.sender_id
        furl = "https://raw.githubusercontent.com/chiupam/JD_Diy/master/config/diybot_beta.sh"
        if '下载代理' in mybot.keys() and str(mybot['下载代理']).lower() != 'false' and 'github' in furl:
            furl = f'{str(mybot["下载代理"])}/{furl}'
        resp = requests.get(furl).text
        if not resp:
            await jdbot.edit_message(msg, "【前瞻计划】\n\n下载shell文件失败\n请稍后重试，或尝试关闭代理重启")
            return
        cmdtext = f"bash {_JdDir}/diybot.sh"
        if os.path.exists(f'{_JdbotDir}/diy/user.py'):
            btns = [
                Button.inline("更新", data="user"),
                Button.inline("不更新", data="no")
            ]
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                msg = await jdbot.edit_message(msg, "【前瞻计划】\n\n下载shell文件成功\n是否更新 user.py？（覆盖式更新）", buttons=split_list(btns, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == "user":
                    cmdtext = f"bash {_JdDir}/diybot.sh {res}"
                conv.cancel()
        fpath = f"{_JdDir}/diybot.sh"
        with open(fpath, 'w+', encoding='utf-8') as f:
            f.write(resp)
        await jdbot.edit_message(msg, "更新过程中程序会重启，请耐心等待")
        os.system(cmdtext)
    except exceptions.TimeoutError:
        await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


if chname:
    jdbot.add_event_handler(myupbot, events.NewMessage(from_users=chat_id, pattern=mybot['命令别名']['cron']))