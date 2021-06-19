#!/usr/bin/env bash
# 从 whyour 大佬的 bot.sh 与 E大 的 jup.sh 与 SuMaiKaDe 大佬的 bot.sh 拼凑出来
## 导入通用变量与函数
if [ ! -d "/ql" ];then
  dir_root=/jd
else
  dir_root=/ql
fi
dir_diy=$dir_root/jbot/diy
dir_repo=$dir_root/repo
url="https://github.com/chiupam/JD_Diy.git"
repo_path="${dir_repo}/diybot"
user_file="${dir_root}/jbot/diy/user.py"

git_pull_scripts() {
  local dir_current=$(pwd)
  local dir_work="$1"
  local branch="$2"
  [[ $branch ]] && local cmd="origin/${branch}"
  cd $dir_work
  echo -e "开始更新仓库：$dir_work\n"
  git fetch --all
  exit_status=$?
  git reset --hard $cmd
  git pull
  cd $dir_current
}

git_clone_scripts() {
  local url=$1
  local dir=$2
  local branch=$3
  [[ $branch ]] && local cmd="-b $branch "
  echo -e "开始克隆仓库 $url 到 $dir\n"
  git clone $cmd $url $dir
  exit_status=$?
}
if [ -d ${repo_path}/.git ]; then
  echo -e "1、下载diybot仓库文件\n"
  git_pull_scripts ${repo_path} "master"
  cp -rf $repo_path/jbot/. $dir_diy
  rm -rf $dir_diy/user.py
else
  echo -e "1、更新diybot仓库文件\n"
  git_clone_scripts ${url} ${repo_path} "master"
  cd $dir_diy
  if [ ! -f "$user_file" ]; then
    echo -e "没有部署user.py文件\n"
    cp -rf $repo_path/jbot/. $dir_diy
    rm -rf $dir_diy/user.py
  else
    echo -e "已部署了user.py文件\n"
    cp -rf $repo_path/jbot/. $dir_diy
  fi
fi
echo -e "2、启动bot程序...\n"
cd $dir_root
if [ -d "/ql" ]; then
  ps -ef | grep "python3 -m jbot" | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null
  nohup python3 -m jbot >$dir_root/log/bot/bot.log 2>&1 &
  echo -e "bot启动成功...\n"
else
  cd $dir_root
  pm2 restart jbot
  echo -e "bot启动成功...\n"
fi
exit 0