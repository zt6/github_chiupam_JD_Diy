#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .. import chat_id, jdbot, logger, chname, mybot
from telethon import events
import os


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/restart$'))
async def myrestart(event):
    try:
        await jdbot.send_message(chat_id, "重启程序")
        cmdtext = "if [ -d '/jd' ]; then cd /jd/jbot; pm2 start ecosystem.config.js; cd /jd; pm2 restart jbot; else " \
                  "ps -ef | grep 'python3 -m jbot' | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null; " \
                  "nohup python3 -m jbot >/ql/log/bot/bot.log 2>&1 & fi "
        os.system(cmdtext)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


if chname:
    jdbot.add_event_handler(myrestart, events.NewMessage(from_users=chat_id, pattern=mybot['命令别名']['cron']))

