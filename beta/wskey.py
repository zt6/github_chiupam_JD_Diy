#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .. import chat_id, jdbot, logger, _ConfigDir
from ..bot.utils import V4, _Auth
from ..diy.utils import QL2, QL8, ql_token, wskey
from telethon import events
from requests import get, put, post
import re
import os
import sys


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'.*wskey.*'))
async def myaddwskey(event):
    try:
        text = ""
        msg = await jdbot.send_message(chat_id, "获取到wskey，正在工作中……")
        messages = event.raw_text.split("\n")
        if V4:
            file = f"{_ConfigDir}/wskey.list"
            if not os.path.exists(file):
                os.system(f"touch {file}")
            for message in messages:
                pin = message.split(";")[0].split("=")[1]
                configs = wskey("str")
                if pin in configs:
                    configs = re.sub(f"pin={pin};wskey=.*;", message, configs)
                    text += f"更新wskey成功！pin为：{pin}\n"
                else:
                    configs += message + "\n"
                    text += f"新增wskey成功！pin为：{pin}\n"
                wskey(configs)
        elif QL8:
            token = ql_token(_Auth)
            for message in messages:
                pin = message.split(";")[0].split('=')[1]
                url = 'http://127.0.0.1:5600/api/envs'
                headers = {'Authorization': f'Bearer {token}'}
                body = {
                    'searchValue': pin + ";wskey",
                    'Authorization': f'Bearer {token}'
                }
                data = get(url, params=body, headers=headers).json()['data']
                if data:
                    body = {"name": "JD_WSCK", "value": message, "_id": data[0]['_id']}
                    put(url, json=body, headers=headers)
                    text += f"更新wskey成功！pin为：{pin}\n"
                else:
                    body = [{"value": message, "name": "JD_WSCK"}]
                    post(url, json=body, headers=headers)
                    text += f"新增wskey成功！pin为：{pin}\n"
                await jdbot.edit_message(msg, text)
        elif QL2:
            text = "青龙2.2无法使用此功能~"
            await jdbot.edit_message(msg, text)
            return
        if len(text) > 1:
            if V4:
                if os.path.exists("/jd/own/wskey_ptkey.py"):
                    text += "\n将自动更新cookie列表，自行查看更新情况"
                    os.system("python /jd/own/wskey_ptkey.py")
                elif os.path.exists("/jd/scripts/wskey_ptkey.py"):
                    text += "\n将自动更新cookie列表，自行查看更新情况"
                    os.system("python /jd/scripts/wskey_ptkey.py")
                if "更新" in text:
                    await jdbot.edit_message(msg, text)
                else:
                    text += "\n不存在wskey_ptkey.py，无法自动更新cookie列表，自行解决更新问题"
                    await jdbot.edit_message(msg, text)
            elif QL8:
                url = 'http://127.0.0.1:5600/api/crons'
                headers = {'Authorization': f'Bearer {token}'}
                body = {
                    'searchValue': "wskey_ptkey.py",
                    'Authorization': f'Bearer {token}'
                }
                data = get(url, params=body, headers=headers).json()['data']
                if data:
                    url = 'http://127.0.0.1:5600/api/crons/run'
                    body = [data[0]['_id']]
                    put(url, headers=headers, json=body)
                    text += "\n将自动更新cookie列表，自行查看更新情况"
                if "更新" in text:
                    await jdbot.edit_message(msg, text)
                else:
                    text += "\n不存在wskey_ptkey.py，无法自动更新cookie列表，自行解决更新问题"
                    await jdbot.edit_message(msg, text)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
