#!/usr/bin/env bash

if [ -d "/jd" ]; then
  root=/jd
else
  root=/ql
fi

dir_jbot=$root/jbot
dir_diy=$dir_jbot/diy
dir_repo=$root/repo
url="https://raw.githubusercontent.com/chiupam/JD_Diy/master/jbot/user.py"

stop() {
  cd $root
  if [ -d "/jd" ]
    then pm2 stop jbot
  else
    ps -ef | grep "python3 -m jbot" | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null
  fi
}

restart() {
  cd $root
  if [ -d "/jd" ]
    then pm2 restart jbot
  else
    nohup python3 -m jbot > /ql/log/bot/bot.log 2>&1 &
  fi
}

tip() {
  echo "登陆完成后使用 Ctrl + C 退出脚本，并使用以下命令启动 user 监控"
  echo ""
  if [ -d "/jd" ]
    then echo "cd $dir_jbot;pm2 restart jbot"
  else
    echo "cd $dir_jbot;nohup python3 -m jbot > /ql/log/bot/bot.log 2>&1 &"
  fi
}

install() {
  stop
  cd $root/jbot/diy
  wget $url
  tip
  python3 -m jbot
}

uninstall() {
  cd $root/jbot/diy
  rm -f "user.py"
  cd $root
  rm -f "user.session"
  rm -f "user.session-journal"
}

update() {
  stop
  cd $root/jbot/diy
  rm -f "user.py"
  wget $url
  restart
}

reinstall() {
  stop
  cd $root/jbot/diy
  rm -f "user.py"
  wget $url
  tip
  python3 -m jbot
}

relogin() {
  stop
  cd $root
  rm -f "user.session"
  rm -f "user.session-journal"
  tip
  python3 -m jbot
}

main() {
    echo "请选择您需要进行的操作:"
    echo "  1) 安装 user"
    echo "  2) 卸载 user"
    echo "  3) 更新 user"
    echo "  4) 重新安装 user"
    echo "  5) 重新登陆 user"
    echo "  6) 退出脚本"
    echo ""
    echo -n "请输入编号: "
    read N
    case $N in
    1) install ;;
    2) uninstall ;;
    3) update ;;
    4) reinstall ;;
    5) relogin ;;
    6) exit ;;
    *) echo "输入错误！请重新 bash user.sh 启动脚本" ;;
    esac
}

main