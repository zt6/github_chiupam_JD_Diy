#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-08 23:10
# @Version  : v 2.4
# @Updata   : 1. 下载 raw 链接后可以识别 cron 表达式并询问是否需要添加；2. 支持 v4-bot 用户在给 /checkcookie 屏蔽后的 cookie可以给面板扫码自动替换；3. 支持发送机器人文件的 raw 链接；4. 优化；5. 混淆
# @Future   :
from ..import chat_id ,jdbot ,_ConfigDir ,_ScriptsDir ,_OwnDir ,_LogDir ,logger ,TOKEN ,_JdbotDir 
from ..bot .utils import cmd ,press_event ,backfile ,jdcmd ,_DiyDir ,V4 ,QL ,_ConfigFile 
from telethon import events ,Button 
from asyncio import exceptions 
import requests ,re ,os ,asyncio 
OOO000O0O0O00000O =int (TOKEN .split (':')[0 ])
def oxoxoxoxox ():
    O0O0O0OO00OO00000 =re .compile (r'pt_key=\S*;pt_pin=\S*;')
    with open (f'{_ConfigDir}/config.sh','r',encoding ='utf-8')as OO0OOO0O0OO0OOOOO :
        OOOOOOOO0O00O0OOO =OO0OOO0O0OO0OOOOO .read ()
    OOO000O0O0O000000 =O0O0O0OO00OO00000 .findall (OOOOOOOO0O00O0OOO )
    for O0OOOOO00OO00OO0O in OOO000O0O0O000000 :
        if O0OOOOO00OO00OO0O =='pt_key=xxxxxxxxxx;pt_pin=xxxx;':
            OOO000O0O0O000000 .remove (O0OOOOO00OO00OO0O )
            break 
    return OOO000O0O0O000000 
def oxoxxoxoxo ():
    OO000O0OO000OO00O =[]
    OOO0O00O0O0O00OOO =oxoxoxoxox ()
    for O00O00O00OOOOO000 in OOO0O00O0O0O00OOO :
        OOOOOOOOO00O0OO0O =OOO0O00O0O0O00OOO .index (O00O00O00OOOOO000 )+1 
        if oxoxxoxooxo (O00O00O00OOOOO000 ):
            OO000O0OO000OO00O .append (OOOOOOOOO00O0OO0O )
    return OO000O0OO000OO00O ,OOO0O00O0O0O00OOO 
def oxoxxoxooxo (OOO0OO0OO00OOOOOO ):
    O0OO0OOO00OOO0OOO ="https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    OOO000O00O0O00OO0 ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":OOO0OO0OO00OOOOOO ,"User-Agent":"jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1","Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate, br"}
    try :
        O0O0O000OO0OO0OO0 =requests .get (O0OO0OOO00OOO0OOO ,headers =OOO000O00O0O00OO0 )
        if O0O0O000OO0OO0OO0 .ok :
            OO0OOOOO0OO0OO0OO =O0O0O000OO0OO0OO0 .json ()
            if OO0OOOOO0OO0OO0OO ['retcode']=='1001':
                return True 
            else :
                return False 
        else :
            return False 
    except :
        return False 
@jdbot .on (events .NewMessage (from_users =chat_id ,pattern =r'^/start$'))
async def myhello (OO0O0O000O00O00OO ):
    try :
        OO0OO0OO0OOO0O000 ="""自定义机器人使用方法如下：
    /start 开始使用此自定义机器人
    /restart 重启机器人
    /upbot 升级此自定义机器人
    /help 获取机器人所有快捷命令，可直接发送至botfather
    /checkcookie 检测失效Cookie并把它屏蔽
    此外 1、发送已 raw 的链接会下载文件，并让用户做出选择（可能不支持青龙）
        2、发送仓库链接会开始添加仓库，用户按要求回复即可（不支持青龙）
        3、接受到 cookie 过期消息自动开启 /checkcookie 指令

    仓库：https://github.com/chiupam/JD_Diy.git
    欢迎🌟Star & 提出🙋[isuss](https://github.com/chiupam/JD_Diy/issues/new) & 请勿🚫Fork
    频道：[👬和东哥做兄弟](https://t.me/jd_diy_bot_channel) （不开放闲聊，仅讨论脚本）
"""
        await asyncio .sleep (0.5 )
        await jdbot .send_message (chat_id ,OO0OO0OO0OOO0O000 )
    except Exception as O00OO00O0000O0000 :
        await jdbot .send_message (chat_id ,'something wrong,I\'m sorry\n'+str (O00OO00O0000O0000 ))
        logger .error ('something wrong,I\'m sorry\n'+str (O00OO00O0000O0000 ))
