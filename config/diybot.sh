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
    diybot_md5sum_old=$(cd $dir_diy; find . -type f \( ! -name "user.*" \) | xargs md5sum)
    git_pull_scripts ${repo_path} "master"
    cp -rf $repo_path/jbot/. $dir_diy
    diybot_md5sum_new=$(cd $dir_diy; find . -type f \( ! -name "user.*" \) | xargs md5sum)
else
  git_clone_scripts ${url} ${repo_path} "master"
  cp -rf $repo_path/jbot/. $dir_diy
fi