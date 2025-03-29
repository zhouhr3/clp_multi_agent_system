# 唇腭裂多智能体系统 AutoDL 部署指南

本文档提供了在 AutoDL 平台上部署唇腭裂多智能体系统的详细步骤。

## 部署前准备

1. 确保您已有 AutoDL 账号并能够登录
2. 准备创建一个新的实例或使用现有实例

## 详细部署步骤

### 步骤 1: 创建 AutoDL 实例

1. 登录 AutoDL 平台 (https://www.autodl.com)
2. 点击"新建实例"按钮
3. 选择以下配置:
   - CPU: 4核或以上
   - 内存: 8GB或以上
   - 系统: Ubuntu 20.04
   - 镜像: Docker
4. 点击"确认创建"按钮

### 步骤 2: 连接到实例

1. 实例创建完成后，点击"打开 Web 终端"按钮
2. 等待终端加载完成

### 步骤 3: 下载部署包

在终端中执行以下命令:

```bash
# 创建工作目录
mkdir -p ~/cleft_multi_agent_system
cd ~/cleft_multi_agent_system

# 下载部署包
wget https://example.com/cleft_multi_agent_system.zip

# 解压部署包
unzip cleft_multi_agent_system.zip
```

### 步骤 4: 执行部署脚本

在终端中执行以下命令:

```bash
# 设置脚本执行权限
chmod +x deploy_autodl.sh

# 执行部署脚本
./deploy_autodl.sh
```

部署脚本会自动完成以下操作:
- 安装必要的依赖
- 配置环境变量
- 启动 Docker 容器
- 初始化系统数据
- 配置端口映射
- 测试系统运行状态

### 步骤 5: 访问系统

部署完成后，您将看到系统访问信息，包括:
- 前端应用地址
- 后端 API 地址
- 登录账户信息

您可以通过浏览器访问前端应用地址，使用提供的账户登录系统。

## 常见问题解答

### Q: 如何查看系统日志?

A: 在终端中执行以下命令:
```bash
cd ~/cleft_multi_agent_system
docker-compose logs -f frontend  # 查看前端日志
docker-compose logs -f backend   # 查看后端日志
```

### Q: 如何停止系统?

A: 在终端中执行以下命令:
```bash
cd ~/cleft_multi_agent_system
docker-compose down
```

### Q: 如何重启系统?

A: 在终端中执行以下命令:
```bash
cd ~/cleft_multi_agent_system
docker-compose up -d
```

### Q: 部署失败怎么办?

A: 请检查以下几点:
1. 确保 AutoDL 实例有足够的资源
2. 确保网络连接正常
3. 查看部署日志，找出错误原因
4. 如需帮助，请联系系统开发者

## 联系支持

如果您在部署过程中遇到任何问题，请随时联系我们获取支持。
