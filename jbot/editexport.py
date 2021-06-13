#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam
# @Data     : 2021-06-13
# @Version  : v 1.0
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, _ConfigDir, logger
from ..bot.utils import press_event, V4, QL, split_list, row
from telethon import events, Button
from asyncio import exceptions
import requests, re, os, asyncio


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/export$'))
async def mychangeexport(event):
    try:
        SENDER = event.sender_id
        start = await jdbot.send_message(chat_id, "开始读取你额外的环境变量")
        with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        knames, vnames, notes, btns = [], [], [], []
        if V4:
            for config in configs:
                if config.find("第五区域") != -1 and config.find("↓") != -1:
                    start_line = configs.index(config) + 1
                elif config.find("第五区域") != -1 and config.find("↑") != -1:
                    end_line = configs.index(config)
            for config in configs[start_line:end_line]:
                if config.find("export") != -1 and config.find("##") == -1:
                    kv = config.replace("export ", "")
                    kname = kv.split("=")[0]
                    vname = re.findall(r"[^\"']+(?=\"|')", kv)[1]
                    if kv.find(" # ") != -1:
                        note = re.findall(r"(?<=#\s).*", kv)[0]
                    else:
                        note = 'none'
                    knames.append(kname), vnames.append(vname), notes.append(note)
                elif config.find("↓") != -1:
                    break
        elif QL:
            for config in configs:
                if config.find("export") != -1:
                    kv = config.replace("export ", "")
                    kname = kv.split("=")[0]
                    vname = re.findall(r"[^\"']+(?=\"|')", kv)[1]
                    if kv.find(" # ") != -1:
                        note = re.findall(r"(?<=#\s).*", kv)[0]
                    else:
                        note = 'none'
                    knames.append(kname), vnames.append(vname), notes.append(note)
        for i in range(len(knames)):
            if notes[i] != 'none':
                btn = Button.inline(notes[i], data=knames[i])
            else:
                btn = Button.inline(knames[i], data=knames[i])
            btns.append(btn)
        btns.append(Button.inline("帮我取消对话", data='cancel'))
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            msg = await conv.send_message("这是我查询到的环境变量名称\n请问你需要修改哪一个？", buttons=split_list(btns, row))
            convdata = await conv.wait_event(press_event(SENDER))
            await jdbot.delete_messages(chat_id, msg)
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                await jdbot.delete_messages(chat_id, msg)
                await jdbot.edit_message(start, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            kname = res
            msg = await conv.send_message("现在请回复你所需要设置的值")
            vname = await conv.get_response()
            vname = vname.raw_text
            await jdbot.delete_messages(chat_id, msg)
            btns = [
                [Button.inline("是的，就是这样", data='yes')],
                [Button.inline("错了，取消对话重新设置", data='cancel')]
            ]
            msg = await conv.send_message(f'好的，请稍等\n键名：{kname}\n值名：{vname}\n请问是这样吗？', buttons=btns)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                await jdbot.delete_messages(chat_id, start)
                await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            await jdbot.delete_messages(chat_id, msg)
            msg = await conv.send_message(f'好的，请稍等\n你设置变量为：{kname}="{vname}"')
            conv.cancel()
        with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
            configs = f2.read()
        configs = re.sub(f'{kname}=(\"|\')\S+(\"|\')', f'{kname}="{vname}"', configs)
        with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f3:
            f3.write(configs)
        await asyncio.sleep(1.5)
        await jdbot.delete_messages(chat_id, msg)
        await jdbot.delete_messages(chat_id, start)
        await jdbot.send_message(chat_id, "修改环境变量成功")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))