@jdbot .on (events .NewMessage (from_users =chat_id ,pattern =r'^/help$'))
async def myhelp (O000OOOO00O000O00 ):
    try :
        O00O0000000000OOO ="""restart - 重启机器人
upbot - 升级自定义机器人
checkcookie - 检测cookie过期
"""
        await asyncio .sleep (0.5 )
        await jdbot .send_message (chat_id ,O00O0000000000OOO )
    except Exception as OO0O000000000O00O :
        await jdbot .send_message (chat_id ,'something wrong,I\'m sorry\n'+str (OO0O000000000O00O ))
        logger .error ('something wrong,I\'m sorry\n'+str (OO0O000000000O00O ))
@jdbot .on (events .NewMessage (from_users =[chat_id ,OOO000O0O0O00000O ],pattern =r'^/checkcookie$|.*cookie已失效'))
async def mycheckcookie (O0OOO00O00000OOOO ):
    try :
        O000OOO00O0O0O000 =await jdbot .send_message (chat_id ,'正在检测 cookie 过期情况')
        O000000000OO0OO00 =oxoxxoxoxo ()
        O000OO0O0OOOO00OO =O000000000OO0OO00 [0 ]
        O0OO0O0O00OO00O0O ,OOOOO0O00O00O0OO0 ='检测结果\n\n','\n\t   └ '
        OOOOOOO0OO0O00000 =False 
        if V4 :
            O0O00OOO000OO0O0O ='/jd/panel/server.js'
            if os .path .isfile (O0O00OOO000OO0O0O ):
                O0O00OOO000OO0O0O =True 
                with open (_ConfigFile ,'r',encoding ='utf-8')as OO00OOOOOOOO0O0OO :
                    O0OO0000O0000O00O =OO00OOOOOOOO0O0OO .read ()
                O0O000O0OO0O00OOO =" ".join ('%s'%O00O0O000OO0OO0OO for O00O0O000OO0OO0OO in O000OO0O0OOOO00OO )
                O0OO0000O0000O00O =re .sub (r'TempBlockCookie=""',f'TempBlockCookie="{O0O000O0OO0O00OOO}"',O0OO0000O0000O00O ,re .M )
                O0OO0O0O00OO00O0O +=f'【屏蔽情况】{OOOOO0O00O00O0OO0}TempBlockCookie="{O0O000O0OO0O00OOO}"\n\n使用修改 TempBlockCookie 策略'
                OOOOOOO0OO0O00000 =True 
            else :
                O0O00OOO000OO0O0O =False 
                with open (_ConfigFile ,'r',encoding ='utf-8')as OO00OOOOOOOO0O0OO :
                    O0OO0000O0000O00O =OO00OOOOOOOO0O0OO .readlines ()
                if O0OO0000O0000O00O [-1 ]=='\n':
                    del (O0OO0000O0000O00O [-1 ])
                OO0OOOOOO00OO00O0 ='此账号的cookie已经失效'
                for OO00OOOOO0O0OOOOO in O000OO0O0OOOO00OO :
                    for OO0O00OOO00OO00O0 in O0OO0000O0000O00O :
                        if OO0O00OOO00OO00O0 .find (f'Cookie{OO00OOOOO0O0OOOOO}')!=-1 and OO0O00OOO00OO00O0 .find ('# Cookie')==-1 :
                            O0OO00OOOOO0O0000 =OO0O00OOO00OO00O0 .split (';')[-2 ].split ('=')[-1 ]
                            O0OO0000O0000O00O [O0OO0000O0000O00O .index (OO0O00OOO00OO00O0 )]=f'Cookie{OO00OOOOO0O0OOOOO}="{O0OO00OOOOO0O0000}{OO0OOOOOO00OO00O0}"\n'
                            OOOOOOO0OO0O00000 =True 
                            O0OO0O0O00OO00O0O +=f'【屏蔽情况】 {O0OO00OOOOO0O0000}{OOOOO0O00O00O0OO0}临时替换第 {OO00OOOOO0O0OOOOO} 个用户的cookie\n'
                        elif OO0O00OOO00OO00O0 .find ('第二区域')!=-1 :
                            break 
        elif QL :
            O0O00OOO000OO0O0O =False 
            with open (_ConfigFile ,'r',encoding ='utf-8')as OO00OOOOOOOO0O0OO :
                O0OO0000O0000O00O =OO00OOOOOOOO0O0OO .readlines ()
            if O0OO0000O0000O00O [-1 ]=='\n':
                del (O0OO0000O0000O00O [-1 ])
            for OO00OOOOO0O0OOOOO in O000OO0O0OOOO00OO :
                OOOO0O0O00OOO00OO =O0OO0000O0000O00O [int (OO00OOOOO0O0OOOOO )-1 ]
                O0OO00OOOOO0O0000 =OOOO0O0O00OOO00OO .split (';')[-2 ]
                del (O0OO0000O0000O00O [int (OO00OOOOO0O0OOOOO )-1 ])
                OOOOOOO0OO0O00000 =True 
                O0OO0O0O00OO00O0O +=f'【删除情况】{O0OO00OOOOO0O0000}{OOOOO0O00O00O0OO0}已经删除第 {OO00OOOOO0O0OOOOO} 个用户的Cookie\n'
        else :
            await jdbot .edit_message (O000OOO00O0O0O000 ,'未知环境的用户，无法使用 /checkcookie 指令')
            return 
        if OOOOOOO0OO0O00000 :
            if O0O00OOO000OO0O0O :
                with open (_ConfigFile ,'w',encoding ='utf-8')as O0O0OOO0O000OOOO0 :
                    O0O0OOO0O000OOOO0 .write (O0OO0000O0000O00O )
            else :
                with open (_ConfigFile ,'w',encoding ='utf-8')as O0O0OOO0O000OOOO0 :
                    O0O0OOO0O000OOOO0 .write (''.join (O0OO0000O0000O00O ))
            await jdbot .edit_message (O000OOO00O0O0O000 ,O0OO0O0O00OO00O0O )
        else :
            await jdbot .edit_message (O000OOO00O0O0O000 ,'配置无需改动，可用cookie中并没有cookie过期')
    except Exception as OO0OOO0OO00OOO000 :
        await jdbot .send_message (chat_id ,'something wrong,I\'m sorry\n'+str (OO0OOO0OO00OOO000 ))
        logger .error ('something wrong,I\'m sorry\n'+str (OO0OOO0OO00OOO000 ))
