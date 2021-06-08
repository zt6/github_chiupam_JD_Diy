#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-08 23:11
# @Version  : v 2.2
# @Updata   : 1. 监控我的频道，及时更新最新的user.py和bot.py；2. 混淆
# @Future   : 1.

from ..import chat_id ,jdbot ,_ConfigDir ,logger ,api_id ,api_hash ,proxystart ,proxy ,_ScriptsDir ,_JdbotDir ,TOKEN
from ..bot .utils import cookies ,cmd ,press_event ,backfile ,jdcmd ,_DiyDir ,V4 ,QL ,_ConfigFile 
from telethon import events ,TelegramClient 
import re ,json ,requests ,os 
if proxystart :
    client =TelegramClient ("diy",api_id ,api_hash ,proxy =proxy ,connection_retries =None ).start ()
else :
    client =TelegramClient ("diy",api_id ,api_hash ,connection_retries =None ).start ()
OOO000O0O0O00000O =int (TOKEN .split (':')[0 ])
if not os .path .isfile ('/jd/jbot/diy/bot.py'):
    os .system (f'cd /jd/jbot/diy/ && wget https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py')
    if os .path .isfile ('/jd/jbot/diy/bot.py'):
        os .system ('pm2 restart jbot')
def oxoxoxoxox ():
    ""
    OO0O00O0OO00OOO0O =re .compile (r'pt_key=\S*;pt_pin=\S*;')
    with open (_ConfigFile ,'r',encoding ='utf-8')as OOO0OO0O00OO0000O :
        OO00OO00O0O000000 =OOO0OO0O00OO0000O .read ()
    OOO0OO00OO00OO0OO =OO0O00O0OO00OOO0O .findall (OO00OO00O0O000000 )
    for OO00O000O000OO00O in OOO0OO00OO00OO0OO :
        if OO00O000O000OO00O =='pt_key=xxxxxxxxxx;pt_pin=xxxx;':
            OOO0OO00OO00OO0OO .remove (OO00O000O000OO00O )
            break 
    return OOO0OO00OO00OO0OO 
def oxoxxoxoxo ():
    ""
    O0O00O0000OO00O00 =[]
    OOOOOO0OOOOO0OO0O =oxoxoxoxox ()
    for O00O0000O0OOO0OO0 in OOOOOO0OOOOO0OO0O :
        O0O00OO000O00O0O0 =OOOOOO0OOOOO0OO0O .index (O00O0000O0OOO0OO0 )+1 
        if oxoxxoxooxo (O00O0000O0OOO0OO0 ):
            O0O00O0000OO00O00 .append (O0O00OO000O00O0O0 )
    return O0O00O0000OO00O00 ,OOOOOO0OOOOO0OO0O 
def oxoxxoxooxo (O00O0OO000O00O0OO ):
    ""
    O000O00OOO000OO0O ="https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    OOO00OOO0OOO00O00 ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":O00O0OO000O00O0OO ,"User-Agent":"jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1","Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate, br"}
    try :
        O00O0O0O00O0OOOO0 =requests .get (O000O00OOO000OO0O ,headers =OOO00OOO0OOO00O00 )
        if O00O0O0O00O0OOOO0 .ok :
            O0O0OO00O000O0000 =O00O0O0O00O0OOOO0 .json ()
            if O0O0OO00O000O0000 ['retcode']=='1001':
                return True 
            else :
                return False 
        else :
            return False 
    except :
        return False 
def checkCrontab (OO00O0OOOOOO0O000 ,OOOOOOOOOO0OOO0O0 ,O000000OO00O0OO0O ,O0O0O00O0OOO000O0 ):
    ""
    O0000O000OO0OOO00 =f'{_ConfigDir}/crontab.list'
    OO0O000O000000000 =f'# {O000000OO00O0OO0O}（请勿删除此行）\n'
    O00O00O0O0O0O0O0O =f'{OO00O0OOOOOO0O000} {OOOOOOOOOO0OOO0O0} {O0O0O00O0OOO000O0}\n'
    with open (O0000O000OO0OOO00 ,'r',encoding ='utf-8')as O00OOOOOO0OOO0O0O :
        OO0OO000OO0000O0O =O00OOOOOO0OOO0O0O .readlines ()
    if OO0OO000OO0000O0O [-1 ]=='\n':
        del (OO0OO000OO0000O0O [-1 ])
    if OO0O000O000000000 in OO0OO000OO0000O0O :
        OO00000OOOOOO000O =OO0OO000OO0000O0O .index (OO0O000O000000000 )+1 
        if OO0OO000OO0000O0O [OO00000OOOOOO000O ]!=O00O00O0O0O0O0O0O :
            OO0OO000OO0000O0O [OO00000OOOOOO000O ]=O00O00O0O0O0O0O0O 
            with open (O0000O000OO0OOO00 ,'w',encoding ='utf-8')as O000OO0OO000OO0OO :
                O000OO0OO000OO0OO .write (''.join (OO0OO000OO0000O0O ))
    else :
        OO0OO000OO0000O0O .append (f'\n{OO0O000O000000000}{O00O00O0O0O0O0O0O}')
        with open (O0000O000OO0OOO00 ,'w',encoding ='utf-8')as O000OO0OO000OO0OO :
            O000OO0OO000OO0OO .write (''.join (OO0OO000OO0000O0O ))
