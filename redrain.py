"""
Author: Chiupam (https://t.me/chiupam)
version: Test v7
date: 2021-05-25
update: 1. 兼容青龙
"""


import re, os, time, requests, sys, json


def readCookies():
    """
    读取 Cookie
    """
    if isv4:
        config = f'{env}/config/config.sh'
    else:
        config = f'{env}/config/cookie.sh' # 青龙
    with open(config, 'r', encoding='utf-8') as f:
        config = ''.join(f.readlines())
    cookie = re.findall(r"pt_key=.*;pt_pin=.*;", config)
    illegal_cookie = 'pt_key=xxxxxxxxxx;pt_pin=xxxx;'
    if illegal_cookie in cookie:
        m = cookie.index(illegal_cookie)
        del(cookie[m])
    return cookie


def readRRAs():
    """
    读取 RRA
    """
    with open(RRA_file, 'r', encoding='utf-8') as f:
        RRA = f.read()[:-1]
        if '&' in RRA:
            RRA = RRA.split('&')
        else:
            RRA = [RRA]
        return RRA


def receiveRedRain(i, cookie, RRA):
    """
    发起 GET 请求
    """
    body = {
        "functionId": "noahRedRainLottery",
        "actId": RRA,
        "client": "wh5",
        "clientVersion": "1.0.0",
        "_": round(time.time() * 1000)
    }
    url = 'https://api.m.jd.com/api'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-cn",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "api.m.jd.com",
        "Referer": f"https://h5.m.jd.com/active/redrain/index.html?id={RRA}&lng=0.000000&lat=0.000000&sid=&un_area=",
        "Cookie": cookie,
        "User-Agent": "JD4iPhone/9.3.5 CFNetwork/1209 Darwin/20.2.0"
        }
    r = requests.get(url, params=body, headers=headers).json()
    account = f'京东账号{i}\n\t\t└'
    if r['subCode'] == '0':
        res = f"{account}领取成功，获得 {r['lotteryResult']['PeasList'][0]['quantity']}京豆\n"
    elif r['subCode'] == '8':
        res = "{account}领取失败，本场已领过\n"
    else:
        res = f"{account}异常：{r['msg']}\n"
    return res


def checkCrontab():
    """
    新旧命令对比，有新命令则写入新命令
    """
    storage = '/' + path_list[-2]
    file = '/' + path_list[-1]
    crontab_list = f'{env}/config/crontab.list'
    key = '# 直播间红包雨（请勿删除此行）\n'
    new = f'{cron} python /jd{storage}{file} >> /jd/log{file.split(".")[0]}.log 2>&1\n'
    with open(crontab_list, 'r', encoding='utf-8') as f1:
        crontab = f1.readlines()
    if crontab[-1] == '\n':
        del(crontab[-1])
    if key in crontab:
        m = crontab.index(key)
        if crontab[m + 1] != new:
            del(crontab[m + 1])
            crontab.insert(m + 1,new)
    else:
        crontab.append(f'\n{key}{new}')
    with open(crontab_list, 'w', encoding='utf-8') as f2:
        print(''.join(crontab), file=f2)


def main(cookies, RRAs):
    """
    执行任务
    """
    i = 0
    info = '京东直播间红包雨\n\n'
    for cookie in cookies:
        for RRA in RRAs:
            try:
                i += 1
                info += receiveRedRain(i, cookie, RRA)
            except Exception as error:
                print(error)
                continue
    tgNofity(info)


def tgNofity(text):
    """
    Telegram Bot 推送
    """
    bot = f'{env}/config/bot.json'
    with open(bot, 'r', encoding='utf-8') as botSet:
        bot = json.load(botSet)
    url = f"https://api.telegram.org/bot{bot['bot_token']}/sendMessage"
    body = {
        "chat_id": bot['user_id'],
        "text": text,
        "disable_web_page_preview": True
    }
    headers = {
        "ontent-Type": "application/x-www-form-urlencoded"
    }
    try:
        r = requests.post(url, data=body, headers=headers)
        if r.ok:
            print("Telegram发送通知消息成功🎉。\n")
        elif r.status_code == '400':
            print("请主动给bot发送一条消息并检查接收用户ID是否正确。\n")
        elif r.status_code == '401':
            print("Telegram bot token 填写错误。\n")
    except Exception as error:
        print(f"telegram发送通知消息失败！！\n{error}")


# 主程序
def run():
    """
    主程序
    """
    checkCrontab()
    if os.path.isfile(RRA_file):
        main(readCookies(), readRRAs())
        os.remove(RRA_file)
    else:
        sys.exit()


# 开始执行主程序
if __name__ == '__main__':
    path_list = os.path.realpath(__file__).split('/')[1:]
    env = '/' + '/'.join(path_list[:-2])
    if os.path.isfile('/ql/config/cookie.sh') or os.path.isfile(f'{env}/config/cookie.sh'): # 青龙
        isv4 = False
        if not os.path.isfile(f'{env}/config/cookie.sh'): # 青龙容器内
            env = '/ql'
    else: # v4-bot
        isv4 = True
        if not os.path.isfile(f'{env}/config/config.sh'): # v4-bot 容器内
            env = '/jd'
    RRA_file = f'{env}/log/{time.localtime()[3]}-{time.localtime()[4]}.txt'
    cron = '*/30 * * * *'
    run()