@jdbot .on (events .NewMessage (from_users =chat_id ,pattern =r'^/restart$'))
async def myrestart (O00OO00O0O0OO0000 ):
    try :
        await jdbot .send_message (chat_id ,'准备重启机器人')
        os .system ('pm2 restart jbot')
    except Exception as O0O00OOOO000O00O0 :
        await jdbot .send_message (chat_id ,'something wrong,I\'m sorry\n'+str (O0O00OOOO000O00O0 ))
        logger .error ('something wrong,I\'m sorry\n'+str (O0O00OOOO000O00O0 ))
@jdbot .on (events .NewMessage (from_users =chat_id ,pattern =r'^/upbot$'))
async def myupbot (O000O0O0O0O0OO0OO ):
    try :
        OOO0O0O00O0O0000O =await jdbot .send_message (chat_id ,'开始下载最新的bot.py文件')
        OO00OO0O00OOOOO0O ='https://raw.githubusercontent.com/chiupam/JD_Diy/master/jbot/bot.py'
        OOOO000O0O0OO0OOO =requests .get (f'http://ghproxy.com/{OO00OO0O00OOOOO0O}').text 
        if OOOO000O0O0OO0OOO :
            O000000OOO0O00O00 =f'{_JdbotDir}/diy/bot.py'
            backfile (O000000OOO0O00O00 )
            with open (O000000OOO0O00O00 ,'w+',encoding ='utf-8')as O0O00O0000OO00OO0 :
                O0O00O0000OO00OO0 .write (OOOO000O0O0OO0OOO )
            await jdbot .edit_message (OOO0O0O00O0O0000O ,'准备重启机器人')
            os .system ('pm2 restart jbot')
        else :
            await jdbot .edit_message (OOO0O0O00O0O0000O ,"下载失败，请稍后重试")
    except Exception as O0OOO0O000O0OOO0O :
        await jdbot .send_message (chat_id ,'something wrong,I\'m sorry\n'+str (O0OOO0O000O0OOO0O ))
        logger .error ('something wrong,I\'m sorry\n'+str (O0OOO0O000O0OOO0O ))
