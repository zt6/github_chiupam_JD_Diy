#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam
# @Data     : 2021-06-13
# @Version  : v 1.0
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, logger, TOKEN, _JdbotDir
from ..bot.utils import press_event, backfile, _DiyDir, V4, QL, cmd, _ConfigFile
from telethon import events, Button
from asyncio import exceptions
import requests, os, asyncio, re


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://github\.com/\S+git$'))
async def myaddrepo(event):
    try:
        if QL:
            await jdbot.send_message(chat_id, "此功能暂不支持青龙")
            return
        SENDER = event.sender_id
        url = event.raw_text
        short_url = url.split('/')[-1].replace(".git", "")
        tips = [f'正在设置 OwnRepoBranch 的值\n该值为你想使用脚本在[仓库]({url})的哪个分支', '正在设置 OwnRepoPath 的\n该值为你要使用的脚本在分支的哪个路径']
        tips_2 = [f'回复 main 代表使用 [{short_url}]({url}) 仓库的 "main" 分支\n回复 master 代表使用 [{short_url}]({url}) 仓库的 "master" 分支\n具体分支名称以你所发仓库实际为准\n',f'回复 scripts/jd normal 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 scripts/jd 和 normal文件夹下\n回复 root cron 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 根目录 和 cron 文件夹下\n具体目录路径以你所发仓库实际为准\n']
        btns = [
            [
                [Button.inline('我使用仓库的 "默认" 分支', data='root')],
                [Button.inline('我使用仓库的 "main" 分支', data='main'), Button.inline('我使用仓库的 "master" 分支', data='master')],
                [Button.inline('请让我手动输入', data='input'), Button.inline('请帮我取消对话', data='cancel')]
            ],
            [
                [Button.inline('我使用的脚本就在仓库根目录下', data='root')],
                [Button.inline('请让我手动输入', data='input'), Button.inline('请帮我取消对话', data='cancel')]
            ]
        ]
        replies, nums = [], []
        async with jdbot.conversation(SENDER, timeout=180) as conv:
            for tip in tips:
                i = tips.index(tip)
                msg = await conv.send_message(tip, buttons=btns[i])
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == 'input':
                    await jdbot.delete_messages(chat_id, msg)
                    msg = await conv.send_message(tips_2[i])
                    reply = await conv.get_response()
                    res = reply.raw_text
                    msg = await jdbot.edit_message(msg, f"你输入的值为：{res}")
                else:
                    msg = await jdbot.edit_message(msg, f"你设置的值为：{res}")
                replies.append(res)
            conv.cancel()
        with open(_ConfigFile, 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        for config in configs:
            if config.find('启用其他开发者的仓库方式一') != -1:
                line = int(configs.index(config))
            elif config.find('OwnRepoUrl') != -1 and config.find('#') == -1:
                num = int(re.findall(r'(?<=OwnRepoUrl)[\d]+(?==")', config)[0])
                content_data = re.findall(r'(?<==")[\S]+(?=")', config)
                if content_data == []:
                    nums.append(num)
                    break
                else:
                    nums.append(num + 1)
        nums.sort()
        OwnRepoUrl = f'OwnRepoUrl{nums[-1]}="{url}"'
        OwnRepoBranch = f'OwnRepoBranch{nums[-1]}="{replies[0].replace("root", "")}"'
        Path = replies[1].replace("root", "''")
        if Path == "''":
            OwnRepoPath = f'OwnRepoPath{nums[-1]}=""'
        else:
            OwnRepoPath = f'OwnRepoPath{nums[-1]}="{Path}"'
        configs.insert(line + 1, f'\n{OwnRepoUrl}\n{OwnRepoBranch}\n{OwnRepoPath}\n')
        with open(_ConfigFile, 'w', encoding='utf-8') as f2:
            f2.write(''.join(configs))
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            btns2 = [
                [Button.inline(f'是的，请帮我拉取{short_url}这个仓库的脚本', data='jup')],
                [Button.inline('谢谢，但我暂时不需要', data='cancel')]
            ]
            msg = await conv.send_message('请问你需要拉取仓库里面的脚本吗？', buttons=btns2)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                msg = await jdbot.edit_message(msg, '配置完成，感谢你的使用')
            else:
                msg = await jdbot.edit_message(msg, '正在为你拉取仓库脚本')
                await cmd(res)
            conv.cancel()
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
