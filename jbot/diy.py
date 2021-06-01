#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-01 16:20
# @Version  : v1.5
# @Updata   : 1. 修改了 getBwan() 函数；
# @Future   : 1. Null


# --------------------------------------------------------------------------------------- #
# 声明：
#     此脚本是根据布道场群文件 shopbean.py(v1.1) 改写的，并非完全自创
# 已有功能：
#     1. 解析 GET 请求后的包，以及其推送到 Telegram Bot 的消息会更加美观
#     2. 同时监控龙王庙频道，截取RRA，配合 redrain.py 定时使用（但 redrain.py 正在测试，因此未启用）
#     3. 给机器人发送 /checkcookie 命令即可临时屏蔽所有失效 cookie
# 使用方法：（直链: https://t.me/monk_dust_channel/692）
#     1. 存储路径：/jd/jbot/diy/（如果没有需要重新映射此文件夹）
#     2. 进入容器：docker exec -it jd bash
#     3. 停机器人：pm2 stop jbot
#     4. 开机器人：python3 -m jbot
#     5. 登陆后按 Ctrl + C 退出前台
#     6. 后台启动：pm2 start jbot
# 报错处理：（直链：https://t.me/monk_dust_channel/714）
#     一、 机器人交互没有反应，或者测试没有反应
#         1. docker exec -it jd bash
#         2. rm shopbean.session
#         3. pm2 stop jbot
#         4. python -m jbot
#         5. 登陆后按 Ctrl + C 退出前台
#         6. pm2 start jbot
# --------------------------------------------------------------------------------------- #


from .. import chat_id, api_hash, api_id, proxystart, proxy, jdbot, _LogDir, _ConfigDir
from ..bot.utils import cookies
from telethon import events, TelegramClient
import requests, re


# 判断用户是否启用代理功能
if proxystart: # 判断成立，即启用了代理功能
    client = TelegramClient("shopbean", api_id, api_hash, proxy=proxy, connection_retries=None).start() # 使用代理开始登录 Telegram
else: # 判断不成立，即未启用代理功能
    client = TelegramClient("shopbean", api_id, api_hash, connection_retries=None).start() # 使用直连登录 Telegram


# 监控布道场频道，检测到关键事件的触发时执行的函数
def getbean(i, cookie, url):
    """
    发起 GET 请求
    :param i: 账号
    :param cookie: 传入Cookie
    :param url: 传入 GET 所需的 url
    :return: 返回推送的消息主体
    """
    headers = { # 请求头
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Cookie": cookie, # cookie
    }
    result, o = '', '\n\t\t└' # 定义一些变量
    try: # 开始尝试执行下列代码
        r = requests.get(url=url, headers=headers) # 发起 GET 网络请求
        r.encoding = r.apparent_encoding # 更换编码
        res = r.json() # 使用 json 解析 GET 后的数据包
        # 判断 cookie 是否过期
        if res['code'] == '0': # cookie 未过期
            followDesc = res['result']['followDesc'] # 截取 followDesc 的值
            if followDesc.find('成功') != -1: # 成功获取奖励
                try:
                    for n in range(len(res['result']['alreadyReceivedGifts'])):
                        redWord = res['result']['alreadyReceivedGifts'][n]['redWord']
                        rearWord = res['result']['alreadyReceivedGifts'][n]['rearWord']
                        result += f"{o}领取成功，获得{redWord}{rearWord}"
                except:
                    giftsToast = res['result']['giftsToast'].split(' \n ')[1]
                    result = f"{o}{giftsToast}"
            elif followDesc.find('已经') != -1: # 已经获取过奖励
                result = f"{o}{followDesc}"
        else: # cookie 已过期或请求头缺少某些键值对
            result = f"{0}账号 Cookie 可能已经过期……"
    except Exception as e: # 如果 try 中发生任何错误
        result = f"{o}访问发生错误：{e}\n返回的包：{r.text}"
    return f"\n京东账号{i}{result}\n" # 执行函数后输出的内容


# 检查 cookie 是否过期的第一个函数
def checkCookie1():
    """
    检测 Cookie 是否过期
    :return: 返回过期的 Cookie 的账号数字列表
    """
    expired = [] # 首先定义一个空列表，名为 expired 列表
    for cookie in cookies: # 从 cookies 列表中轮询 cookie
        # 判断 cookie 是否过期
        if checkCookie2(cookie): # 过期了
            expired.append(cookies.index(cookie) + 1) # 把过期的第x个账号添加进 expired 列表中
    return expired # 执行函数后输出 expired 列表


