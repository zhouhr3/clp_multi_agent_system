#!/bin/bash

# 唇腭裂多智能体系统权限设置脚本

# 确保脚本在错误时退出
set -e

echo "设置文件权限..."

# 设置脚本可执行权限
chmod +x deploy.sh
chmod +x init_data.sh

# 设置数据目录权限
mkdir -p ./data
chmod 777 ./data

# 设置日志目录权限
mkdir -p ./logs
chmod 777 ./logs

echo "权限设置完成！"
