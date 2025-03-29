#!/bin/bash

# 唇腭裂多智能体系统演示环境部署脚本

# 确保脚本在错误时退出
set -e

echo "====================================================="
echo "  唇腭裂多智能体系统演示环境部署脚本"
echo "====================================================="
echo ""

# 创建工作目录
DEMO_DIR="/home/ubuntu/cleft_multi_agent_system/demo_environment"
mkdir -p $DEMO_DIR
cd $DEMO_DIR

echo "步骤 1: 准备演示环境配置..."
mkdir -p ./data
mkdir -p ./logs
chmod 777 ./data
chmod 777 ./logs

# 复制必要的文件
cp -r /home/ubuntu/cleft_multi_agent_system/backend ./
cp -r /home/ubuntu/cleft_multi_agent_system/frontend ./
cp /home/ubuntu/cleft_multi_agent_system/docker-compose.yml ./

# 修改docker-compose.yml文件，添加演示环境特定配置
sed -i 's/8000:8000/8080:8000/g' docker-compose.yml
sed -i 's/3000:80/8081:80/g' docker-compose.yml

echo "步骤 2: 配置演示环境变量..."
cat > .env << EOL
# 应用设置
APP_NAME=唇腭裂多智能体系统演示版
API_V1_STR=/api/v1
DEMO_MODE=true

# 安全设置
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24小时

# 数据库设置
DATABASE_URL=sqlite:////data/cleft_multi_agent_demo.db

# CORS设置
CORS_ORIGINS=*

# 外部API设置
OPENAI_API_KEY=sk-your-openai-api-key
PUBMED_API_KEY=your-pubmed-api-key
EOL

cp .env ./backend/.env

echo "步骤 3: 创建演示用Dockerfile..."
cat > backend/Dockerfile << EOL
FROM python:3.10-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p /data

# 设置演示模式环境变量
ENV DEMO_MODE=true

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

# 修改前端配置，添加演示模式标识
cat > frontend/public/demo-config.js << EOL
window.DEMO_MODE = true;
window.DEMO_RESET_INTERVAL = 86400; // 24小时重置
window.DEMO_VERSION = "1.0.0";
window.DEMO_NOTICE = "这是唇腭裂多智能体系统的演示版本，数据将每24小时自动重置。";
EOL

# 修改前端Dockerfile，包含演示配置
cat > frontend/Dockerfile << EOL
FROM node:16-alpine as build

WORKDIR /app

# 复制依赖文件
COPY package.json package-lock.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

# 添加演示模式标识
RUN echo "REACT_APP_DEMO_MODE=true" > .env

# 构建应用
RUN npm run build

# 生产环境
FROM nginx:alpine

# 复制构建产物到Nginx目录
COPY --from=build /app/build /usr/share/nginx/html

# 复制演示配置
COPY public/demo-config.js /usr/share/nginx/html/

# 复制Nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
EOL

echo "步骤 4: 创建演示数据初始化脚本..."
cat > init_demo_data.py << EOL
#!/usr/bin/env python3
"""
唇腭裂多智能体系统演示数据初始化脚本
"""
import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
import hashlib