# 检查 cookie 是否过期的第二个函数
def checkCookie2(cookie):
    """
    检测 Cookie 是否过期
    :param cookiex: 传入 Cookie
    :return: 返回是否过期
    """
    url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion" # 定义 GET 的链接
    headers = { # 请求头
        "Host": "me-api.jd.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": cookie, # 传入 cookie 的值
        "User-Agent": "jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
        "Accept-Language": "zh-cn",
        "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try: # 开始尝试执行下列代码
        r = requests.get(url, headers=headers) # 发起 GET 网络请求
        if r.ok: # 状态码为 200
            res = r.json() # 解析 GET 后返回的数据包
            if res['retcode'] == '1001': # 如果 retcode 的值为 1001 则视为 cookie 过期
                return True # 执行函数后输出真
            else: # 如果 retcode 的值不为 1001 则视为 cookie 未过期
                return False # 执行函数后输出假
        else: # 状态码不为 200
            return False # 执行函数后输出假
    except: # 如果 try 中发生任何错误
        return False # 执行函数后输出假


# 监控布道场频道
@client.on(events.NewMessage(chats=-1001197524983))
async def shopbean(event):
    """
    监控布道场
    """
    message = event.message.text # 获取频道发布的消息
    url = re.findall(re.compile(r"[(](https://api\.m\.jd\.com.*?)[)]", re.S), message) # 获取频道发布的消息中符合正则表达式的 url 链接
    if url != [] and len(cookies) > 0: # 如果 url 链接不为空，且 cookies 列表的长度大于 0
        i = 0 # 定义 i 为 0
        info = '关注店铺\n' + message.split("\n")[0] + "\n" # 定义给 Telegram Bot 发送消息的消息标题
        for cookie in cookies: # 从 cookies 列表中轮询 cookie
            try: # 开始尝试执行下列代码
                i += 1 # 把上一个 i 加上 1
                info += getbean(i, cookie, url[0]) # 执行 getBean() 函数后生成消息的消息内容
            except:  # 如果 try 中发生任何错误
                continue # 继续执行 for 下的代码
        await jdbot.send_message(chat_id, info) # 执行完 for 下的代码给 Telegram Bot 发送消息


# 监控龙王庙频道
@client.on(events.NewMessage(chats=-1001159808620))
async def redrain(event):
    """
    监控龙王庙
    """
    message = event.message.text # 获取频道发布的消息
    if 'RRA' in message and '开始' in message and '结束' in message: # 消息中包含 RRA 开始 结束 三个词
        RRA = re.findall(r"RRA.*", message) # 截取 RRA 字符串
        input_RRA = '&'.join(RRA) # 处理 RRA 字符串
        start_time = re.findall(re.compile(r"开.*"), message) # 截取开始时间
        file = '-'.join(start_time[0].split(' ')[1].split(':')[:-1]) # 定义文件名
        with open(f'{_LogDir}/{file}.txt', 'w', encoding='utf-8') as f: # 打开 log 下一个新的写入文件
            print(input_RRA, file=f) # 把 RRA 字符串写入文件中


# 临时屏蔽某个cookie
@client.on(events.NewMessage(from_users=chat_id, pattern=r'^/checkcookie'))
async def check():
    """
    临时屏蔽某个cookie
    """
    m = checkCookie1() #定义 m 为执行 checkCookie1() 函数检查是否有过期的 cookie 的结果
    msg = await jdbot.send_message(chat_id, '正在自动检测 cookie 过期情况......') # 给用户发送一条消息证明程序没有在偷懒
    if m == []: # 如果 m 是一个空列表
        await jdbot.edit_message(msg, '没有 Cookie 过期，无需临时屏蔽') # 给用户发送一条消息证明程序没有在偷懒
    else: # 否则执行下列代码
        n = " ".join('%s' % i for i in m) # 处理 m 列表，并把结果定义成 n 变量
        path = f'{_ConfigDir}/config.sh' # 定义 path 变量为 config.sh 文件的路径
        with open(path, 'r', encoding='utf-8') as f1: # 打开 config.sh 文件，只读
            configs = f1.readlines() # 把 config.sh 文件的每一行写入一个列表，定义为 configs 变量
        for config in configs: # 从 configs 列表中轮询元素，把元素定义为 config
            if config.find('TempBlockCookie=""') != -1: # 如果 config 中找到 TempBlockCookie="" 字符串
                i = configs.index(config) # 定义 i 为该元素序列
                configs[i] = f'TempBlockCookie="{n}"\n' # 把 configs 列表中第 i 个元素替换成 TempBlockCookie="{n}"\n
                with open(path, 'w', encoding='utf-8') as f2: # 打开 config.sh 文件，覆写
                    print(''.join(configs), file=f2) # 把新的 configs 列表转化成字符串，最后写入进 config.sh 文件
                await jdbot.edit_message(msg, f'已临时屏蔽Cookie{n}') # 给用户发送一条消息证明程序没有在偷懒
                break # 退出 for 循环
            elif config.find('AutoDelCron') != -1: # 如果 config 中找不到 TempBlockCookie="" 字符串，但是却找到了 AutoDelCron 证明找过头了
                break # 退出 for 循环
            elif config.find(f'TempBlockCookie="{n}"') != -1: # 如果 config 中找到此前用户就屏蔽了这几个过期的 cookie 账户
                await jdbot.edit_message(msg, f'早时已临时屏蔽Cookie{n}，无需再次屏蔽') # 给用户发送一条消息证明程序没有在偷懒
                break # 退出 for 循环


@client.on(events.NewMessage(from_users=chat_id, pattern=r'^/untempblockcookie'))
async def check():
    """
    取消屏蔽某个cookie
    """
    msg = await jdbot.send_message(chat_id, '正在自动检测 cookie 屏蔽情况......') # 给用户发送一条消息证明程序没有在偷懒
    path = f'{_ConfigDir}/config.sh' # 定义 path 变量为 config.sh 文件的路径
    with open(path, 'r', encoding='utf-8') as f1: # 打开 config.sh 文件，只读
        configs = f1.readlines() # 把 config.sh 文件的每一行写入一个列表，定义为 configs 变量
    del(configs[-1]) # 删除 configs 列表最后一个元素，因为这一行往往是空白行
    for config in configs: # 从 configs 列表中轮询元素，把元素定义为 config 变量
        if config.find('TempBlockCookie') != -1 and config.find('举例') == -1 and configs[configs.index(config) + 1].find(';;\n') == -1: # 如果找到需要的。。。
            m = re.findall(r'\d', config) # 从 config 变量中截取纯数字，判断这是第几个账户，并定义成 m 列表
            if m != []: # 如果 m 列表不为空，则证明有账户的 cookie 被临时屏蔽
                for n in m: # 从 m 列表中轮询元素，把元素定义为 n 变量
                    Expired = checkCookie2(cookies[int(n) - 1]) # 执行 checkCookie2() 函数，并把返回结果定义为 Expired
                    if not Expired: # 如果 Expired 值不为真（即 Expired 的值是假）
                        del(m[m.index(n)]) # 把 n 的值从 m 中删除，因为第 n 个账号的 cookie 值已经有效
                        await jdbot.edit_message(msg, f'取消临时屏蔽 Cookie{n} 成功') # 给用户发送一条消息证明程序没有在偷懒
                if m != []: # 如果轮询完发现 m 列表不为空，则仍有账户的 cookie 是过期的
                    x = ' '.join(m) # 把 m 列表转换成字符串，并定义为 x
                    configs[configs.index(config)] = f'TempBlockCookie="{x}"\n' # 把 configs 列表的第 configs.index(config) 个元素替换成需要的格式
                else: # 如果轮询完发现 m 列表为空，则已经没有账户的 cookie 是过期的了
                    configs[configs.index(config)] = f'TempBlockCookie=""\n'  # 把 configs 列表的第 configs.index(config) 个元素替换成需要的格式，即 TempBlockCookie=""
                    await jdbot.edit_message(msg, '取消屏蔽所有 Cookie 成功') # 给用户发送一条消息证明程序没有在偷懒
                with open(path, 'w', encoding='utf-8') as f2: # 打开 config.sh 文件，覆写
                        print(''.join(configs), file=f2)  # 把新的 configs 列表转化成字符串，最后写入进 config.sh 文件
            else: # 如果一开始的 m 列表不为空，则证明没有账户的 cookie 被临时屏蔽
                await jdbot.edit_message(msg, '没有 Cookie 被临时屏蔽') # 给用户发送一条消息证明程序没有在偷懒
        elif config.find('AutoDelCron') != -1: # 如果 config 中找不到符合条件的字符串，但是却找到了 AutoDelCron 则证明找过头了
            break # 退出 for 循环
