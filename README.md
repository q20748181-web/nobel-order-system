# 橱柜订单管理系统 (Nobel订单管理系统)

## 🎉 最新功能 - 云端数据同步 & 多用户协作

**✨ 已完成网络同步功能升级！**

- ✅ **多用户支持**: 不同用户在不同电脑上可以看到相同数据
- ✅ **云端数据库**: 使用 Supabase 实现数据实时同步
- ✅ **外网访问**: 支持多种外网访问方案，同事可随时随地访问
- ✅ **数据安全**: 云端备份，防止数据丢失

## 🌐 在线使用（推荐）

**点击下方链接直接使用（已预载示例数据）：**

```
https://coze-coding-project.tos.coze.site/coze_storage_7611717619640762422/c_6876f231.html?sign=1774837928-6b88125758-0-107d76cec2c67c76ec8444a197a0835e543f4c6a3e03ac82ba0b24e2577129d9
```

✅ 无需下载 | ✅ 已有示例数据 | ✅ 在线即可使用 | ✅ 数据本地保存

---

# 项目结构说明

本项目包含一个基于 Python + Streamlit 的橱柜订单管理 Web 应用。

## 功能特性

### HTML 版本（单机版）
- 📊 **仪表盘**：查看订单统计数据和状态分布
- 👥 **客户管理**：添加、查看、编辑、删除客户信息
- 🏷️ **产品管理**：管理橱柜产品（型号、价格、类别等）
- 📦 **订单管理**：创建订单、跟踪状态、导出数据

### Streamlit 后端版（云端版）⭐ 新功能
- 🌐 **用户登录**：支持多用户登录系统
- 👥 **客户管理**：云端客户信息管理
- 📝 **订单管理**：云端订单数据同步
- 🔄 **实时同步**：多用户实时看到相同数据
- 🌍 **外网访问**：支持同事在外网访问系统

## 快速开始

### 🚀 方式1：使用 Streamlit 后端（推荐，支持多用户）

#### 1. 启动服务
```bash
cd /workspace/projects
bash scripts/quick_start.sh
```

#### 2. 访问系统
- 内网访问: http://9.128.127.13:8501
- 本地访问: http://localhost:8501

#### 3. 配置外网访问（可选）
```bash
# 查看外网访问方案
python scripts/show_tunnel_solutions.py
```

#### 4. 查看详细教程
```bash
cat docs/QUICK_START_TUTORIAL.md
```

### 💻 方式2：使用 HTML 版本（单机使用）

#### 1. 安装依赖
```bash
pip install -r requirements.txt
```

#### 2. 运行应用
```bash
# 方式1：使用启动脚本
bash scripts/run_cabinet_order_system.sh

# 方式2：直接运行
streamlit run src/app.py
```

应用将在浏览器中自动打开：`http://localhost:8501`

### 🧪 测试数据库功能
```bash
python tests/test_cabinet_order_system.py
```

---

## 🚀 部署到生产环境

### 快速部署向导

运行部署向导，选择最适合您的部署方案：

```bash
bash scripts/deployment_wizard.sh
```

### 部署方案对比

| 方案 | 难度 | 费用 | 时间 | 稳定性 | 推荐度 |
|------|------|------|------|--------|--------|
| **Streamlit Cloud** | ⭐ 免费 | 3分钟 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 强烈推荐 |
| **云服务器** | ⭐⭐⭐ 50-100元/月 | 10-30分钟 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 长期使用 |
| **隧道服务** | ⭐⭐ 免费 | 5分钟 | ⭐⭐ | ⭐⭐ | 临时测试 |

### 方案1：Streamlit Cloud（最推荐）

**3分钟免费部署，固定URL，自动HTTPS**

1. 推送代码到 GitHub
2. 访问 https://share.streamlit.io/
3. 点击 "Deploy"

📖 详细教程：[docs/DEPLOY_STREAMLIT_CLOUD.md](docs/DEPLOY_STREAMLIT_CLOUD.md)

### 方案2：云服务器（最稳定）

**固定IP，高性能，完全控制**

1. 购买云服务器（50-100元/月）
2. 运行部署脚本：
   ```bash
   bash scripts/deploy_to_server.sh
   ```
3. 上传代码
4. 完成！

📖 详细教程：[docs/DEPLOY_CLOUD_SERVER.md](docs/DEPLOY_CLOUD_SERVER.md)

### 方案3：隧道服务（临时使用）

**快速设置，免费，无需购买**

```bash
# 在本地电脑执行
ssh -R 80:9.128.127.13:8501 serveo.net
```

等待显示外网地址即可！

💡 查看更多方案：`python scripts/show_tunnel_solutions.py`

### 📚 完整部署文档

- **部署指南总结**：[docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)
- **Streamlit Cloud部署**：[docs/DEPLOY_STREAMLIT_CLOUD.md](docs/DEPLOY_STREAMLIT_CLOUD.md)
- **云服务器部署**：[docs/DEPLOY_CLOUD_SERVER.md](docs/DEPLOY_CLOUD_SERVER.md)

---

## 🎯 我的推荐

### 如果你是：

👉 **小团队（<10人）** → **Streamlit Cloud**
- 免费、简单、够用
- 3分钟部署完成

👉 **中大型团队（>10人）** → **云服务器**
- 性能好、可扩展、专业
- 固定IP，可配置域名

👉 **临时测试** → **隧道服务**
- 快速、免费、无需购买

## 详细文档

### 📚 Streamlit 后端文档
- **快速使用教程**: [docs/QUICK_START_TUTORIAL.md](docs/QUICK_START_TUTORIAL.md)
- **完成报告**: [COMPLETION_REPORT.md](COMPLETION_REPORT.md)

### 📖 HTML 版本文档
- **完整使用文档**: [docs/CABINET_ORDER_SYSTEM_README.md](docs/CABINET_ORDER_SYSTEM_README.md)

### 🔧 脚本工具
- `scripts/quick_start.sh` - 快速启动脚本
- `scripts/start_server.sh` - 服务启动脚本
- `scripts/show_tunnel_solutions.py` - 外网访问方案展示
- `scripts/migrate_data.py` - 数据迁移工具

---

# 本地运行
## 运行流程
bash scripts/local_run.sh -m flow

## 运行节点
bash scripts/local_run.sh -m node -n node_name

# 启动HTTP服务
bash scripts/http_run.sh -m http -p 5000

