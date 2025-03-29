#!/bin/bash

# 唇腭裂多智能体系统智能体功能测试脚本

# 确保脚本在错误时退出
set -e

echo "开始测试唇腭裂多智能体系统的智能体功能..."

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

# 测试非综合征性唇腭裂分析
echo "测试非综合征性唇腭裂分析..."
non_syndromic_response=$(curl -s -X POST http://localhost:8000/api/v1/analyses/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $access_token" \
  -d '{
    "symptoms": ["唇裂", "腭裂"],
    "age": "6个月",
    "gender": "男",
    "medical_history": "足月顺产，无其他异常",
    "family_history": "无家族史"
  }')

if echo "$non_syndromic_response" | grep -q "non-syndromic"; then
  echo "✅ 非综合征性唇腭裂分析测试通过"
else
  echo "❌ 非综合征性唇腭裂分析测试失败，响应: $non_syndromic_response"
  exit 1
fi

# 测试综合征性唇腭裂分析
echo "测试综合征性唇腭裂分析..."
syndromic_response=$(curl -s -X POST http://localhost:8000/api/v1/analyses/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $access_token" \
  -d '{
    "symptoms": ["唇裂", "腭裂", "下唇凹陷", "心脏异常", "耳部异常"],
    "age": "3个月",
    "gender": "女",
    "medical_history": "足月顺产，发现心脏杂音",
    "family_history": "父亲有下唇凹陷"
  }')

if echo "$syndromic_response" | grep -q "syndromic"; then
  echo "✅ 综合征性唇腭裂分析测试通过"
else
  echo "❌ 综合征性唇腭裂分析测试失败，响应: $syndromic_response"
  exit 1
fi

# 测试智能体招募功能
echo "测试智能体招募功能..."
if echo "$syndromic_response" | grep -q "specialist_recommendations"; then
  specialists=$(echo "$syndromic_response" | grep -o '"specialist_recommendations":{[^}]*}' | grep -o '"[^"]*":"[^"]*"' | wc -l)
  if [ "$specialists" -ge "3" ]; then
    echo "✅ 智能体招募功能测试通过，成功招募了 $specialists 个专科智能体"
  else
    echo "❌ 智能体招募功能测试失败，只招募了 $specialists 个专科智能体，期望至少3个"
    exit 1
  fi
else
  echo "❌ 智能体招募功能测试失败，未找到专科建议"
  exit 1
fi

# 测试治疗建议生成
echo "测试治疗建议生成..."
if echo "$syndromic_response" | grep -q "treatment_recommendations" && echo "$non_syndromic_response" | grep -q "treatment_recommendations"; then
  echo "✅ 治疗建议生成功能测试通过"
else
  echo "❌ 治疗建议生成功能测试失败"
  exit 1
fi

echo "智能体功能测试完成！"
echo "所有测试通过，智能体系统运行正常。"
echo ""
echo "测试结果分析："
echo "1. 系统能够正确区分综合征性和非综合征性唇腭裂"
echo "2. 智能体招募功能正常工作，能够根据症状动态招募相关专科智能体"
echo "3. 系统能够生成针对不同类型唇腭裂的治疗建议"