# 创建数据库连接
db_path = "/data/cleft_multi_agent_demo.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建用户表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 创建患者表
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age TEXT NOT NULL,
    gender TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    medical_history TEXT,
    family_history TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users (id)
)
''')

# 创建分析结果表
cursor.execute('''
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    cleft_type TEXT NOT NULL,
    syndrome_type TEXT NOT NULL,
    specialist_recommendations TEXT,
    treatment_recommendations TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients (id),
    FOREIGN KEY (created_by) REFERENCES users (id)
)
''')

# 创建治疗指南表
cursor.execute('''
CREATE TABLE IF NOT EXISTS treatment_guidelines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    condition_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    cleft_type TEXT NOT NULL,
    syndrome_type TEXT NOT NULL,
    age_group TEXT,
    treatment_steps TEXT NOT NULL,
    specialist_involvement TEXT,
    follow_up_protocol TEXT,
    evidence_level TEXT,
    references TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users (id)
)
''')

# 简单的密码哈希函数
def get_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 创建演示用户
demo_users = [
    {
        "email": "admin@example.com",
        "password": "demo123",
        "full_name": "系统管理员",
        "role": "admin"
    },
    {
        "email": "doctor@example.com",
        "password": "demo123",
        "full_name": "唇腭裂专科医生",
        "role": "doctor"
    }
]

for user in demo_users:
    cursor.execute(
        "INSERT OR REPLACE INTO users (email, hashed_password, full_name, role) VALUES (?, ?, ?, ?)",
        (user["email"], get_password_hash(user["password"]), user["full_name"], user["role"])
    )

# 获取医生用户ID
cursor.execute("SELECT id FROM users WHERE email = ?", ("doctor@example.com",))
doctor_id = cursor.fetchone()[0]

# 创建演示治疗指南
demo_guidelines = [
    {
        "condition_id": "CLP_NONSYNDROMIC",
        "title": "非综合征性唇腭裂治疗指南",
        "description": "针对非综合征性唇腭裂患者的标准治疗方案",
        "cleft_type": "CLP",
        "syndrome_type": "non-syndromic",
        "age_group": "infant",
        "treatment_steps": json.dumps({
            "0-3个月": "评估和喂养指导",
            "3-6个月": "唇裂修复手术",
            "9-18个月": "腭裂修复手术",
            "2-5岁": "语音评估和治疗",
            "5-7岁": "牙齿和颌骨评估",
            "8-12岁": "牙齿矫正和骨移植",
            "16-18岁": "最终整形手术"
        }),
        "specialist_involvement": json.dumps({
            "整形外科医生": "唇裂和腭裂修复手术",
            "语言治疗师": "语音评估和治疗",
            "牙医和正畸医生": "牙齿和颌骨评估与治疗",
            "耳鼻喉科医生": "听力评估",
            "遗传咨询师": "家族遗传风险评估"
        }),
        "follow_up_protocol": json.dumps({
            "手术后": "每周一次，持续一个月",
            "1-5岁": "每3个月一次",
            "5-12岁": "每6个月一次",
            "12岁以上": "每年一次"
        }),
        "evidence_level": "A",
        "references": json.dumps([
            "American Cleft Palate-Craniofacial Association. Parameters for evaluation and treatment of patients with cleft lip/palate or other craniofacial anomalies. Cleft Palate-Craniofacial Journal, 2018.",
            "World Health Organization. Global strategies to reduce the health-care burden of craniofacial anomalies. Geneva: WHO, 2020."
        ]),
        "created_by": doctor_id
    },
    {
        "condition_id": "CLP_SYNDROMIC",
        "title": "综合征性唇腭裂治疗指南",
        "description": "针对综合征性唇腭裂患者的综合治疗方案",
        "cleft_type": "CLP",
        "syndrome_type": "syndromic",
        "age_group": "infant",
        "treatment_steps": json.dumps({
            "出生后": "综合评估和遗传检测",
            "0-3个月": "喂养指导和呼吸管理",
            "3-6个月": "唇裂修复手术",
            "9-18个月": "腭裂修复手术",
            "2-5岁": "语音评估和治疗",
            "5-7岁": "牙齿和颌骨评估",
            "8-12岁": "牙齿矫正和骨移植",
            "12-18岁": "综合征相关并发症管理",
            "16-18岁": "最终整形手术"
        }),
        "specialist_involvement": json.dumps({
            "整形外科医生": "唇裂和腭裂修复手术",
            "遗传学专家": "综合征诊断和管理",
            "语言治疗师": "语音评估和治疗",
            "牙医和正畸医生": "牙齿和颌骨评估与治疗",
            "耳鼻喉科医生": "听力评估和中耳炎管理",
            "眼科医生": "视力评估",
            "神经科医生": "神经发育评估",
            "心脏科医生": "心脏异常评估",
            "遗传咨询师": "家族遗传风险评估"
        }),
        "follow_up_protocol": json.dumps({
            "手术后": "每周一次，持续一个月",
            "1-5岁": "每2个月一次",
            "5-12岁": "每4个月一次",
            "12岁以上": "每6个月一次"
        }),
        "evidence_level": "A",
        "references": json.dumps([
            "American Cleft Palate-Craniofacial Association. Parameters for evaluation and treatment of patients with cleft lip/palate or other craniofacial anomalies. Cleft Palate-Craniofacial Journal, 2018.",
            "World Health Organization. Global strategies to reduce the health-care burden of craniofacial anomalies. Geneva: WHO, 2020.",
            "Robin NH, et al. ACMG statement on the clinical genetic evaluation of the child with syndromic cleft lip and/or cleft palate. Genetics in Medicine, 2021."
        ]),
        "created_by": doctor_id
    }
]

for guideline in demo_guidelines:
    cursor.execute(
        """
        INSERT OR REPLACE INTO treatment_guidelines 
        (condition_id, title, description, cleft_type, syndrome_type, age_group, 
        treatment_steps, specialist_involvement, follow_up_protocol, 
        evidence_level, references, created_by) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            guideline["condition_id"], guideline["title"], guideline["description"],
            guideline["cleft_type"], guideline["syndrome_type"], guideline["age_group"],
            guideline["treatment_steps"], guideline["specialist_involvement"],
            guideline["follow_up_protocol"], guideline["evidence_level"],
            guideline["references"], guideline["created_by"]
        )
    )

# 创建演示患者数据
demo_patients = [
    {
        "name": "张小明",
        "age": "6个月",
        "gender": "男",
        "symptoms": "唇裂,腭裂",
        "medical_history": "足月顺产，无其他异常",
        "family_history": "无家族史",
        "created_by": doctor_id
    },
    {
        "name": "李小红",
        "age": "3个月",
        "gender": "女",
        "symptoms": "唇裂,腭裂,下唇凹陷,心脏异常,耳部异常",
        "medical_history": "足月顺产，发现心脏杂音",
        "family_history": "父亲有下唇凹陷",
        "created_by": doctor_id
    }
]

for patient in demo_patients:
    cursor.execute(
        """
        INSERT INTO patients 
        (name, age, gender, symptoms, medical_history, family_history, created_by) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient["name"], patient["age"], patient["gender"],
            patient["symptoms"], patient["medical_history"],
            patient["family_history"], patient["created_by"]
        )
    )
    
    # 获取新插入的患者ID
    patient_id = cursor.lastrowid
    
    # 根据症状判断是否为综合征性唇腭裂
    is_syndromic = "下唇凹陷" in patient["symptoms"] or "心脏异常" in patient["symptoms"]
    
    # 创建分析结果
    analysis = {
        "patient_id": patient_id,
        "cleft_type": "CLP",
        "syndrome_type": "syndromic" if is_syndromic else "non-syndromic",
        "specialist_recommendations": json.dumps({
            "整形外科医生": "评估唇腭裂严重程度，制定手术计划",
            "语言治疗师": "评估语音发育，提供早期干预",
            "牙医和正畸医生": "评估牙齿和颌骨发育",
            "耳鼻喉科医生": "评估听力，检查中耳炎风险",
            "遗传咨询师": "评估遗传风险，提供家族咨询"
        }) if not is_syndromic else json.dumps({
            "整形外科医生": "评估唇腭裂严重程度，制定手术计划",
            "遗传学专家": "进行综合征诊断，制定管理方案",
            "语言治疗师": "评估语音发育，提供早期干预",
            "牙医和正畸医生": "评估牙齿和颌骨发育",
            "耳鼻喉科医生": "评估听力，管理中耳炎",
            "眼科医生": "评估视力，检查眼部异常",
            "心脏科医生": "评估心脏功能，管理心脏异常",
            "遗传咨询师": "评估遗传风险，提供家族咨询"
        }),
        "treatment_recommendations": json.dumps({
            "短期计划": "喂养指导，准备唇裂修复手术",
            "中期计划": "腭裂修复手术，语音治疗",
            "长期计划": "牙齿矫正，颌骨评估，心理支持",
            "随访安排": "术后每周一次，之后每3个月一次"
        }) if not is_syndromic else json.dumps({
            "短期计划": "综合评估，喂养指导，准备唇裂修复手术",
            "中期计划": "腭裂修复手术，语音治疗，心脏功能监测",
            "长期计划": "牙齿矫正，颌骨评估，综合征并发症管理，心理支持",
            "随访安排": "术后每周一次，之后每2个月一次",
            "特殊注意事项": "需要多学科团队协作，密切监测心脏和耳部异常"
        }),
        "created_by": doctor_id
    }
    
    cursor.execute(
        """
        INSERT INTO analyses 
        (patient_id, cleft_type, syndrome_type, specialist_recommendations, 
        treatment_recommendations, created_by) 
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            analysis["patient_id"], analysis["cleft_type"], analysis["syndrome_type"],
            analysis["specialist_recommendations"], analysis["treatment_recommendations"],
            analysis["created_by"]
        )
    )

# 提交更改并关闭连接
conn.commit()
conn.close()

print("演示数据初始化完成！")
EOL

chmod +x init_demo_data.py

echo "步骤 5: 构建并启动演示环境..."
docker-compose up -d --build

echo "步骤 6: 等待服务启动..."
sleep 15

echo "步骤 7: 初始化演示数据..."
docker-compose exec -T backend python /app/init_demo_data.py

echo "步骤 8: 创建定时重置任务..."
cat > reset_demo.sh << EOL
#!/bin/bash
# 演示环境重置脚本
cd $DEMO_DIR
docker-compose exec -T backend python /app/init_demo_data.py
echo "\$(date) - 演示环境已重置" >> ./logs/reset.log
EOL

chmod +x reset_demo.sh

# 添加定时任务，每24小时重置一次
(crontab -l 2>/dev/null; echo "0 0 * * * $DEMO_DIR/reset_demo.sh") | crontab -

echo "步骤 9: 测试演示环境..."
# 测试后端健康状态
health_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)
if [ "$health_status" -eq "200" ]; then
  echo "✅ 后端健康状态检查通过"
else
  echo "❌ 后端健康状态检查失败，HTTP状态码: $health_status"
  echo "请检查日志: docker-compose logs backend"
fi

# 测试前端可访问性
frontend_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8081)
if [ "$frontend_status" -eq "200" ]; then
  echo "✅ 前端可访问性测试通过"
else
  echo "❌ 前端可访问性测试失败，HTTP状态码: $frontend_status"
  echo "请检查日志: docker-compose logs frontend"
fi

# 获取服务器的公网IP
PUBLIC_IP=$(curl -s ifconfig.me)

echo ""
echo "====================================================="
echo "  演示环境部署完成！"
echo "====================================================="
echo ""
echo "您可以通过以下地址访问演示系统："
echo "  前端应用：http://$PUBLIC_IP:8081"
echo "  后端API：http://$PUBLIC_IP:8080"
echo ""
echo "使用以下账户登录："
echo "  医生账户：doctor@example.com / demo123"
echo "  管理员账户：admin@example.com / demo123"
echo ""
echo "演示环境将每24小时自动重置一次"
echo ""
echo "如需查看日志，请使用以下命令："
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f frontend"
echo ""
echo "如需手动重置演示环境，请使用以下命令："
echo "  ./reset_demo.sh"
echo ""
echo "感谢您使用唇腭裂多智能体系统演示环境！"
