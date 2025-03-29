#!/bin/bash

# 唇腭裂多智能体系统初始化脚本

# 确保脚本在错误时退出
set -e

echo "开始初始化唇腭裂多智能体系统数据..."

# 检查容器是否运行
backend_status=$(docker-compose ps | grep backend | grep -c "Up" || echo "0")
if [ "$backend_status" -ne "1" ]; then
  echo "后端服务未运行，请先运行部署脚本"
  exit 1
fi

# 创建初始管理员用户
echo "创建初始管理员用户..."
docker-compose exec backend python -c "
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

# 创建初始医生用户
echo "创建初始医生用户..."
docker-compose exec backend python -c "
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

# 创建初始治疗指南
echo "创建初始治疗指南..."
docker-compose exec backend python -c "
from utils.database import get_db_session
from models.treatment_guideline import TreatmentGuideline
from models.user import User
import json

with get_db_session() as db:
    # 获取医生用户ID
    doctor = db.query(User).filter(User.email == 'doctor@example.com').first()
    if not doctor:
        print('医生用户不存在，无法创建治疗指南')
        exit(1)
    
    # 检查是否已存在治疗指南
    guideline = db.query(TreatmentGuideline).filter(TreatmentGuideline.condition_id == 'CLP_NONSYNDROMIC').first()
    if not guideline:
        guideline = TreatmentGuideline(
            condition_id='CLP_NONSYNDROMIC',
            title='非综合征性唇腭裂治疗指南',
            description='针对非综合征性唇腭裂患者的标准治疗方案',
            cleft_type='CLP',
            syndrome_type='non-syndromic',
            age_group='infant',
            treatment_steps=json.dumps({
                '0-3个月': '评估和喂养指导',
                '3-6个月': '唇裂修复手术',
                '9-18个月': '腭裂修复手术',
                '2-5岁': '语音评估和治疗',
                '5-7岁': '牙齿和颌骨评估',
                '8-12岁': '牙齿矫正和骨移植',
                '16-18岁': '最终整形手术'
            }),
            specialist_involvement=json.dumps({
                '整形外科医生': '唇裂和腭裂修复手术',
                '语言治疗师': '语音评估和治疗',
                '牙医和正畸医生': '牙齿和颌骨评估与治疗',
                '耳鼻喉科医生': '听力评估',
                '遗传咨询师': '家族遗传风险评估'
            }),
            follow_up_protocol=json.dumps({
                '手术后': '每周一次，持续一个月',
                '1-5岁': '每3个月一次',
                '5-12岁': '每6个月一次',
                '12岁以上': '每年一次'
            }),
            evidence_level='A',
            references=json.dumps([
                'American Cleft Palate-Craniofacial Association. Parameters for evaluation and treatment of patients with cleft lip/palate or other craniofacial anomalies. Cleft Palate-Craniofacial Journal, 2018.',
                'World Health Organization. Global strategies to reduce the health-care burden of craniofacial anomalies. Geneva: WHO, 2020.'
            ]),
            created_by=doctor.id
        )
        db.add(guideline)
        print('非综合征性唇腭裂治疗指南已创建')
    else:
        print('非综合征性唇腭裂治疗指南已存在')
    
    # 创建综合征性唇腭裂治疗指南
    guideline = db.query(TreatmentGuideline).filter(TreatmentGuideline.condition_id == 'CLP_SYNDROMIC').first()
    if not guideline:
        guideline = TreatmentGuideline(
            condition_id='CLP_SYNDROMIC',
            title='综合征性唇腭裂治疗指南',
            description='针对综合征性唇腭裂患者的综合治疗方案',
            cleft_type='CLP',
            syndrome_type='syndromic',
            age_group='infant',
            treatment_steps=json.dumps({
                '出生后': '综合评估和遗传检测',
                '0-3个月': '喂养指导和呼吸管理',
                '3-6个月': '唇裂修复手术',
                '9-18个月': '腭裂修复手术',
                '2-5岁': '语音评估和治疗',
                '5-7岁': '牙齿和颌骨评估',
                '8-12岁': '牙齿矫正和骨移植',
                '12-18岁': '综合征相关并发症管理',
                '16-18岁': '最终整形手术'
            }),
            specialist_involvement=json.dumps({
                '整形外科医生': '唇裂和腭裂修复手术',
                '遗传学专家': '综合征诊断和管理',
                '语言治疗师': '语音评估和治疗',
                '牙医和正畸医生': '牙齿和颌骨评估与治疗',
                '耳鼻喉科医生': '听力评估和中耳炎管理',
                '眼科医生': '视力评估',
                '神经科医生': '神经发育评估',
                '心脏科医生': '心脏异常评估',
                '遗传咨询师': '家族遗传风险评估'
            }),
            follow_up_protocol=json.dumps({
                '手术后': '每周一次，持续一个月',
                '1-5岁': '每2个月一次',
                '5-12岁': '每4个月一次',
                '12岁以上': '每6个月一次'
            }),
            evidence_level='A',
            references=json.dumps([
                'American Cleft Palate-Craniofacial Association. Parameters for evaluation and treatment of patients with cleft lip/palate or other craniofacial anomalies. Cleft Palate-Craniofacial Journal, 2018.',
                'World Health Organization. Global strategies to reduce the health-care burden of craniofacial anomalies. Geneva: WHO, 2020.',
                'Robin NH, et al. ACMG statement on the clinical genetic evaluation of the child with syndromic cleft lip and/or cleft palate. Genetics in Medicine, 2021.'
            ]),
            created_by=doctor.id
        )
        db.add(guideline)
        print('综合征性唇腭裂治疗指南已创建')
    else:
        print('综合征性唇腭裂治疗指南已存在')
"

echo "初始化完成！"
echo "您可以使用以下账户登录系统："
echo "  管理员：admin@example.com / admin123"
echo "  医生：doctor@example.com / doctor123"
