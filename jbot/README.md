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
1.Qus1: 发送指令没有反应
  Ans: 尝试进入容器后，删除位于 `/jd` 目录下的 `shopbean.session` 文件，然后重新按上述使用方法重新操作
2. Qus2：给机器人发送 `/untempblockcookie` 指令会无法取消屏蔽一些没有过期的账号
  Ans: 尝试多发送几次
## 已有功能
- 监控布道场，关注有礼
- 监控龙王庙，领取直播间红包
- 发送 `/checkcookie` 指令可临时屏蔽失效 `cookie`
- 发送 `/untempblockcookie` 指令可取消屏蔽 `cookie`

