from .. import chat_id, jdbot, logger, chname, mybot
from ..bot.utils import press_event, V4, QL, _ConfigFile, row, split_list, _Auth, myck
from telethon import events, Button
from asyncio import exceptions
import re, json, requests, time


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/tempblockcookie|^/blockcookie'))
async def mytempblockcookie(event):
    try:
        SENDER = event.sender_id
        message = event.message.raw_text
        ck_num = message.replace("/tempblockcookie","").replace("/blockcookie","")
        goon = True
        if len(ck_num) <= 1:
            async with jdbot.conversation(SENDER, timeout=120) as conv:
                while goon:
                    if V4:
                        goon = await V4_tempblockcookie(conv, SENDER)
                    else:
                        goon = await QL_tempblockcookie(conv, SENDER)
                conv.cancel()
        elif not ck_num.replace(" ","").isdigit():
            await jdbot.send_message(chat_id, "非法输入！参考下面所给实例进行操作！\n/tempblockcookie 1（屏蔽账号1）")
        elif ck_num.replace(" ","").isdigit():
            await tempblockcookie_3(ck_num.replace(" ",""))
    except exceptions.TimeoutError:
        await jdbot.send_message(chat_id, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def V4_tempblockcookie(conv, SENDER):
    msg = await conv.send_message("请做出您的选择")
    buttons = [
        Button.inline("查询目前屏蔽", data="inquire"),
        Button.inline("指定屏蔽账号", data="designated block"),
        Button.inline("指定取消屏蔽", data="designated unblock"),
        Button.inline("取消所有屏蔽", data="unblock all accounts"),
        Button.inline('取消会话', data='cancel')
    ]
    msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=split_list(buttons, row))
    convdata = await conv.wait_event(press_event(SENDER))
    res = bytes.decode(convdata.data)
    if res == 'cancel':
        await jdbot.edit_message(msg, '对话已取消')
        conv.cancel()
        return False
    else:
        with open(_ConfigFile, 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        for config in configs:
            if "TempBlockCookie" in config and " TempBlockCookie" not in config and "举例" not in config:
                line = configs.index(config)
                blocks = re.findall(r'"([^"]*)"', config)[0]
                if len(blocks) == 0:
                    blocks = []
                elif " " in blocks:
                    blocks = list(map(int, blocks.split(" ")))
                else:
                    blocks = [int(blocks)]
                break
            elif "AutoDelCron" in config:
                await jdbot.edit_message(msg, "无法找到 TempBlockCookie 目标字符串，请检查是否使用了标准配置模板")
                return False
        if res == 'inquire':
            message = f"目前的屏蔽情况是：\n{str(' '.join('%s' % _ for _ in sorted(blocks, reverse=False))) if len(blocks) != 0 else '没有帐号被屏蔽'}"
            return await operate(conv, SENDER, msg, message)
        elif res == 'designated block':
            acounts = len(myck(_ConfigFile))
            if acounts == len(blocks):
                message = "所有账号都已被屏蔽，无需继续屏蔽"
                return await operate(conv, SENDER, msg, message)
            cks, btns = [], []
            for i in range(acounts):
                cks.append(i + 1)
            btns_list = list(set(cks) - set(blocks))
            btns_list.sort()
            for block in btns_list:
                btn = Button.inline(f"账号{str(block)}", data=block)
                btns.append(btn)
            btns.append(Button.inline("上级菜单", data="upper menu"))
            btns.append(Button.inline('取消会话', data='cancel'))
            msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=split_list(btns, row))
            convdata = await conv.wait_event(press_event(SENDER))
            res_2 = bytes.decode(convdata.data)
            if res_2 == 'upper menu':
                await jdbot.delete_messages(chat_id, msg)
                return True
            elif res_2 == 'cancel':
                await jdbot.edit_message(msg, '对话已取消')
                return False
            else:
                blocks.append(int(res_2))
                blocks = " ".join('%s' % _ for _ in sorted(blocks, reverse=False))
                configs[line] = f'TempBlockCookie="{blocks}"\n'
                with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                    f2.write(''.join(configs))
                message = f"指定屏蔽账号{str(res_2)}成功"
                return await operate(conv, SENDER, msg, message)
        elif res == 'designated unblock':
            if blocks == []:
                message = "没有账号被屏蔽，无需取消屏蔽"
                return await operate(conv, SENDER, msg, message)
            btns = []
            for block in blocks:
                btn = Button.inline(f"账号{str(block)}", data=block)
                btns.append(btn)
            btns.append(Button.inline("上级菜单", data="upper menu"))
            btns.append(Button.inline('取消会话', data='cancel'))
            msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=split_list(btns, row))
            convdata = await conv.wait_event(press_event(SENDER))
            res_2 = bytes.decode(convdata.data)
            if res_2 == 'upper menu':
                await jdbot.delete_messages(chat_id, msg)
                return True
            elif res_2 == 'cancel':
                await jdbot.edit_message(msg, '对话已取消')
                return False
            else:
                blocks.remove(int(res_2))
                blocks = " ".join('%s' % _ for _ in sorted(blocks, reverse=False))
                configs[line] = f'TempBlockCookie="{blocks}"\n'
                with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                    f2.write(''.join(configs))
                message = f"指定取消屏蔽账号{res_2}成功"
                return await operate(conv, SENDER, msg, message)
        elif res == 'unblock all accounts':
            configs[line] = 'TempBlockCookie=""\n'
            with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                f2.write(''.join(configs))
            message = "取消屏蔽所有账号成功"
            return await operate(conv, SENDER, msg, message)


