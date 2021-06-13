#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam1
# @Data     : 2021-06-12
# @Version  : v 1.0
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, _ConfigDir, logger
from ..bot.utils import press_event
from telethon import events, Button
from asyncio import exceptions
import requests, re, os, asyncio


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'(export\s)?\w*=(".*"|\'.*\')'))
async def myaddexport(event):
    try:
        start = await jdbot.send_message(chat_id, '开始添加环境变量')
        SENDER = event.sender_id
        message = event.raw_text
        kv = message.replace("export ", "")
        kname = kv.split("=")[0]
        vname = re.findall(r"(\".*\"|'.*')", kv)[0][1:-1]
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            btns = [
                [Button.inline("是的，就是这样", data='yes')],
                [Button.inline("错了，取消对话重新设置", data='cancel')]
            ]
            msg = await conv.send_message(f"我检测到你需要添加一个环境变量\n键名：{kname}\n值名：{vname}\n请问是这样吗？", buttons=btns)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                await jdbot.delete_messages(chat_id, start)
                await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            else:
                await jdbot.delete_messages(chat_id, msg)
                msg = await conv.send_message(f"好的，请稍等\n你设置变量为：{kname}=\"{vname}\"")
            conv.cancel()
        with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
            configs = f1.read()
        await asyncio.sleep(1.5)
        await jdbot.delete_messages(chat_id, msg)
        if configs.find(kname) != -1:
            configs = re.sub(f'{kname}=(\"|\').*(\"|\')', f'{kname}="{vname}"', configs)
            end = "替换环境变量成功"
        else:
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                btns = [
                    [Button.inline("是的，我需要", data='yes')],
                    [Button.inline("谢谢，但我暂时不需要", data='cancel')]
                ]
                msg = await conv.send_message(f"这个环境变量是新增的，需要我给他添加注释嘛？", buttons=btns)
                convdata = await conv.wait_event(press_event(SENDER))
                await jdbot.delete_messages(chat_id, msg)
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await conv.send_message("那好吧，准备新增变量")
                    note = ''
                else:
                    msg = await conv.send_message("那请回复你所需要添加的注释")
                    note = await conv.get_response()
                    await jdbot.delete_messages(chat_id, msg)
                    note = f" # {note.raw_text}"
                conv.cancel()
            with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f3:
                configs = f3.readlines()
            for config in configs:
                if config.find("第五区域") != -1 and config.find("↑") != -1:
                    end_line = configs.index(config)
                    break
            configs.insert(end_line - 2, f'export {kname}="{vname}"{note}\n')
            await asyncio.sleep(1.5)
            await jdbot.delete_messages(chat_id, msg)
            end = "新增环境变量成功"
        with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f2:
            f2.write(''.join(configs))
        await jdbot.delete_messages(chat_id, start)
        await jdbot.send_message(chat_id, end)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
