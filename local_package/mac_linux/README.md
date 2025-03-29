# 唇腭裂多智能体系统 - 本地部署指南

本文档提供了在本地环境中部署唇腭裂多智能体系统的详细步骤。

## 系统要求

- **操作系统**：macOS 10.15+或Linux
- **内存**：至少4GB RAM
- **存储空间**：至少2GB可用空间
- **必备软件**：Docker和Docker Compose

## Docker安装指南

### Mac系统

1. 下载并安装 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. 安装完成后，启动Docker Desktop
3. 等待Docker服务完全启动（菜单栏图标变为稳定状态）

### Linux系统

根据您的Linux发行版，执行相应的安装命令：

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

**CentOS/RHEL**:
```bash
sudo yum install -y docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

## 部署步骤

1. 解压下载包到任意目录
2. 打开终端，进入解压目录
3. 执行以下命令：
   ```bash
   chmod +x deploy_local.sh
   ./deploy_local.sh
   ```
4. 等待部署完成（约5-10分钟）
5. 系统会自动打开浏览器访问http://localhost:3000

## 系统访问

部署完成后，您可以通过以下地址访问系统：

- **前端应用**：http://localhost:3000
- **后端API**：http://localhost:8000

## 登录信息

系统预设了以下账户：

- **管理员账户**：
  - 邮箱：admin@example.com
  - 密码：admin123

- **医生账户**：
  - 邮箱：doctor@example.com
  - 密码：doctor123

## 常见问题解答

### Q: 如何停止系统？

A: 在命令行中执行以下命令：
```bash
docker-compose down
```

### Q: 如何重启系统？

A: 在命令行中执行以下命令：
```bash
docker-compose up -d
```

### Q: 如何查看系统日志？

A: 在命令行中执行以下命令：
```bash
# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend
```

### Q: 部署失败怎么办？

A: 请检查以下几点：
1. 确保Docker已正确安装并运行
2. 确保端口8000和3000未被其他应用占用
3. 查看部署脚本输出的错误信息
4. 检查Docker日志：`docker-compose logs`

### Q: 如何更新系统？

A: 下载最新版本的部署包，然后按照上述部署步骤重新部署。

## 系统功能简介

唇腭裂多智能体系统是一个基于人工智能的医疗辅助决策系统，专门用于唇腭裂患者的诊断和治疗建议。系统主要功能包括：

1. **患者分析**：输入患者症状、年龄等信息，系统会自动分析是否为综合征性唇腭裂
2. **智能体协作**：系统会根据症状自动招募相关专科智能体（颅面外科、遗传学、外耳科等）
3. **治疗建议**：系统会生成个性化的治疗建议和随访计划
4. **医学文献**：可以搜索相关医学文献和参考资料

## 联系与支持

如果您在部署或使用过程中遇到任何问题，请联系系统开发团队获取支持。
