#!/bin/bash

# 添加所有更改
git add .

# 获取当前时间作为提交信息
commit_message="+++$(date '+%Y-%m-%d %H:%M:%S')"

# 提交更改
git commit -m "$commit_message"

# 推送到远程仓库
git push