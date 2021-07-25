#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .. import chat_id, jdbot, logger, _JdbotDir, chname, mybot
from telethon import events
import os, sys


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/list$'))
async def mylist(event):
    try:
        lists = []
        mydiy = {
            "checkcookie.py": "检查账号过期",
            "tempblockcookie.py": "屏蔽账号",
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
        title = "【💥错误💥】"
        name = sys.argv[0].split("/")[-1].split(".")[0]
        function = sys._getframe().f_code.co_name
        await jdbot.send_message(chat_id, f"{title}\n\n文件名：{name}\n函数名：{function}\n错误原因：{str(e)}\n\n建议百度/谷歌查询")
        logger.error(f"错误--->{str(e)}")


if chname:
    jdbot.add_event_handler(mylist, events.NewMessage(from_users=chat_id, pattern=mybot['命令别名']['cron']))