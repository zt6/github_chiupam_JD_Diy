#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam
# @Data     : 2021-06-13
# @Version  : v 1.0
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, _ConfigDir, _ScriptsDir, _OwnDir, logger
from ..bot.utils import cmd, press_event, backfile, jdcmd, V4, QL, _ConfigFile, mycron, split_list, row
from telethon import events, Button
from asyncio import exceptions
import requests, re, os, asyncio


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://(raw)?.*(js|py|sh)$'))
async def mydownload(event):
    try:
        SENDER = event.sender_id
        btn = [
            [Button.inline('我需要下载此链接文件，请继续', data='confirm')],
            [Button.inline('我不需要下载，请取消对话', data='cancel')]
        ]
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            msg = await conv.send_message('检测到你发送了一条链接，请做出你的选择：\n', buttons=btn)
            convdata = await conv.wait_event(press_event(SENDER))
            await jdbot.delete_messages(chat_id, msg)
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                await jdbot.send_message(chat_id, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            furl = event.raw_text
            speeds = ["http://ghproxy.com/", "https://mirror.ghproxy.com/", ""]
            for speed in speeds:
                resp = requests.get(f"{speed}{furl}").text
                if resp:
                    break
            if resp:
                fname = furl.split('/')[-1]
                fname_cn, cron = "", False
                if furl.endswith(".js"):
                    fname_cn, cron = re.findall(r"(?<=new\sEnv\(').*(?=')", resp, re.M), mycron(resp)
                btns = [
                    Button.inline('放入config目录', data=_ConfigDir),
                    Button.inline('放入jbot/diy目录', data=f'{_JdbotDir}/diy'),
                    Button.inline('放入scripts目录', data=_ScriptsDir),
                    Button.inline('放入own目录', data=_OwnDir ),
                    Button.inline('请帮我取消对话', data='cancel')
                ]
                write, cmdtext = True, False
                msg = await conv.send_message(f'成功下载{fname_cn}脚本\n现在，请做出你的选择：', buttons=split_list(btns, row))
                convdata = await conv.wait_event(press_event(SENDER))
                await jdbot.delete_messages(chat_id, msg)
                res1 = bytes.decode(convdata.data)
                if res1 == 'cancel':
                    await jdbot.send_message(chat_id, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res1 == _ScriptsDir:
                    fpath = f"{_ScriptsDir}/{fname}"
                    btns = [
                        [Button.inline("是", data="confirm")],
                        [Button.inline("否", data="cancel")]
                    ]
                    msg = await conv.send_message(f"请问需要运行{fname_cn}脚本吗？", buttons=btns)
                    convdata = await conv.wait_event(press_event(SENDER))
                    await jdbot.delete_messages(chat_id, msg)
                    res2 = bytes.decode(convdata.data)
                    if res2 == 'cancel':
                        await jdbot.send_message(chat_id, f'那好吧，文件将保存到{res1}目录')
                    else:
                        cmdtext = f'{jdcmd} {_ScriptsDir}/{fname} now'
                        await jdbot.send_message(chat_id, f"文件将保存到{res1}目录，并随后执行它")
                elif res1 == _OwnDir:
                    fpath = f"{_OwnDir}/raw/{fname}"
                    btns = [
                        [Button.inline("是", data="confirm")],
                        [Button.inline("否", data="cancel")]
                    ]
                    msg = await conv.send_message(f"请问需要运行{fname_cn}脚本吗？", buttons=btns)
                    convdata = await conv.wait_event(press_event(SENDER))
                    await jdbot.delete_messages(chat_id, msg)
                    res2 = bytes.decode(convdata.data)
                    if res2 == 'cancel':
                        await jdbot.send_message(chat_id, f'那好吧，文件将保存到{res1}目录')
                    else:
                        with open(f"{_ConfigDir}/corntab.list", 'r', encoding="utf-8") as f1:
                            crontabs = f1.readlines()
                        for crontab in crontabs:
                            if crontab.find("OwnRawFile") != -1 and crontab.find("#") == -1:
                                line = crontabs.index(crontab) + 1
                                break
                            elif crontab.find("第五区域") != -1:
                                break
                        crontabs.insert(line, f"\t{event.raw_text}")
                        with open(f"{_ConfigDir}/corntab.list", 'w', encoding="utf-8") as f2:
                            f2.write(''.join(crontabs))
                        cmdtext = f'{jdcmd} {_OwnDir}/{fname} now'
                        await jdbot.send_message(chat_id, f'文件将保存到{res1}目录，且已写入配置中，随后执行它')
                conv.cancel()
        backfile(path)
        with open(fpath, 'w+', encoding='utf-8') as f:
            f.write(resp)
        if cmdtext:
            await cmd(cmdtext)

















    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def addown(jdbot, conv, fname, fname_cn):
    None


async def addscripts(jdbot, conv, fname, fname_cn, cron):
    btns = [
        [Button.inline("好的，请帮我执行它", data="confirm")],
        [Button.inline("谢谢，但我暂时不需要", data="cancel")]
    ]
    msg = await conv.send_message(f"请问现在需要运行{fname_cn}脚本吗？", buttons=btns)
    convdata = await conv.wait_event(press_event(SENDER))
    await jdbot.delete_messages(chat_id, msg)
    res = bytes.decode(convdata.data)
    if res == "cancel":
        await conv.send_message(f'那好吧，文件已保存到{res}目录')
        conv