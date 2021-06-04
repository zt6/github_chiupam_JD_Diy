<h1 align="center">
  自启机器人
  <br>
  Author: chiupam
</h1>

## 简介
随着 v4-bot 启动而启动的自定义机器人。
## 目录
- [简介](#简介)
- [目录](#目录)
- [已有功能](#已有功能)
  - [bot.py功能](#botpy功能)
  - [user.py功能](#userpy功能)
- [使用方式](#使用方式)
  - [启动bot.py文件](#启动botpy文件)
  - [部署bot.py快捷命令](#部署botpy快捷命令)
  - [启动user.py文件](#启动userpy文件)
- [常见问题](#常见问题)
- [注意事项](#注意事项)
## 已有功能
### bot.py功能
- [x] 发送 `/start` 指令可开启自定义机器人
- [x] 发送 `/restart` 指令可重启机器人
- [x] 发送 `/help` 指令可获取快捷命令
- [x] 发送 `/checkcookie` 指令可临时屏蔽失效 `cookie`
- [x] 监控 `cookie` 过期通知，并及时自动屏蔽
- [x] 监控到用户发送了 `raw` 链接时下载文件并选择对文件进行操作 
### user.py功能
- [x] 监控布道场，关注店铺有礼
- [ ] 监控龙王庙，领取直播间红包
## 使用方法
### 启动[bot.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/bot.py)文件
1. 把文件存储在路径 `/jbot/diy/` 下，如果没有此路径请重新映射出来
2. 进入容器，使用命令 `docker exec -it jd bash`
3. 输入命令 `pm2 restart jbot` 重启机器人即可
### 部署bot.py快捷命令
```
docker exec -it jd bash
wget -p /jd/jbot/diy -O bot.py https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py
pm2 restart jbot
```
### 启动[user.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/user.py)文件
1. 把文件存储在路径 `/jbot/diy/` 下，如果没有此路径请重新映射出来
2. 进入容器，使用命令 `docker exec -it jd bash`
3. 先手动停止机器人，输入命令：`pm2 stop jbot`
4. 手动前台开启机器人，输入命令：`python3 -m jbot`
5. (1) 如果卡住，请给机器人发送 `/start` 测试一下；(2) 如果需要登录，请登录
6. 按 `Ctrl`+`C` 退出前台运行，然后输入命令 `pm2 start jbot` 启动机器人
## 常见问题
1. Question: 使用 `user.py` 后发送机器人自带指令没有反应
> Answer: 尝试进入容器后，删除位于 `/jd` 目录下的 `diy.session` 文件，然后重新按上述使用方法重新操作
## 注意事项
- 如果有使用旧的[diy.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/backup/diy.py)请删除后再使用以上两个脚本，因为大部分功能重复
- 首次使用[bot.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/bot.py)需要按说明登录 `telegram`，因为 `.session` 文件名已经修改
