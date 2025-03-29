# 唇腭裂多智能体系统后端架构设计

## 1. 架构概述

唇腭裂多智能体系统后端采用分层架构，主要包括以下几个层次：

- **API层**：处理HTTP请求和响应，提供RESTful API接口
- **服务层**：实现业务逻辑，协调各个组件
- **模型层**：定义数据模型和数据库交互
- **智能体层**：集成现有的智能体系统
- **工具层**：提供通用工具和辅助功能
- **配置层**：管理系统配置和环境变量

## 2. 技术栈选择

- **Web框架**：FastAPI（高性能异步框架，支持自动API文档生成）
- **数据库**：PostgreSQL（关系型数据库，适合存储结构化医疗数据）
- **ORM**：SQLAlchemy（功能强大的ORM工具，支持异步操作）
- **认证**：JWT（JSON Web Token，用于用户认证和授权）
- **API文档**：Swagger/OpenAPI（自动生成API文档）
- **部署**：Docker + Kubernetes（容器化部署，便于扩展和管理）
- **缓存**：Redis（高性能缓存，用于存储会话和临时数据）
- **异步任务**：Celery（处理长时间运行的任务，如复杂分析）

## 3. 目录结构

```
backend/
├── api/                  # API层，处理HTTP请求和响应
│   ├── endpoints/        # API端点定义
│   ├── dependencies.py   # API依赖项
│   ├── errors.py         # 错误处理
│   └── router.py         # 路由配置
├── models/               # 数据模型定义
│   ├── patient.py        # 患者模型
│   ├── analysis.py       # 分析结果模型
│   ├── user.py           # 用户模型
│   └── base.py           # 基础模型类
├── services/             # 服务层，实现业务逻辑
│   ├── patient_service.py    # 患者相关服务
│   ├── analysis_service.py   # 分析相关服务
│   ├── agent_service.py      # 智能体服务
│   └── user_service.py       # 用户相关服务
├── agents/               # 智能体集成
│   ├── agent_manager.py      # 智能体管理器
│   ├── cleft_agent.py        # 唇腭裂专科智能体
│   ├── craniofacial_agent.py # 颅面外科智能体
│   └── genetic_agent.py      # 遗传学智能体
├── utils/                # 工具和辅助功能
│   ├── database.py       # 数据库连接工具
│   ├── security.py       # 安全相关工具
│   └── logger.py         # 日志工具
├── config/               # 配置管理
│   ├── settings.py       # 系统设置
│   └── constants.py      # 常量定义
├── tasks/                # 异步任务
│   ├── worker.py         # Celery worker
│   └── tasks.py          # 任务定义
├── tests/                # 测试
│   ├── api/              # API测试
│   ├── services/         # 服务测试
│   └── conftest.py       # 测试配置
├── alembic/              # 数据库迁移
├── main.py               # 应用入口
├── requirements.txt      # 依赖列表
└── Dockerfile            # Docker配置
```

## 4. API设计

### 4.1 用户管理API

- `POST /api/users/register` - 用户注册
- `POST /api/users/login` - 用户登录
- `GET /api/users/me` - 获取当前用户信息
- `PUT /api/users/me` - 更新用户信息
- `POST /api/users/reset-password` - 重置密码

### 4.2 患者管理API

- `POST /api/patients` - 创建新患者
- `GET /api/patients` - 获取患者列表
- `GET /api/patients/{patient_id}` - 获取患者详情
- `PUT /api/patients/{patient_id}` - 更新患者信息
- `DELETE /api/patients/{patient_id}` - 删除患者

### 4.3 分析API

- `POST /api/analysis/patient/{patient_id}` - 分析患者数据
- `GET /api/analysis/{analysis_id}` - 获取分析结果
- `GET /api/analysis/patient/{patient_id}` - 获取患者的所有分析结果
- `DELETE /api/analysis/{analysis_id}` - 删除分析结果

### 4.4 治疗指南API

