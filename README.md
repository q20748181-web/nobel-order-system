# 项目结构说明

# 橱柜订单管理系统

本项目包含一个基于 Python + Streamlit 的橱柜订单管理 Web 应用。

## 功能特性

- 📊 **仪表盘**：查看订单统计数据和状态分布
- 👥 **客户管理**：添加、查看、编辑、删除客户信息
- 🏷️ **产品管理**：管理橱柜产品（型号、价格、类别等）
- 📦 **订单管理**：创建订单、跟踪状态、导出数据

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
# 方式1：使用启动脚本
bash scripts/run_cabinet_order_system.sh

# 方式2：直接运行
streamlit run src/app.py
```

应用将在浏览器中自动打开：`http://localhost:8501`

### 3. 测试数据库功能
```bash
python tests/test_cabinet_order_system.py
```

## 详细文档

完整使用文档请查看：[docs/CABINET_ORDER_SYSTEM_README.md](docs/CABINET_ORDER_SYSTEM_README.md)

---

# 本地运行
## 运行流程
bash scripts/local_run.sh -m flow

## 运行节点
bash scripts/local_run.sh -m node -n node_name

# 启动HTTP服务
bash scripts/http_run.sh -m http -p 5000

