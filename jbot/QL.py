from .. import chat_id, jdbot, logger
from ..bot.utils import press_event, _DiyDir, V4, QL, cmd, _ConfigFile, split_list, row
from telethon import events, Button
from asyncio import exceptions
import requests, os, asyncio, re


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/ql$'))
async def ql(event):
    try:
        SENDER = event.sender_id
        url = event.raw_text
        url = "https://github.com/whyour/qinglong.git"
        short_url = url.split('/')[-1].replace(".git", "")
        btns_yn = [Button.inline("是", data="yes"), Button.inline("否", data="no")]
        if QL:
            tips_1 = [
                f'正在设置 branch 的值\n该值为你想使用脚本在[仓库]({url})的哪个分支',
                f'正在设置 path 的值\n该值为你要使用的脚本在分支的哪个路径，或要使用根目录下哪些名字开头的脚本（可用空格隔开）',
                f'正在设置 blacklist 的值\n该值为你不需要使用以哪些名字开头的脚本（可用空格隔开）',
                f'正在设置 dependence 的值\n该值为你想使用的依赖文件名称']
            tips_2 = [
                f'回复 main 代表使用 [{short_url}]({url}) 仓库的 "main" 分支\n回复 master 代表使用 [{short_url}]({url}) 仓库的 "master" 分支\n具体分支名称以你所发仓库实际为准\n',
                f'回复 scripts normal 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 scripts 和 normal文件夹下\n具体目录路径以你所发仓库实际为准\n',
                f'回复 jd_ jx_ 代表你不想使用开头为 jd_ 和 jx_ 的脚本\n具体文件名以你所发仓库实际、以你个人所需为准\n',
                f'回复你所需要安装依赖的文件全称\n具体文件名以你所发仓库实际、以你个人所需为准\n'
            ]
            tips_3 = [
                [Button.inline('"默认" 分支', data='root'), Button.inline('"main" 分支', data='main'),
                 Button.inline('"master" 分支', data='master'), Button.inline('手动输入', data='input'),
                 Button.inline('取消对话', data='cancel')],
                [Button.inline('仓库根目录', data='root'), Button.inline('手动输入', data='input'),
                 Button.inline('取消对话', data='cancel')],
                [Button.inline("不设置", data="root"), Button.inline('手动输入', data='input'),
                 Button.inline('取消对话', data='cancel')],
                [Button.inline("不设置", data="root"), Button.inline('手动输入', data='input'),
                 Button.inline('取消对话', data='cancel')]
            ]
            replies = []
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                for tip_1 in tips_1:
                    i = tips_1.index(tip_1)
                    msg = await conv.send_message(tip_1, buttons=split_list(tips_3[i], row))
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
                        msg = await jdbot.edit_message(msg, f"你输入的值为：{res.replace('root', '')}")
                    else:
                        msg = await jdbot.edit_message(msg, f"你设置的值为：{res.replace('root', '')}")
                    replies.append(res)
                    await asyncio.sleep(1)
                    await jdbot.delete_messages(chat_id, msg)
                conv.cancel()
            branch = replies[0]
            path = replies[1].replace(" ", "|")
            blacklist = replies[2].replace(" ", "|").replace("root", "")
            dependence = replies[3].replace("root", "")
            cmdtext = f'ql repo {url} {path} {blacklist} {dependence} {branch}'
            await jdbot.send_message(chat_id, str(cmdtext))
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
