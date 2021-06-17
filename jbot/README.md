<h1 align="center">
  自启机器人
  <br>
  Author: chiupam
</h1>

## 简介
随着 v4-bot 启动而启动的自定义机器人，其中大部分功能亦支持青龙用户。
## 目录
- [简介](#简介)
- [目录](#目录)
- [已有功能](#已有功能)
  - [bot.py功能](#botpy功能)
  - [bot.py可拓展功能](#botpy可拓展功能)
  - [user.py功能](#userpy功能)
- [使用方式](#使用方式)
  - [V4BOT用户部署bot.py](#v4bot用户部署botpy)
  - [青龙用户部署bot.py](#青龙用户部署botpy)
  - [V4BOT用户部署user.py](#v4bot用户部署userpy)
  - [青龙用户部署user.py](#青龙用户部署userpy)
## 已有功能
### bot.py功能
- [x] 发送 `/start` 指令可开启自定义机器人
- [x] 发送 `/restart` 指令可重启机器人
- [x] 发送 `/help` 指令可获取快捷命令
- [x] 发送 `/install` 指令可拓展功能
- [x] 发送 `/uninstall` 指令可卸载功能
- [x] 发送 `/list` 指令列出已有功能
### bot.py可拓展功能
- [x] 发送 `/upbot` 升级机器人
- [x] 发送 `/checkcookie` 检测过期情况
- [x] 发送`/export` 修改环境变量
- [x] 下载 `.js` `.py` `.sh` 的 `raw` 文件
- [x] 添加以 `.git` 结尾的仓库链接可添加仓库（暂不支持青龙用户）
- [x] 发送 `变量名="变量值"` 的格式消息可快捷添加环境变量
### user.py功能
- [x] 部署成功后可自动开启 `bot.py` 所有功能
- [x] 监控布道场，关注店铺有礼
- [x] 监控我的脚本频道，自动更新最新的脚本
- [x] 监控组队瓜分ID频道，自动替换环境变量
## 使用方法
### V4BOT用户部署[bot.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/bot.py)
#### 方法一、 在终端中使用命令
```
docker exec -it jd bash && cd /jd/jbot/diy && rm -rf bot.py && wget http://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py && pm2 restart jbot
```
#### 方法二、 给机器人发消息
```
/cmd cd /jd/jbot/diy && rm -rf bot.py && wget http://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py && pm2 restart jbot
```
#### 方法三、在终端中手动存储文件
1. 把文件存储在路径 `/jbot/diy/` 下
2. 重启机器人，输入命令：`pm2 restart jbot`
### 青龙用户部署[bot.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/bot.py)
#### 方法一、 在终端中使用命令
```
docker exec -it qinglong bash && cd /ql/jbot/diy && rm -rf bot.py && wget http://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py && ql bot
```
#### 方法二、 给机器人发消息
```
/cmd cd /ql/jbot/diy && rm -rf bot.py && wget http://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py && ql bot
```
#### 方法三、在终端中手动存储文件
1. 把文件存储在路径 `/jbot/diy/` 下
2. 重启机器人，输入命令：`ql bot`
### V4BOT用户部署[user.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/user.py)
1. 把文件存储在路径 `/jbot/diy/` 下
2. 进入容器，使用命令 `docker exec -it jd bash`
3. 先手动停止机器人，输入命令：`pm2 stop jbot`
4. 为了避免不必要的麻烦，输入命令：`rm -rf user.session`
5. 手动前台开启机器人，输入命令：`python3 -m jbot`
6. 输入手机号和 `telegram` 验证码进行登录后按 `Ctrl`+`C` 退出前台运行
7. 后台挂起机器人，输入命令 `pm2 start jbot` 
### 青龙用户部署[user.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/user.py)
1. 把文件存储在路径 `/jbot/diy/` 下
2. 进入容器，使用命令 `docker exec -it qinglong bash`
3. 先手动停止机器人，输入命令：`pm2 stop jbot`
4. 为了避免不必要的麻烦，输入命令：`rm -rf user.session`
5. 手动前台开启机器人，输入命令：`python3 -m jbot`
6. 输入手机号和 `telegram` 验证码进行登录后按 `Ctrl`+`C` 退出前台运行
7. 重启机器人，输入命令 `ql bot` 