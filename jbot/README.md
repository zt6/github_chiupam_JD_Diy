<h1 align="center">
  自启机器人
  <br>
  Author: chiupam
</h1>

## 简介
随着 v4-bot 启动而启动的自定义机器人。
## 使用方法
1. 把文件存储在路径 `/jbot/diy/` 下，如果没有此路径请重新映射出来
2. 进入容器，使用命令 `docker exec -it jd bash`
3. 先手动停止机器人，输入命令：`pm2 stop jbot`
4. 手动前台开启机器人，输入命令：`python3 -m jbot`
5. 输入手机号码和验证码后，登陆成功，按 `Ctrl` + `C` 退出前台
6. 最后后台启动机器人，输入命令：`pm2 start jbot`
## 常见问题
- Qus1: 发送指令没有反应
  - Ans: 尝试进入容器后，删除位于 `/jd` 目录下的 `shopbean.session` 文件，然后重新按上述使用方法重新操作
- Qus2：给机器人发送 `/untempblockcookie` 指令会无法取消屏蔽一些没有过期的账号
  - Ans: 尝试多发送几次
## 已有功能
- 监控布道场，关注有礼
- 监控龙王庙，领取直播间红包
- 发送 `/checkcookie` 指令可临时屏蔽失效 `cookie`
- 发送 `/untempblockcookie` 指令可取消屏蔽 `cookie`
## 代码块
### 监控布道场
```python
@client.on(events.NewMessage(chats=-1001197524983))
async def shopbean(event):
    message = event.message.text
    url = re.findall(re.compile(r"[(](https://api\.m\.jd\.com.*?)[)]", re.S), message)
    if url != [] and len(cookies) > 0:
        i = 0
        info = '关注店铺\n' + message.split("\n")[0] + "\n"
        for cookie in cookies:
            try:
                i += 1
                info += getbean(i, cookie, url[0])
            except Exception as error:
                await jdbot.send_message(chat_id, f'\n京东账号{i}\n\t └【错误】{str(error)}')
                continue
        await jdbot.send_message(chat_id, info)
```
### 监控龙王
```python
@client.on(events.NewMessage(chats=-1001159808620))
async def redrain(event):
    message = event.message.text
    if 'RRA' in message:
        RRA = re.findall(r"RRA.*", message)
        input_RRA = '&'.join(RRA)
        start_time = re.findall(re.compile(r"开.*"), message)
        file = '-'.join(start_time[0].split(' ')[1].split(':')[:-1])
        with open(f'{_LogDir}/{file}.txt', 'w', encoding='utf-8') as f:
            print(input_RRA, file=f)
```
### checkcookie指令
```python
@client.on(events.NewMessage(from_users=chat_id, pattern=r'^/checkcookie'))
async def check(event):
    m = checkCookie1()
    msg = await jdbot.send_message(chat_id, '正在自动检测 cookie 过期情况......')
    if m == []:
        await jdbot.edit_message(msg, '没有 Cookie 过期，无需临时屏蔽')
    else:
        n = " ".join('%s' % i for i in m)
        path = f'{_ConfigDir}/config.sh'
        with open(path, 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        for config in configs:
            if config.find('TempBlockCookie=""') != -1:
                i = configs.index(config)
                configs[i] = f'TempBlockCookie="{n}"\n'
                with open(path, 'w', encoding='utf-8') as f2:
                    print(''.join(configs), file=f2)
                await jdbot.edit_message(msg, f'已临时屏蔽Cookie{n}')
                break
            elif config.find('AutoDelCron') != -1:
                break
            elif config.find(f'TempBlockCookie="{n}"') != -1:
                await jdbot.edit_message(msg, f'早时已临时屏蔽Cookie{n}，无需再次屏蔽')
```
### untempblockcookie指令
```python
@client.on(events.NewMessage(from_users=chat_id, pattern=r'^/untempblockcookie'))
async def check(event):
    msg = await jdbot.send_message(chat_id, '正在自动检测 cookie 屏蔽情况......')
    path = f'{_ConfigDir}/config.sh'
    with open(path, 'r', encoding='utf-8') as f1:
        configs = f1.readlines()
    del(configs[-1])
    for config in configs:
        if config.find('TempBlockCookie') != -1 and config.find('举例') == -1 and configs[configs.index(config) + 1].find(';;\n') == -1:
            m = re.findall(r'\d', config)
            if m != []:
                for n in m:
                    Expired = checkCookie2(cookies[int(n) - 1])
                    if not Expired:
                        del(m[m.index(n)])
                        await jdbot.edit_message(msg, f'取消临时屏蔽 Cookie{n} 成功')
                if m != []:
                    x = ' '.join(m)
                    configs[configs.index(config)] = f'TempBlockCookie="{x}"\n'
                else:
                    configs[configs.index(config)] = f'TempBlockCookie=""\n'
                    await jdbot.edit_message(msg, '取消屏蔽所有 Cookie 成功')
                with open(path, 'w', encoding='utf-8') as f2:
                        print(''.join(configs), file=f2)
            else:
                print(False)
                await jdbot.edit_message(msg, '没有 Cookie 被临时屏蔽')
        elif config.find('AutoDelCron') != -1:
            break
```
