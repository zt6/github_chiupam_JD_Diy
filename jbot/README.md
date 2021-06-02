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
5. 如果感觉卡住或要求输入手机号码和验证码后出现登陆成功信息，按 `Ctrl` + `C` 退出前台
6. 最后后台启动机器人，输入命令：`pm2 start jbot`
## 常见问题
1. Question: 发送机器人自带指令没有反应
> Answer: 尝试进入容器后，删除位于 `/jd` 目录下的 `shopbean.session` 文件，然后重新按上述使用方法重新操作
2. Question: 给机器人发送 `/untempblockcookie` 指令会无法取消屏蔽一些没有过期的账号
> Answer: `v4-bot`用户可尝试多发送几次，青龙用户暂不可用
## 已有功能
- 监控布道场，关注店铺有礼
- 监控龙王庙，领取直播间红包
- 发送 `/start` 指令可开启自定义机器人
- 发送 `/restart` 指令可重启机器人
- 发送 `/help` 指令可获取快捷命令
- 发送 `/checkcookie` 指令可临时屏蔽失效 `cookie`
- 监控 `cookie` 过期通知，并及时自动屏蔽
