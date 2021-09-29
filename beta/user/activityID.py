#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
import sys

from telethon import events

from .login import user
from .. import chat_id, jdbot, logger, TOKEN
from ..bot.utils import V4
from ..diy.utils import myzdjr_chatIds
from ..diy.utils import rwcon

bot_id = int(TOKEN.split(":")[0])


@user.on(events.NewMessage(chats=myzdjr_chatIds, pattern=r'export\s(jd_zdjr_activity|jd_joinTeam_activity|FAV).*=(".*"|\'.*\')'))
async def activityID(event):
    try:
        text = event.message.text
        if "jd_zdjr_activity" in text:
            activity , name = "jd_zdjr_activity", "组队瓜分1"
        elif "jd_joinTeam_activity" in text:
            activity, name = "jd_joinTeam_activity", "组队瓜分2"
        elif "FAV_SHOP" in text:
            activity, name = "FAV_SHOP", "关注有礼"
        else:
            return
        msg = await jdbot.send_message(chat_id, f'【监控】 监测到`{name}` 环境变量！')
        messages = event.message.text.split("\n")
        change = ""
        for message in messages:
            kv = message.replace("export ", "")
            key = kv.split("=")[0]
            value = re.findall(r'"([^"]*)"', kv)[0]
            if "jd_zdjr_activityId" in key and len(value) != 32:
                await jdbot.edit_message(msg, f"这不是去幼儿园的车🚗！\n\n`{kv}`")
                return
            configs = rwcon("list")
            if kv in configs:
                continue
            if key in configs:
                configs = re.sub(f'{key}=(\"|\').*(\"|\')', kv, configs)
                change += f"【替换】 `{name}` 环境变量成功\n`{kv}`\n\n"
                msg = await jdbot.edit_message(msg, change)
            else:
                if V4:
                    end_line = 0
                    configs = rwcon("list")
                    for config in configs:
                        if config.find("第五区域") != -1 and config.find("↑") != -1:
                            end_line = configs.index(config)
                            break
                    configs.insert(end_line - 2, f'export {key}="{value}"\n')
                else:
                    configs = rwcon("str")
                    configs += f'export {key}="{value}"\n'
                change += f"【新增】 `{name}` 环境变量成功\n`{kv}`\n\n"
                msg = await jdbot.edit_message(msg, change)
            rwcon(configs)
        if len(change) == 0:
            await jdbot.edit_message(msg, f"【取消】 `{name}` 环境变量无需改动！")
            return
        try:
            if "jd_zdjr_activity" in event.message.text:
                from ..diy.diy import smiek_jd_zdjr
                await smiek_jd_zdjr()
            elif "jd_joinTeam_activityId" in event.message.text:
                from ..diy.diy import jd_joinTeam_activityId
                await jd_joinTeam_activityId()
            elif "FAV_SHOP_ID" in event.message.text:
                from ..diy.diy import jd_fav_shop_gift
                await jd_fav_shop_gift()
        except ImportError:
            pass
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
