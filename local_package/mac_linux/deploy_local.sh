#!/bin/bash

# 唇腭裂多智能体系统本地部署脚本 (Mac/Linux版)

# 确保脚本在错误时退出
set -e

echo "====================================================="
echo "  唇腭裂多智能体系统本地部署脚本 (Mac/Linux版)"
echo "====================================================="
echo ""

# 检查Docker是否已安装
if ! command -v docker &> /dev/null; then
    echo "Docker未安装或未正确配置。"
    echo "请先安装Docker，然后再运行此脚本。"
    echo "您可以从Docker官网获取安装指南：https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查Docker是否正在运行
if ! docker info &> /dev/null; then
    echo "Docker未运行。请启动Docker服务后再运行此脚本。"
    exit 1
fi

echo "步骤 1: 准备部署环境..."
mkdir -p ./data
mkdir -p ./logs
chmod 777 ./data
chmod 777 ./logs

echo "步骤 2: 配置环境变量..."
cat > .env << EOL
# 应用设置
APP_NAME=唇腭裂多智能体系统
API_V1_STR=/api/v1

# 安全设置
SECRET_KEY=local_development_secret_key_please_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24小时

# 数据库设置
DATABASE_URL=sqlite:///./data/cleft_multi_agent.db

# CORS设置
CORS_ORIGINS=*

# 外部API设置
OPENAI_API_KEY=sk-your-openai-api-key
PUBMED_API_KEY=your-pubmed-api-key
EOL

cp .env ./backend/.env

echo "步骤 3: 构建并启动Docker容器..."
docker-compose up -d --build

echo "步骤 4: 等待服务启动..."
sleep 15

echo "步骤 5: 初始化系统数据..."
docker-compose exec -T backend python -c "
from utils.database import get_db_session
from models.user import User
from utils.auth import get_password_hash

with get_db_session() as db:
    # 检查是否已存在管理员
    admin = db.query(User).filter(User.email == 'admin@example.com').first()
    if not admin:
        admin = User(
            email='admin@example.com',
            hashed_password=get_password_hash('admin123'),
            full_name='系统管理员',
            role='admin'
        )
        db.add(admin)
        print('管理员用户已创建')
    else:
        print('管理员用户已存在')
"

docker-compose exec -T backend python -c "
from utils.database import get_db_session
from models.user import User
from utils.auth import get_password_hash

with get_db_session() as db:
    # 检查是否已存在医生
    doctor = db.query(User).filter(User.email == 'doctor@example.com').first()
    if not doctor:
        doctor = User(
            email='doctor@example.com',
            hashed_password=get_password_hash('doctor123'),
            full_name='唇腭裂专科医生',
            role='doctor'
        )
        db.add(doctor)
        print('医生用户已创建')
    else:
        print('医生用户已存在')
"

echo "步骤 6: 测试系统是否正常运行..."
# 测试后端健康状态
health_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$health_status" -eq "200" ]; then
  echo "✅ 后端健康状态检查通过"
else
  echo "❌ 后端健康状态检查失败，HTTP状态码: $health_status"
  echo "请检查日志: docker-compose logs backend"
fi

# 测试前端可访问性
frontend_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$frontend_status" -eq "200" ]; then
  echo "✅ 前端可访问性测试通过"
else
  echo "❌ 前端可访问性测试失败，HTTP状态码: $frontend_status"
  echo "请检查日志: docker-compose logs frontend"
fi

echo ""
echo "====================================================="
echo "  部署完成！"
echo "====================================================="
echo ""
echo "您可以通过以下地址访问系统："
echo "  前端应用：http://localhost:3000"
echo "  后端API：http://localhost:8000"
echo ""
echo "使用以下账户登录："
echo "  管理员：admin@example.com / admin123"
echo "  医生：doctor@example.com / doctor123"
echo ""
echo "如需查看日志，请使用以下命令："
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f frontend"
echo ""
echo "如需停止系统，请使用以下命令："
echo "  docker-compose down"
echo ""
echo "如需重启系统，请使用以下命令："
echo "  docker-compose up -d"
echo ""
echo "感谢您使用唇腭裂多智能体系统！"

# 尝试打开浏览器
if command -v xdg-open &> /dev/null; then
  xdg-open http://localhost:3000 &
elif command -v open &> /dev/null; then
  open http://localhost:3000 &
fi
