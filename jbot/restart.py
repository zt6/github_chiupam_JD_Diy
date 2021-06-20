#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam
# @Data     : 2021-06-20
# @Version  : v 1.0
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, logger
from ..bot.utils import  V4, QL
from telethon import events
import os


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/restart$'))
async def myrestart(event):
    try:
        await restart()
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


# 重启函数
async def restart():
    try:
        if V4:
            await jdbot.send_message(chat_id, "重启程序")
            os.system("pm2 restart jbot")
        elif QL:
            await jdbot.send_message(chat_id, "重启程序")
            os.system("ql bot")
        else:
            await jdbot.send_message(chat_id, "未知用户，自行重启机器人")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))