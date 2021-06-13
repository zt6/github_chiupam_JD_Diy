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
  - [启动user.py文件](#启动userpy文件)
- [常见问题](#常见问题)
- [注意事项](#注意事项)
## 已有功能
### bot.py功能
- [x] 发送 `/start` 指令可开启自定义机器人
- [x] 发送 `/restart` 指令可重启机器人
- [x] 发送 `/help` 指令可获取快捷命令
- [x] 发送 `/install` 指令可拓展功能
- [x] 发送 `/uninstall` 指令可卸载功能
- [x] 发送 `/list` 指令列出已有功能
  - [x] `/upbot` 升级机器人
  - [x] `/checkcookie` 检测过期情况
  - [x] 下载 `.js` `.py` `.sh` 的 `raw` 文件
  - [x] 添加以 `.git` 结尾的仓库链接可添加仓库
  - [x] 发送 `变量名="变量值"` 的格式消息可快捷添加环境变量
  - [x] `/export` 修改环境变量
### user.py功能
- [x] 部署成功后可自动开启 `bot.py` 所有功能
- [x] 监控布道场，关注店铺有礼
- [ ] 监控龙王庙，领取直播间红包
- [x] 监控我的脚本频道，自动更新最新的脚本
- [x] 监控组队瓜分ID频道，自动替换环境变量
## 使用方法
### 启动[bot.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/bot.py)文件
方法一、 在终端中使用 Linux 命令
```
docker exec -it jd bash
cd /jd/jbot/diy
rm -rf bot.py
wget http://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py
pm2 restart jbot
```
方法二、 给机器人发消息（需开启cmd命令功能，且执行完后机器人不会有实际回应，请等待一阵后用 `/start` 查看效果）
```
/cmd cd /jd/jbot/diy && rm -rf bot.py && wget http://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py && pm2 restart jbot
```
### 启动[user.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/user.py)文件
1. 把文件存储在路径 `/jbot/diy/` 下， 或可以开启cmd功能给机器人发消息 `/cmd cd /jd/jbot/diy && wget http://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/user.py`
2. 进入容器，使用命令 `docker exec -it jd bash`
3. 先手动停止机器人，输入命令：`pm2 stop jbot`
4. 手动前台开启机器人，输入命令：`python3 -m jbot`
5. 可能需要输入手机号和 `telegram` 验证码进行登录，如果没有要求输入，请给机器人发送 `/start`，看到机器人回复两条消息后可进行第下一步
6. 按 `Ctrl`+`C` 退出前台运行，然后输入命令 `pm2 start jbot` 启动机器人
## 常见问题
1. Question: 部署 `user.py` 进行到第 5 步没有反应
> Answer: I am worried that you cannot read Chinese, so I will answer you in English. This is because step 5 says that you may need to enter your phone number and telegram verification code to log in. If you are not required to enter it, please send `/start` to the robot. After you see the second message, you can proceed to the next step.
2. Question：部署 `bot.py` 的步骤正确做完后 `/start` 也无法看到两条消息
> Answer：查看 `log/bot/run.log` 的报错自行解决，一般是自己的镜像过老的问题
3. Question：我是青龙用户，部署@￥%%#￥@%
> Answer：我不用青龙，部署有问题请自行解决