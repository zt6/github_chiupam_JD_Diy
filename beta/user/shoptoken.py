#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
import sys

from telethon import events

from .login import user
from .. import chat_id, jdbot, logger, TOKEN
from ..bot.utils import V4, QL
from ..diy.utils import rwcon
from ..diy.utils import shoptokenIds

bot_id = int(TOKEN.split(":")[0])


@user.on(events.NewMessage(chats=shoptokenIds, pattern=r'(export\s)?MyShopToken\d*=(".*"|\'.*\')'))
async def myshoptoken(event):
    try:
        messages = event.message.text.split("\n")
        exports = re.findall(r'export MyShopToken(\d+)="(.*)"', rwcon("str"))
        change, line, number = "", 0, 1
        if not exports:
            msg = await jdbot.send_message(chat_id, '监控到店铺签到环境变量，直接添加！')
            configs = rwcon("str")
            for message in messages:
                value = re.findall(r'"([^"]*)"', message)[0]
                if V4:
                    configs = rwcon("list")
                    for config in configs:
                        if "第五区域" in config and "↑" in config:
                            line = configs.index(config)
                            break
                    change += f'export MyShopToken1="{value}"\n'
                    configs.insert(line - 2, f'export MyShopToken1="{value}"\n')
                elif QL:
                    change += f'export MyShopToken1="{value}"\n'
                    configs += f'export MyShopToken1="{value}"\n'
                rwcon(configs)
            await jdbot.edit_message(msg, f"【店铺签到领京豆】\n\n此次添加的变量\n{change}")
            return
        msg = await jdbot.send_message(chat_id, '监控到店铺签到环境变量，继续添加！')
        for message in messages:
            value = re.findall(r'"([^"]*)"', message)[0]
            configs = rwcon("str")
            if value in configs:
                continue
            configs = rwcon("list")
            for config in configs:
                if "export MyShopToken" in config:
                    number = int(re.findall(r'\d+', config.split("=")[0])[0]) + 1
                    line = configs.index(config) + 1
            change += f'export MyShopToken{number}="{value}"\n'
            configs.insert(line, f'export MyShopToken{number}="{value}"\n')
            rwcon(configs)
        if len(change) == 0:
            await jdbot.edit_message(msg, "目前配置中的环境变量无需改动")
            return
        await jdbot.edit_message(msg, f"【店铺签到领京豆】\n\n此次添加的变量\n{change}")
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
