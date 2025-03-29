#!/bin/bash

# 唇腭裂多智能体系统部署脚本

# 确保脚本在错误时退出
set -e

echo "开始部署唇腭裂多智能体系统..."

# 创建数据目录
mkdir -p ./data
echo "数据目录已创建"

# 检查环境变量文件
if [ ! -f ./backend/.env ]; then
  echo "环境变量文件不存在，从示例文件创建..."
  cp ./backend/.env.example ./backend/.env
  echo "请编辑 ./backend/.env 文件，填入正确的配置值"
  exit 1
fi

# 构建并启动容器
echo "构建并启动Docker容器..."
docker-compose up -d --build

echo "等待服务启动..."
sleep 10

# 检查服务是否正常运行
backend_status=$(docker-compose ps | grep backend | grep -c "Up" || echo "0")
frontend_status=$(docker-compose ps | grep frontend | grep -c "Up" || echo "0")

if [ "$backend_status" -eq "1" ] && [ "$frontend_status" -eq "1" ]; then
  echo "部署成功！"
  echo "后端API地址: http://localhost:8000"
  echo "前端应用地址: http://localhost:3000"
else
  echo "部署失败，请检查日志:"
  docker-compose logs
  exit 1
fi

echo "您可以使用以下命令查看日志:"
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f frontend"

echo "部署完成！"
