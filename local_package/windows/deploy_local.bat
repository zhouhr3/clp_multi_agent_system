@echo off
echo ===================================================
echo   唇腭裂多智能体系统本地部署脚本 (Windows版)
echo ===================================================
echo.

REM 检查Docker是否已安装
docker --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Docker未安装或未正确配置。
    echo 请先安装Docker Desktop，然后再运行此脚本。
    echo 您可以从Docker官网下载：https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM 检查Docker是否正在运行
docker info > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Docker未运行。请启动Docker Desktop后再运行此脚本。
    pause
    exit /b 1
)

echo 步骤 1: 准备部署环境...
if not exist data mkdir data
if not exist logs mkdir logs

echo 步骤 2: 配置环境变量...
echo # 应用设置 > .env
echo APP_NAME=唇腭裂多智能体系统 >> .env
echo API_V1_STR=/api/v1 >> .env
echo. >> .env
echo # 安全设置 >> .env
echo SECRET_KEY=local_development_secret_key_please_change_in_production >> .env
echo ALGORITHM=HS256 >> .env
echo ACCESS_TOKEN_EXPIRE_MINUTES=1440 >> .env
echo. >> .env
echo # 数据库设置 >> .env
echo DATABASE_URL=sqlite:///./data/cleft_multi_agent.db >> .env
echo. >> .env
echo # CORS设置 >> .env
echo CORS_ORIGINS=* >> .env
echo. >> .env
echo # 外部API设置 >> .env
echo OPENAI_API_KEY=sk-your-openai-api-key >> .env
echo PUBMED_API_KEY=your-pubmed-api-key >> .env

copy .env backend\.env

echo 步骤 3: 构建并启动Docker容器...
docker-compose up -d --build

echo 步骤 4: 等待服务启动...
timeout /t 15 /nobreak > nul

echo 步骤 5: 初始化系统数据...
docker-compose exec -T backend python -c "from utils.database import get_db_session; from models.user import User; from utils.auth import get_password_hash; with get_db_session() as db: admin = db.query(User).filter(User.email == 'admin@example.com').first(); if not admin: admin = User(email='admin@example.com', hashed_password=get_password_hash('admin123'), full_name='系统管理员', role='admin'); db.add(admin); print('管理员用户已创建'); else: print('管理员用户已存在')"

docker-compose exec -T backend python -c "from utils.database import get_db_session; from models.user import User; from utils.auth import get_password_hash; with get_db_session() as db: doctor = db.query(User).filter(User.email == 'doctor@example.com').first(); if not doctor: doctor = User(email='doctor@example.com', hashed_password=get_password_hash('doctor123'), full_name='唇腭裂专科医生', role='doctor'); db.add(doctor); print('医生用户已创建'); else: print('医生用户已存在')"

echo 步骤 6: 测试系统是否正常运行...
curl -s -o nul -w "%%{http_code}" http://localhost:8000/health > temp.txt
set /p health_status=<temp.txt
del temp.txt

if "%health_status%"=="200" (
    echo ✓ 后端健康状态检查通过
) else (
    echo ✗ 后端健康状态检查失败，HTTP状态码: %health_status%
    echo 请检查日志: docker-compose logs backend
)

curl -s -o nul -w "%%{http_code}" http://localhost:3000 > temp.txt
set /p frontend_status=<temp.txt
del temp.txt

if "%frontend_status%"=="200" (
    echo ✓ 前端可访问性测试通过
) else (
    echo ✗ 前端可访问性测试失败，HTTP状态码: %frontend_status%
    echo 请检查日志: docker-compose logs frontend
)

echo.
echo ===================================================
echo   部署完成！
echo ===================================================
echo.
echo 您可以通过以下地址访问系统：
echo   前端应用：http://localhost:3000
echo   后端API：http://localhost:8000
echo.
echo 使用以下账户登录：
echo   管理员：admin@example.com / admin123
echo   医生：doctor@example.com / doctor123
echo.
echo 如需查看日志，请使用以下命令：
echo   docker-compose logs -f backend
echo   docker-compose logs -f frontend
echo.
echo 如需停止系统，请使用以下命令：
echo   docker-compose down
echo.
echo 如需重启系统，请使用以下命令：
echo   docker-compose up -d
echo.
echo 感谢您使用唇腭裂多智能体系统！
echo.

start http://localhost:3000

pause
