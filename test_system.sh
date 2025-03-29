#!/bin/bash

# 唇腭裂多智能体系统测试脚本

# 确保脚本在错误时退出
set -e

echo "开始测试唇腭裂多智能体系统..."

# 检查容器是否运行
backend_status=$(docker-compose ps | grep backend | grep -c "Up" || echo "0")
frontend_status=$(docker-compose ps | grep frontend | grep -c "Up" || echo "0")

if [ "$backend_status" -ne "1" ] || [ "$frontend_status" -ne "1" ]; then
  echo "系统未完全运行，请先执行部署脚本"
  exit 1
fi

# 测试后端健康状态
echo "测试后端健康状态..."
health_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$health_status" -eq "200" ]; then
  echo "✅ 后端健康状态检查通过"
else
  echo "❌ 后端健康状态检查失败，HTTP状态码: $health_status"
  exit 1
fi

# 测试API根端点
echo "测试API根端点..."
api_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1)
if [ "$api_status" -eq "200" ] || [ "$api_status" -eq "404" ]; then
  echo "✅ API根端点测试通过"
else
  echo "❌ API根端点测试失败，HTTP状态码: $api_status"
  exit 1
fi

# 测试用户登录
echo "测试用户登录..."
login_response=$(curl -s -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=doctor@example.com&password=doctor123")

if echo "$login_response" | grep -q "access_token"; then
  echo "✅ 用户登录测试通过"
  # 提取访问令牌
  access_token=$(echo "$login_response" | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')
else
  echo "❌ 用户登录测试失败，响应: $login_response"
  exit 1
fi

# 测试获取当前用户信息
echo "测试获取当前用户信息..."
user_response=$(curl -s -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $access_token")

if echo "$user_response" | grep -q "doctor@example.com"; then
  echo "✅ 获取用户信息测试通过"
else
  echo "❌ 获取用户信息测试失败，响应: $user_response"
  exit 1
fi

# 测试获取治疗指南
echo "测试获取治疗指南..."
guidelines_response=$(curl -s -X GET http://localhost:8000/api/v1/treatment-guidelines \
  -H "Authorization: Bearer $access_token")

if echo "$guidelines_response" | grep -q "CLP_NONSYNDROMIC" && echo "$guidelines_response" | grep -q "CLP_SYNDROMIC"; then
  echo "✅ 获取治疗指南测试通过"
else
  echo "❌ 获取治疗指南测试失败，响应: $guidelines_response"
  exit 1
fi

# 测试前端可访问性
echo "测试前端可访问性..."
frontend_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$frontend_status" -eq "200" ]; then
  echo "✅ 前端可访问性测试通过"
else
  echo "❌ 前端可访问性测试失败，HTTP状态码: $frontend_status"
  exit 1
fi

echo "基本功能测试完成！"
echo "所有测试通过，系统运行正常。"
echo ""
echo "您可以通过以下地址访问系统："
echo "  前端应用：http://localhost:3000"
echo "  后端API：http://localhost:8000"
echo ""
echo "使用以下账户登录："
echo "  管理员：admin@example.com / admin123"
echo "  医生：doctor@example.com / doctor123"
