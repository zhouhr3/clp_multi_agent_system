#!/bin/bash

# 唇腭裂多智能体系统性能测试脚本

# 确保脚本在错误时退出
set -e

echo "开始性能测试唇腭裂多智能体系统..."

# 检查是否安装了必要的工具
if ! command -v ab &> /dev/null; then
    echo "未安装Apache Benchmark (ab)工具，正在安装..."
    apt-get update && apt-get install -y apache2-utils
fi

# 检查容器是否运行
backend_status=$(docker-compose ps | grep backend | grep -c "Up" || echo "0")
if [ "$backend_status" -ne "1" ]; then
  echo "后端系统未运行，请先执行部署脚本"
  exit 1
fi

# 获取访问令牌
echo "获取访问令牌..."
login_response=$(curl -s -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=doctor@example.com&password=doctor123")

access_token=$(echo "$login_response" | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')

if [ -z "$access_token" ]; then
  echo "获取访问令牌失败，无法继续测试"
  exit 1
fi

# 创建临时文件存储令牌
token_file=$(mktemp)
echo "Authorization: Bearer $access_token" > "$token_file"

echo "开始API性能测试..."

# 测试健康检查端点性能
echo "测试健康检查端点性能..."
ab -n 100 -c 10 http://localhost:8000/health

# 测试获取用户信息端点性能
echo "测试获取用户信息端点性能..."
ab -n 50 -c 5 -H "Authorization: Bearer $access_token" http://localhost:8000/api/v1/users/me

# 测试获取治疗指南端点性能
echo "测试获取治疗指南端点性能..."
ab -n 50 -c 5 -H "Authorization: Bearer $access_token" http://localhost:8000/api/v1/treatment-guidelines

# 清理临时文件
rm "$token_file"

echo "性能测试完成！"
echo ""
echo "性能测试结果分析："
echo "1. 健康检查端点：应该能够处理每秒至少100个请求"
echo "2. 用户信息端点：应该能够处理每秒至少50个请求"
echo "3. 治疗指南端点：应该能够处理每秒至少50个请求"
echo ""
echo "如果任何测试未达到预期性能，请考虑优化数据库查询或增加服务器资源"