@jdbot .on (events .NewMessage (from_users =chat_id ,pattern =r'^https?://(raw)?.*(github|GitHub)?.*(js|py|sh)$'))
async def mydownload (OO0OO0OO00OO00OOO ):
    try :
        OO000O00OO0OOO000 =OO0OO0OO00OO00OOO .sender_id 
        O0OO00O0O00OOOO0O =await jdbot .send_message (chat_id ,'开启下载文件会话')
        OOOOO00O00O0OO000 =[[Button .inline ('我需要下载此链接文件，请继续',data ='confirm')],[Button .inline ('我不需要下载，请取消对话',data ='cancel')]]
        async with jdbot .conversation (OO000O00OO0OOO000 ,timeout =60 )as OO0OOO0OOO0OO0O0O :
            await jdbot .delete_messages (chat_id ,O0OO00O0O00OOOO0O )
            O0OO00O0O00OOOO0O =await OO0OOO0OOO0OO0O0O .send_message ('检测到你发送了一条链接，请做出你的选择：\n')
            O0OO00O0O00OOOO0O =await jdbot .edit_message (O0OO00O0O00OOOO0O ,'检测到你发送了一条链接，请做出你的选择：',buttons =OOOOO00O00O0OO000 )
            OO00O00OO00O00O0O =await OO0OOO0OOO0OO0O0O .wait_event (press_event (OO000O00OO0OOO000 ))
            OO0O0O0OOOO0O00O0 =bytes .decode (OO00O00OO00O00O0O .data )
            if OO0O0O0OOOO0O00O0 =='cancel':
                O0OO00O0O00OOOO0O =await jdbot .edit_message (O0OO00O0O00OOOO0O ,'对话已取消')
                OO0OOO0OOO0OO0O0O .cancel ()
            else :
                await jdbot .delete_messages (chat_id ,O0OO00O0O00OOOO0O )
                OOO0OO0OO000O0000 =OO0OO0OO00OO00OOO .raw_text 
                if OOO0OO0OO000O0000 .startswith ('https://raw.githubusercontent.com'):
                    O00O0000000OO0O00 =f'http://ghproxy.com/{OOO0OO0OO000O0000}'
                OO000OOO0OO000O00 =O00O0000000OO0O00 .split ('/')[-1 ]
                O000O00000OOOO000 =requests .get (OOO0OO0OO000O0000 ).text 
                OOOO00O00O000OOO0 =re .findall (r"(?<=new\sEnv\(').*(?=')",O000O00000OOOO000 ,re .M )
                try :
                    OOO0OOO000OO0O00O =re .search (r'(\d\s|\*\s){4}\*',O000O00000OOOO000 ).group ()
                except :
                    OOO0OOO000OO0O00O =None 
                if OOOO00O00O000OOO0 !=[]:
                    OOOO00O00O000OOO0 =OOOO00O00O000OOO0 [0 ]
                else :
                    OOOO00O00O000OOO0 =''
                OOOOO00O00O0OO000 =[[Button .inline ('放入config目录',data =_ConfigDir ),Button .inline ('放入jbot/diy目录',data =f'{_JdbotDir}/diy')],[Button .inline ('放入own目录',data =_DiyDir ),Button .inline ('放入own并运行',data ='run_own')],[Button .inline ('放入scripts目录',data =_ScriptsDir ),Button .inline ('放入scripts并运行',data ='run_scripts')],[Button .inline ('请帮我取消对话',data ='cancel')]]
                if O000O00000OOOO000 :
                    O0O0O0OOOOO000O0O =True 
                    OOO0O00O00O0OO0O0 =None 
                    O0OO00O0O00OOOO0O =await OO0OOO0OOO0OO0O0O .send_message (f'成功下载{OOOO00O00O000OOO0}脚本\n现在，请做出你的选择：')
                    O0OO00O0O00OOOO0O =await jdbot .edit_message (O0OO00O0O00OOOO0O ,f'成功下载{OOOO00O00O000OOO0}脚本\n现在，请做出你的选择：',buttons =OOOOO00O00O0OO000 )
                    OO00O00OO00O00O0O =await OO0OOO0OOO0OO0O0O .wait_event (press_event (OO000O00OO0OOO000 ))
                    OO0O0O0OOOO0O00O0 =bytes .decode (OO00O00OO00O00O0O .data )
                    if OO0O0O0OOOO0O00O0 =='cancel':
                        O0O0O0OOOOO000O0O =False 
                        O0OO00O0O00OOOO0O =await jdbot .edit_message (O0OO00O0O00OOOO0O ,'对话已取消')
                    elif OO0O0O0OOOO0O00O0 =='run_own':
                        OOO0OO00O0O000OO0 ,OOO0O00O00O0OO0O0 =f'{_DiyDir}/{OO000OOO0OO000O00}',f'{jdcmd} {_DiyDir}/{OO000OOO0OO000O00} now'
                        await jdbot .edit_message (O0OO00O0O00OOOO0O ,f'{OOOO00O00O000OOO0}脚本已保存到own目录，并成功在后台运行，请稍后自行查看日志')
                    elif OO0O0O0OOOO0O00O0 =='run_scripts':
                        OOO0OO00O0O000OO0 ,OOO0O00O00O0OO0O0 =f'{_ScriptsDir}/{OO000OOO0OO000O00}',f'{jdcmd} {_ScriptsDir}/{OO000OOO0OO000O00} now'
                        await jdbot .edit_message (O0OO00O0O00OOOO0O ,f'{OOOO00O00O000OOO0}脚本已保存到scripts目录，并成功在后台运行，请稍后自行查看日志')
                    elif OO0O0O0OOOO0O00O0 ==f'{_JdbotDir}/diy':
                        OOO0OO00O0O000OO0 =f'{OO0O0O0OOOO0O00O0}/{OO000OOO0OO000O00}'
                        await jdbot .edit_message (O0OO00O0O00OOOO0O ,f'机器人文件已保存到{OO0O0O0OOOO0O00O0}目录\n请记得使用 /restart 指令重启机器人')
                        OOO0OOO000OO0O00O =False 
                    else :
                        OOO0OO00O0O000OO0 =f'{OO0O0O0OOOO0O00O0}/{OO000OOO0OO000O00}'
                        await jdbot .edit_message (O0OO00O0O00OOOO0O ,f'{OOOO00O00O000OOO0}脚本已保存到{OO0O0O0OOOO0O00O0}目录')
                    if OOO0OOO000OO0O00O :
                        OOOOO00O00O0OO000 =[[Button .inline ('是的，请帮我添加定时任务',data ='add')],[Button .inline ('谢谢，但我暂时不需要',data ='cancel')],]
                        O0OO00O0O00OOOO0O =await OO0OOO0OOO0OO0O0O .send_message (f"这是我识别出来的 cron 表达式\n{OOO0OOO000OO0O00O}\n请问需要把它添加进定时任务中吗？")
                        await jdbot .edit_message (O0OO00O0O00OOOO0O ,f"这是我识别出来的 cron 表达式\n{OOO0OOO000OO0O00O}\n请问需要把它添加进定时任务中吗？",buttons =OOOOO00O00O0OO000 )
                        OO00O00OO00O00O0O =await OO0OOO0OOO0OO0O0O .wait_event (press_event (OO000O00OO0OOO000 ))
                        O0OOO0O00O0OO0O0O =bytes .decode (OO00O00OO00O00O0O .data )
                        if O0OOO0O00O0OO0O0O =='add':
                            OO000OOOOOOOOOO00 =f'{_ConfigDir}/crontab.list'
                            with open (OO000OOOOOOOOOO00 ,'a',encoding ='utf-8')as OOO0OOOO000O00OO0 :
                                OOO0OOOO000O00OO0 .write (f'{OOO0OOO000OO0O00O} mtask {OOO0OO00O0O000OO0}\n')
                            await jdbot .edit_message (O0OO00O0O00OOOO0O ,'我已经把它添加进定时任务中了')
                        else :
                            await jdbot .edit_message (O0OO00O0O00OOOO0O ,'那好吧，会话结束，感谢你的使用')
                    OO0OOO0OOO0OO0O0O .cancel ()
                    if O0O0O0OOOOO000O0O :
                        backfile (OOO0OO00O0O000OO0 )
                        with open (OOO0OO00O0O000OO0 ,'w+',encoding ='utf-8')as OOO0OOOO000O00OO0 :
                            OOO0OOOO000O00OO0 .write (O000O00000OOOO000 )
                    if OOO0O00O00O0OO0O0 :
                        await cmd (OOO0O00O00O0OO0O0 )
                else :
                    O0OO00O0O00OOOO0O =await OO0OOO0OOO0OO0O0O .send_message ('下载失败，请稍后重试')
                    await jdbot .edit_message (O0OO00O0O00OOOO0O ,'下载失败，请稍后重试')
                    OO0OOO0OOO0OO0O0O .cancel ()
    except exceptions .TimeoutError :
        O0OO00O0O00OOOO0O =await jdbot .send_message (chat_id ,'选择已超时，对话已停止，感谢你的使用')
    except Exception as O0OOOOO00000O0OO0 :
        await jdbot .send_message (chat_id ,'something wrong,I\'m sorry\n'+str (O0OOOOO00000O0OO0 ))
        logger .error ('something wrong,I\'m sorry\n'+str (O0OOOOO00000O0OO0 ))