def getbean (OO00O0000OO0OOO0O ,OOOOOOOO0OO0O0OO0 ,OO0O0OOOO0000O0OO ):
    ""
    O0OOOO000000OOOO0 ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36","Accept-Encoding":"gzip,compress,br,deflate","Cookie":OOOOOOOO0OO0O0OO0 ,}
    O000OO000OO00OO0O ,O0OOOO00OOOOO0OOO ='','\n\t\t└'
    try :
        O0OOO0OOO000OOO0O =requests .get (url =OO0O0OOOO0000O0OO ,headers =O0OOOO000000OOOO0 )
        O0O0O0OOOOOOOOOO0 =O0OOO0OOO000OOO0O .json ()
        if O0O0O0OOOOOOOOOO0 ['code']=='0':
            O0O00O0OO0O0OOOO0 =O0O0O0OOOOOOOOOO0 ['result']['followDesc']
            if O0O00O0OO0O0OOOO0 .find ('成功')!=-1 :
                try :
                    for OO0O0OO00O000O0O0 in range (len (O0O0O0OOOOOOOOOO0 ['result']['alreadyReceivedGifts'])):
                        O00000OO00OOO0OOO =O0O0O0OOOOOOOOOO0 ['result']['alreadyReceivedGifts'][OO0O0OO00O000O0O0 ]['redWord']
                        OO000O00O0OO0OOO0 =O0O0O0OOOOOOOOOO0 ['result']['alreadyReceivedGifts'][OO0O0OO00O000O0O0 ]['rearWord']
                        O000OO000OO00OO0O +=f"{O0OOOO00OOOOO0OOO}领取成功，获得{O00000OO00OOO0OOO}{OO000O00O0OO0OOO0}"
                except :
                    OO0O000OOO0O0OOO0 =O0O0O0OOOOOOOOOO0 ['result']['giftsToast'].split (' \n ')[1 ]
                    O000OO000OO00OO0O =f"{O0OOOO00OOOOO0OOO}{OO0O000OOO0O0OOO0}"
            elif O0O00O0OO0O0OOOO0 .find ('已经')!=-1 :
                O000OO000OO00OO0O =f"{O0OOOO00OOOOO0OOO}{O0O00O0OO0O0OOOO0}"
        else :
            O000OO000OO00OO0O =f"{O0OOOO00OOOOO0OOO}Cookie 可能已经过期"
    except Exception as OO00OOO0OO0OO0OOO :
        if str (OO00OOO0OO0OO0OOO ).find ('(char 0)')!=-1 :
            O000OO000OO00OO0O =f"{O0OOOO00OOOOO0OOO}访问发生错误：无法解析数据包"
        else :
            O000OO000OO00OO0O =f"{O0OOOO00OOOOO0OOO}访问发生错误：{OO00OOO0OO0OO0OOO}"
    return f"\n京东账号{OO00O0000OO0OOO0O}{O000OO000OO00OO0O}\n"
@client .on (events .NewMessage (chats =-1001197524983 ,pattern =r'.*店'))
async def shopbean (O0O000O00OOO0OO0O ):
    OO0OOOO0OOOOOO000 =O0O000O00OOO0OO0O .message .text 
    OO00OOO0000OOO000 =re .findall (re .compile (r"[(](https://api\.m\.jd\.com.*?)[)]",re .S ),OO0OOOO0OOOOOO000 )
    if OO00OOO0000OOO000 !=[]and len (cookies )>0 :
        OOOOO0O0OO0000000 =0 
        O0OOOOOOOO00OO000 ='关注店铺\n'+OO0OOOO0OOOOOO000 .split ("\n")[0 ]+"\n"
        for O000OOO000O0000O0 in cookies :
            try :
                OOOOO0O0OO0000000 +=1 
                O0OOOOOOOO00OO000 +=getbean (OOOOO0O0OO0000000 ,O000OOO000O0000O0 ,OO00OOO0000OOO000 [0 ])
            except :
                continue 
        await jdbot .send_message (chat_id ,O0OOOOOOOO00OO000 )
@client .on (events .NewMessage (chats =-1001431256850 ))
async def myupuser (OO00OOOO0OO00OO0O ):
    """
    关注频道：https://t.me/jd_diy_bot_channel
    """
    try :
        if OO00OOOO0OO00OO0O .message .file :
            O0OOOOOO000O0O0OO =OO00OOOO0OO00OO0O .message .file .name 
            if O0OOOOOO000O0O0OO .endswith ("bot.py")or O0OOOOOO000O0O0OO .endswith ("user.py"):
                OO000OO00O0OOO0OO =f'{_JdbotDir}/diy/{O0OOOOOO000O0O0OO}'
                backfile (OO000OO00O0OOO0OO )
                await client .download_file (input_location =OO00OOOO0OO00OO0O .message ,file =OO000OO00O0OOO0OO )
                await jdbot .send_file (chat_id ,OO000OO00O0OOO0OO ,caption ='已更新，准备重启')
                os .system ('pm2 restart jbot')
    except Exception as O00OOOOO00OOOOO0O :
        await jdbot .send_message (chat_id ,'something wrong,I\'m sorry\n'+str (O00OOOOO00OOOOO0O ))
        logger .error ('something wrong,I\'m sorry\n'+str (O00OOOOO00OOOOO0O ))