async def QL_tempblockcookie(conv, SENDER):
    msg = await conv.send_message("请做出您的选择")
    buttons = [
        Button.inline("查询启停状态", data="query start and stop status"),
        Button.inline("指定启用账号", data="specify to able an account"),
        Button.inline("指定禁用账号", data="specify to disable an account"),
        Button.inline("启用全部账号", data="enable all accounts"),
        Button.inline("禁用全部账号", data="disable all accounts"),
        Button.inline('取消会话', data='cancel')
    ]
    msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=split_list(buttons, row))
    convdata = await conv.wait_event(press_event(SENDER))
    res = bytes.decode(convdata.data)
    if res == 'cancel':
        await jdbot.edit_message(msg, '对话已取消')
        conv.cancel()
        return False
    else:
        with open(_Auth, 'r', encoding='utf-8') as f:
            auth = json.load(f)
        token = auth['token']
        headers = {'Authorization': f'Bearer {token}'}
        cookiedatas = []
        try:
            ql_version = '2.2'
            url = 'http://127.0.0.1:5600/api/cookies'
            body = {'t': int(round(time.time() * 1000))}
            datas = requests.get(url, params=body, headers=headers).json()['data']
            for data in datas:
                cknum = datas.index(data) + 1
                cookie = data['value']
                remarks = data['nickname']
                status = data['status']
                _id = data['_id']
                cookiedatas.append([cknum, cookie, remarks, status, _id])
        except:
            ql_version = '2.8+'
            url = 'http://127.0.0.1:5600/api/envs'
            body = {
                'searchValue': 'JD_COOKIE',
                'Authorization': f'Bearer {token}'
            }
            datas = requests.get(url, params=body, headers=headers).json()['data']
            for data in datas:
                cookiedatas.append([datas.index(data) + 1, data['value'], data['remarks'] if 'remarks' in data.keys() else "未备注", '启用' if data['status'] == 1 else '禁用', data['_id']])
        if res == 'query start and stop status':
            message = "目前启停状态\n\n"
            for cookiedata in cookiedatas:
                message += f'账号{cookiedata[0]}\n备注：{cookiedata[2]}\n启停状态：{cookiedata[3]}\n\n'
            return await operate(conv, SENDER, msg, message)
        elif res == 'specify to able an account':
            None




async def operate(conv, SENDER, msg, message):
    buttons = [
        Button.inline("上级菜单", data="upper menu"),
        Button.inline('取消会话', data='cancel')
    ]
    msg = await jdbot.edit_message(msg, message, buttons=split_list(buttons, row))
    convdata = await conv.wait_event(press_event(SENDER))
    res = bytes.decode(convdata.data)
    if res == 'upper menu':
        await jdbot.delete_messages(chat_id, msg)
        return True
    else:
        await jdbot.edit_message(msg, '对话已取消')
        return False


async def tempblockcookie_3(ck_num):
    msg = await jdbot.send_message(chat_id, f"开始屏蔽账号{ck_num}")
    with open(_ConfigFile, 'r', encoding='utf-8') as f1:
        configs = f1.readlines()
    for config in configs:
        i = configs.index(config)
        if config.find("TempBlockCookie") != -1 and config.find("##") == -1 and configs[i + 1].find(";") == -1:
            Temp = re.findall(r'"([^"]*)"', config)[0]
            if ck_num in Temp:
                await jdbot.edit_message(msg, "此账号已经被屏蔽，无需再次屏蔽")
            else:
                configs[i] = f'TempBlockCookie="{Temp} {ck_num}"\n'
                with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                    f2.write(''.join(configs))
                await jdbot.edit_message(msg, f"指定屏蔽账号{ck_num}成功")


if chname:
    jdbot.add_event_handler(mytempblockcookie, events.NewMessage(from_users=chat_id, pattern=mybot['命令别名']['cron']))