@jdbot .on (events .NewMessage (from_users =chat_id ,pattern =r'^https?://github\.com/\S+'))
async def myaddrepo (OOOO0O00OO0OOO000 ):
    try :
        OO0OO0OOO0O00O0O0 =await jdbot .send_message (chat_id ,'开始添加仓库，请按提示进行选择或操作')
        OO0O0OOO0OO0O000O =OOOO0O00OO0OOO000 .sender_id 
        O0000OO0O0000O0OO =OOOO0O00OO0OOO000 .raw_text 
        OO0OOOOOOOO0000OO =O0000OO0O0000O0OO .split ('/')[-1 ].replace (".git","")
        OOO0O0O0O0OOOO00O =[f'正在设置 OwnRepoBranch 的值\n该值为你想使用脚本在[仓库]({O0000OO0O0000O0OO})的哪个分支','正在设置 OwnRepoPath 的\n该值为你要使用的脚本在分支的哪个路径']
        OOO00O00000OOO0OO =[f'回复 main 代表使用 [{OO0OOOOOOOO0000OO}]({O0000OO0O0000O0OO}) 仓库的 "main" 分支\n回复 master 代表使用 [{short_url}]({url}) 仓库的 "master" 分支\n具体分支名称以你所发仓库实际为准\n',f'回复 scripts/jd normal 代表你想使用的脚本在 [{OO0OOOOOOOO0000OO}]({O0000OO0O0000O0OO}) 仓库的 scripts/jd 和 normal文件夹下\n回复 root cron 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 根目录 和 cron 文件夹下\n具体目录路径以你所发仓库实际为准\n']
        O000OOO000O0O00O0 =[[[Button .inline ('我使用仓库的 "默认" 分支',data ='root')],[Button .inline ('我使用仓库的 "main" 分支',data ='main'),Button .inline ('我使用仓库的 "master" 分支',data ='master')],[Button .inline ('请让我手动输入',data ='input'),Button .inline ('请帮我取消对话',data ='cancel')]],[[Button .inline ('我使用的脚本就在仓库根目录下',data ='root')],[Button .inline ('请让我手动输入',data ='input'),Button .inline ('请帮我取消对话',data ='cancel')]]]
        O0O00O0000000O0O0 =[]
        O000O00OO000OO0O0 =[]
        async with jdbot .conversation (OO0O0OOO0OO0O000O ,timeout =180 )as O000O0000OOOOO0OO :
            for O0000O00O0O00OOO0 in OOO0O0O0O0OOOO00O :
                O00O0OOOO0OOO000O =OOO0O0O0O0OOOO00O .index (O0000O00O0O00OOO0 )
                OOOOO0OO0O0O000O0 =await O000O0000OOOOO0OO .send_message (O0000O00O0O00OOO0 )
                OOOOO0OO0O0O000O0 =await jdbot .edit_message (OOOOO0OO0O0O000O0 ,O0000O00O0O00OOO0 ,buttons =O000OOO000O0O00O0 [O00O0OOOO0OOO000O ])
                O0O0OOOOO0OOOO0O0 =await O000O0000OOOOO0OO .wait_event (press_event (OO0O0OOO0OO0O000O ))
                O0OOO000O0O0000O0 =bytes .decode (O0O0OOOOO0OOOO0O0 .data )
                if O0OOO000O0O0000O0 =='cancel':
                    OOOOO0OO0O0O000O0 =await jdbot .edit_message (OOOOO0OO0O0O000O0 ,'对话已取消')
                    O000O0000OOOOO0OO .cancel ()
                    return 
                elif O0OOO000O0O0000O0 =='input':
                    await jdbot .delete_messages (chat_id ,OOOOO0OO0O0O000O0 )
                    OOOOO0OO0O0O000O0 =await O000O0000OOOOO0OO .send_message (OOO00O00000OOO0OO [O00O0OOOO0OOO000O ])
                    O0O00O0O0O00OOOO0 =await O000O0000OOOOO0OO .get_response ()
                    O0O00O0000000O0O0 .append (O0O00O0O0O00OOOO0 .raw_text )
                    await jdbot .delete_messages (chat_id ,OOOOO0OO0O0O000O0 )
                else :
                    await jdbot .delete_messages (chat_id ,OOOOO0OO0O0O000O0 )
                    O0O00O0000000O0O0 .append (O0OOO000O0O0000O0 )
            O000O0000OOOOO0OO .cancel ()
        with open (_ConfigFile ,'r',encoding ='utf-8')as O00OOOO0000OO0O0O :
            OOO0OOOO0O00O0OO0 =O00OOOO0000OO0O0O .readlines ()
        for O000OOO0OOO0O00O0 in OOO0OOOO0O00O0OO0 :
            if O000OOO0OOO0O00O0 .find ('启用其他开发者的仓库方式一')!=-1 :
                OOO0O00OO0OOOO0O0 =int (OOO0OOOO0O00O0OO0 .index (O000OOO0OOO0O00O0 ))
            elif O000OOO0OOO0O00O0 .find ('OwnRepoUrl')!=-1 and O000OOO0OOO0O00O0 .find ('#')==-1 :
                OOOO0000OO0O00O00 =int (re .findall (r'(?<=OwnRepoUrl)[\d]+(?==")',O000OOO0OOO0O00O0 )[0 ])
                OOOO0OO0000OOOO00 =re .findall (r'(?<==")[\S]+(?=")',O000OOO0OOO0O00O0 )
                if OOOO0OO0000OOOO00 ==[]:
                    O000O00OO000OO0O0 .append (OOOO0000OO0O00O00 )
                    break 
                else :
                    O000O00OO000OO0O0 .append (OOOO0000OO0O00O00 +1 )
        O000O00OO000OO0O0 .sort ()
        OO000O0000OOOOOOO =f'OwnRepoUrl{O000O00OO000OO0O0[-1]}="{O0000OO0O0000O0OO}"'
        O0O000000OO00000O =f'OwnRepoBranch{O000O00OO000OO0O0[-1]}="{O0O00O0000000O0O0[0].replace("root", "")}"'
        OOOOOO0000O0000O0 =O0O00O0000000O0O0 [1 ].replace ("root","''")
        O0OOOO00OO0O0O00O =f'OwnRepoPath{O000O00OO000OO0O0[-1]}="{OOOOOO0000O0000O0}"'
        OOO0OOOO0O00O0OO0 .insert (OOO0O00OO0OOOO0O0 +1 ,f'\n{OO000O0000OOOOOOO}\n{O0O000000OO00000O}\n{O0OOOO00OO0O0O00O}\n')
        with open (_ConfigFile ,'w',encoding ='utf-8')as OO0OO0OOOO000O000 :
            OO0OO0OOOO000O000 .write (''.join (OOO0OOOO0O00O0OO0 ))
        await jdbot .delete_messages (chat_id ,OO0OO0OOO0O00O0O0 )
        await jdbot .send_file (chat_id ,_ConfigFile ,caption ='你可以查阅上面这个文件')
        async with jdbot .conversation (OO0O0OOO0OO0O000O ,timeout =60 )as O000O0000OOOOO0OO :
            O00O0OOOOOO000O00 =[[Button .inline (f'是的，请帮我拉取{OO0OOOOOOOO0000OO}这个仓库的脚本',data ='jup')],[Button .inline ('谢谢，但我暂时不需要',data ='cancel')]]
            OOOOO0OO0O0O000O0 =await jdbot .send_message (chat_id ,'请问你需要拉取仓库里面的脚本吗？',buttons =O00O0OOOOOO000O00 )
            O0O0OOOOO0OOOO0O0 =await O000O0000OOOOO0OO .wait_event (press_event (OO0O0OOO0OO0O000O ))
            O0OOO000O0O0000O0 =bytes .decode (O0O0OOOOO0OOOO0O0 .data )
            if O0OOO000O0O0000O0 =='cancel':
                OOOOO0OO0O0O000O0 =await jdbot .edit_message (OOOOO0OO0O0O000O0 ,'配置完成，感谢你的使用')
            else :
                OOOOO0OO0O0O000O0 =await jdbot .edit_message (OOOOO0OO0O0O000O0 ,'正在为你拉取仓库脚本，详情请查阅下一条通知')
                await cmd (O0OOO000O0O0000O0 )
            O000O0000OOOOO0OO .cancel ()
    except exceptions .TimeoutError :
        OOOOO0OO0O0O000O0 =await jdbot .send_message (chat_id ,'选择已超时，对话已停止，感谢你的使用')
    except Exception as O00O0O0OO0OO0OO0O :
        await jdbot .send_message (chat_id ,'something wrong,I\'m sorry\n'+str (O00O0O0OO0OO0OO0O ))
        logger .error ('something wrong,I\'m sorry\n'+str (O00O0O0OO0OO0OO0O ))


