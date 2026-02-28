# 橱柜订单管理系统

一个基于 Python + Streamlit 的橱柜订单管理 Web 应用，支持客户管理、产品管理、订单管理和数据导出功能。

## 功能特性

### 📊 仪表盘
- 查看订单统计数据
- 订单状态分布图表

### 👥 客户管理
- 添加新客户（姓名、电话、地址、邮箱）
- 查看客户列表
- 编辑客户信息
- 删除客户（无关联订单时）

### 🏷️ 产品管理
- 添加新产品（名称、类别、价格、单位、描述）
- 查看产品列表
- 编辑产品信息
- 删除产品（无关联订单时）
- 按类别筛选产品

### 📦 订单管理
- 创建订单（选择客户、添加产品、设置数量）
- 查看订单列表
- 更新订单状态（待处理、已确认、生产中、已完成、已取消）
- 查看订单明细
- 删除订单
- 搜索和筛选订单
- 导出订单数据为 CSV

## 技术栈

- **后端框架**: Streamlit
- **数据库**: SQLite
- **数据处理**: Pandas
- **Python 版本**: 3.8+

## 安装与运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
streamlit run src/app.py
```

应用将在浏览器中自动打开，默认地址为：`http://localhost:8501`

## 数据结构

### 客户表 (customers)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | TEXT | 客户姓名 |
| phone | TEXT | 联系电话 |
| address | TEXT | 地址 |
| email | TEXT | 邮箱（可选） |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### 产品表 (products)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | TEXT | 产品名称 |
| category | TEXT | 产品类别 |
| description | TEXT | 产品描述 |
| price | REAL | 价格 |
| unit | TEXT | 单位 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### 订单表 (orders)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| order_no | TEXT | 订单编号（唯一） |
| customer_id | INTEGER | 客户ID（外键） |
| status | TEXT | 订单状态 |
| total_amount | REAL | 总金额 |
| notes | TEXT | 备注 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### 订单明细表 (order_items)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| order_id | INTEGER | 订单ID（外键） |
| product_id | INTEGER | 产品ID（外键） |
| quantity | REAL | 数量 |
| unit_price | REAL | 单价 |
| subtotal | REAL | 小计 |

## 使用流程

### 创建订单流程

1. **添加客户**
   - 在"客户管理"页面添加客户信息

2. **添加产品**
   - 在"产品管理"页面添加产品信息

3. **创建订单**
   - 进入"订单管理" → "创建订单"
   - 选择客户
   - 选择产品并设置数量
   - 点击"添加到订单"
   - 可以添加多个产品
   - 填写备注（可选）
   - 点击"提交订单"

### 管理订单

1. **查看订单**
   - 在"订单管理" → "订单列表"查看所有订单
   - 可以按状态筛选
   - 可以搜索订单号或客户姓名

2. **更新状态**
   - 选择订单后，更新订单状态
   - 状态包括：待处理、已确认、生产中、已完成、已取消

3. **导出订单**
   - 点击"导出订单"按钮
   - 下载 CSV 格式的订单数据

## 数据存储

- 数据库文件位置：`assets/cabinet_orders.db`
- 首次运行时自动创建数据库和表结构

## 常见问题

### Q: 如何备份数据？
A: 直接复制 `assets/cabinet_orders.db` 文件即可备份所有数据。

### Q: 如何重置系统？
A: 删除 `assets/cabinet_orders.db` 文件，重新运行应用即可创建新的空数据库。

### Q: 订单编号格式是什么？
A: 订单编号格式为 `ORD + 年月日 + 序号`，例如 `ORD202401010001`

### Q: 可以同时添加多个产品到订单吗？
A: 可以，在创建订单时可以多次选择产品添加到购物车中。

## 开发说明

### 项目结构
```
src/
├── app.py                    # Streamlit 主应用
├── storage/
│   └── database.py           # 数据库管理模块
assets/
└── cabinet_orders.db         # SQLite 数据库文件
```

### 数据库操作

数据库操作封装在 `storage/database.py` 中，主要类：
- `DatabaseManager`: 数据库管理类
  - 客户管理：`add_customer`, `get_customer`, `update_customer`, `delete_customer`
  - 产品管理：`add_product`, `get_product`, `update_product`, `delete_product`
  - 订单管理：`create_order`, `get_order`, `update_order_status`, `delete_order`
  - 统计查询：`get_order_stats`

## 许可证

MIT License

## 支持

如有问题或建议，请联系开发团队。
