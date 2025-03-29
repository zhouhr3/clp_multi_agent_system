#!/bin/bash

# 唇腭裂多智能体系统 AutoDL 部署脚本
# 此脚本专为 AutoDL 环境优化，提供一键式部署体验

# 确保脚本在错误时退出
set -e

echo "====================================================="
echo "  唇腭裂多智能体系统 AutoDL 部署脚本"
echo "====================================================="
echo ""

# 检查是否在 AutoDL 环境中
if [ ! -d "/root/autodl-tmp" ]; then
  echo "警告: 未检测到 AutoDL 环境，但将继续执行"
fi

# 创建工作目录
WORK_DIR="/root/cleft_multi_agent_system"
mkdir -p $WORK_DIR
cd $WORK_DIR

echo "步骤 1: 安装必要的依赖..."
apt-get update
apt-get install -y docker.io docker-compose python3-pip unzip curl wget

# 启动 Docker 服务
systemctl start docker
systemctl enable docker

echo "步骤 2: 创建数据和日志目录..."
mkdir -p ./data
mkdir -p ./logs
chmod 777 ./data
chmod 777 ./logs

echo "步骤 3: 配置环境变量..."
cat > .env << EOL
# 应用设置
APP_NAME=唇腭裂多智能体系统
API_V1_STR=/api/v1

# 安全设置
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24小时

# 数据库设置
DATABASE_URL=sqlite:////data/cleft_multi_agent.db

# CORS设置
CORS_ORIGINS=*

# 外部API设置
OPENAI_API_KEY=sk-your-openai-api-key
PUBMED_API_KEY=your-pubmed-api-key
EOL

cp .env ./backend/.env

echo "步骤 4: 构建并启动 Docker 容器..."
docker-compose up -d --build

echo "步骤 5: 等待服务启动..."
sleep 15

echo "步骤 6: 初始化系统数据..."
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

# 获取 AutoDL 实例的公网 IP
PUBLIC_IP=$(curl -s ifconfig.me)

echo "步骤 7: 配置端口映射..."
# 在 AutoDL 中，我们需要将容器端口映射到主机端口
docker-compose down
sed -i 's/8000:8000/8000:8000/g' docker-compose.yml
sed -i 's/3000:80/80:80/g' docker-compose.yml
docker-compose up -d

echo "步骤 8: 测试系统是否正常运行..."
# 测试后端健康状态
health_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$health_status" -eq "200" ]; then
  echo "✅ 后端健康状态检查通过"
else
  echo "❌ 后端健康状态检查失败，HTTP状态码: $health_status"
  echo "请检查日志: docker-compose logs backend"
fi

# 测试前端可访问性
frontend_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80)
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
echo "  前端应用：http://$PUBLIC_IP"
echo "  后端API：http://$PUBLIC_IP:8000"
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