- `GET /api/guidelines` - 获取所有治疗指南
- `GET /api/guidelines/{condition_id}` - 获取特定条件的治疗指南

### 4.5 医学文献API

- `GET /api/literature/search` - 搜索医学文献
- `GET /api/literature/{literature_id}` - 获取文献详情

## 5. 数据模型设计

### 5.1 用户模型 (User)

```python
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 5.2 患者模型 (Patient)

```python
class Patient(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    age = Column(String)
    gender = Column(String)
    symptoms = Column(ARRAY(String))
    medical_history = Column(Text)
    family_history = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="patients")
    analyses = relationship("Analysis", back_populates="patient")
```

### 5.3 分析结果模型 (Analysis)

```python
class Analysis(Base):
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    syndrome_type = Column(String)  # syndromic/non-syndromic
    syndrome_name = Column(String, nullable=True)  # 如果是综合征性，则记录综合征名称
    cleft_type = Column(String)  # 唇腭裂类型
    severity = Column(String)  # 严重程度
    treatment_recommendations = Column(JSONB)  # 治疗建议
    specialist_recommendations = Column(JSONB)  # 专科会诊建议
    follow_up_plan = Column(JSONB)  # 随访计划
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="analyses")
```

### 5.4 治疗指南模型 (TreatmentGuideline)

```python
class TreatmentGuideline(Base):
    id = Column(Integer, primary_key=True, index=True)
    condition_id = Column(String, unique=True, index=True)  # 条件ID，如"non_syndromic_cleft_lip"
    title = Column(String)
    recommendations = Column(JSONB)  # 治疗建议
    follow_up = Column(Text)  # 随访建议
    references = Column(ARRAY(String))  # 参考文献
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 5.5 医学文献模型 (Literature)

```python
class Literature(Base):
    id = Column(Integer, primary_key=True, index=True)
    pubmed_id = Column(String, unique=True, index=True)
    title = Column(String)
    authors = Column(JSONB)
    journal = Column(String)
    publication_date = Column(Date)
    abstract = Column(Text)
    doi = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## 6. 认证与授权

系统将使用JWT（JSON Web Token）进行认证和授权：

1. 用户登录时，系统验证凭据并生成JWT令牌
2. 客户端在后续请求中包含JWT令牌
3. 系统验证令牌的有效性和权限

权限级别：
- 匿名用户：可以查看公开信息
- 注册用户：可以创建和管理自己的患者数据
- 医生用户：可以查看和分析患者数据
- 管理员：可以管理系统和用户

## 7. 安全考虑

- 使用HTTPS加密所有通信
- 密码哈希存储（使用bcrypt）
- 输入验证和清理，防止注入攻击
- 敏感数据加密存储
- 定期安全审计和更新
- 遵循HIPAA等医疗数据隐私标准

## 8. 性能优化

- 使用Redis缓存频繁访问的数据
- 数据库索引优化
- 异步处理长时间运行的任务
- 分页处理大量数据
- 按需加载关联数据

## 9. 扩展性考虑

- 模块化设计，便于添加新功能
- 微服务架构，可独立扩展各组件
- API版本控制，支持向后兼容
- 容器化部署，便于水平扩展

## 10. 部署架构

系统将采用以下部署架构：

- Web服务器：Nginx（处理静态资源和反向代理）
- 应用服务器：FastAPI应用（多实例部署）
- 数据库服务器：PostgreSQL（主从复制）
- 缓存服务器：Redis（集群模式）
- 任务队列：Celery + RabbitMQ
- 容器编排：Kubernetes
- 监控：Prometheus + Grafana
- 日志：ELK Stack（Elasticsearch, Logstash, Kibana）

## 11. 开发和部署流程

1. 本地开发环境设置
2. 代码版本控制（Git）
3. 自动化测试（单元测试、集成测试）
4. CI/CD流水线（GitHub Actions）
5. 容器构建和推送
6. Kubernetes部署
7. 监控和日志收集
8. 定期备份和恢复测试
