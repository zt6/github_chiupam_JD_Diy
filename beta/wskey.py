#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .. import chat_id, jdbot, logger, _ConfigDir
from ..bot.utils import V4, _Auth, press_event, split_list, row
from ..diy.utils import QL2, QL8, ql_token, wskey, read, write
from telethon import events, Button
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
        if V4 or QL2:
            file = f"{_ConfigDir}/wskey.list"
            configs = read("str")
            if not os.path.exists(file) and "wskey" not in configs:
                sender = event.sender_id
                async with jdbot.conversation(sender, timeout=120) as conv:
                    tip = "由于这是你第一次使用此功能，关于wskey的存储位置，请做出您的选择："
                    buttons = [
                        Button.inline("存储在config.sh中", data="config.sh"),
                        Button.inline("存储在wskey.list中", data="wskey.list"),
                        Button.inline('取消会话', data='cancel')
                    ]
                    msg = await jdbot.edit_message(msg, tip, buttons=split_list(buttons, row))
                    convdata = await conv.wait_event(press_event(sender))
                    res = bytes.decode(convdata.data)
                    if res == 'cancel':
                        await jdbot.edit_message(msg, '对话已取消')
                        return False
                    elif res == 'wskey.list':
                        os.system(f"touch {file}")
                    msg = await jdbot.edit_message(msg, f'你的选择是：存储在{res}中\n准备继续工作……')
            if os.path.exists(file):
                for message in messages:
                    ws = re.findall(r'(pin=.*)(wskey=[^;]*);*', message)[0]
                    pin, key = ws[0], ws[1]
                    message = pin + key
                    configs = wskey("str")
                    if pin in configs:
                        configs = re.sub(f"pin={pin};wskey=.*;", message, configs)
                        text += f"更新wskey成功！pin为：{pin}\n"
                    else:
                        configs += message + "\n"
                        text += f"新增wskey成功！pin为：{pin}\n"
                    wskey(configs)
            else:
                for message in messages:
                    ws = re.findall(r'(pin=.*)(wskey=[^;]*);*', message)[0]
                    pin, key = ws[0], ws[1]
                    message = pin + key
                    configs = read("str")
                    if pin + ";wskey" in configs:
                        configs = re.sub(f'pin={pin};wskey=.*;', message, configs)
                        text += f"更新wskey成功！pin为：{pin}\n"
                    elif V4:
                        configs = read("list")
                        for config in configs:
                            if pin in config and "wskey" not in config:
                                line = configs.index(config)
                                num = re.findall(r'(?<=[Cc]ookie)[\d]+(?==")', config)[0]
                                configs.insert(line, f'wskey{num}="{message}"\n')
                                text += f"新增wskey成功！pin为：{pin}\n"
                                break
                            elif "第二区域" in config:
                                await jdbot.edit_message(msg, "请使用标准模板！")
                                return
                    elif QL2:
                        configs = read("str")
                        configs += f"{message}\n"
                        text += f"新增wskey成功！pin为：{pin}\n"
                    await jdbot.edit_message(msg, text)
                    write(configs)
        elif QL8:
            token = ql_token(_Auth)
            for message in messages:
                ws = re.findall(r'(pin=.*)(wskey=[^;]*);*', message)[0]
                pin, key = ws[0], ws[1]
                message = pin + key
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
            else:
                token = ql_token(_Auth)
                url = 'http://127.0.0.1:5600/api/crons'
                headers = {'Authorization': f'Bearer {token}'}
                if QL8:
                    body = {'searchValue': "wskey_ptkey.py", 'Authorization': f'Bearer {token}'}
                else:
                    body = {'searchValue': "wskey_ptkey.py"}
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
