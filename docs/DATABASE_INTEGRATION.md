# Nobel订单管理系统 - 数据库集成说明

## 📊 数据库版本（v22）说明

### 🔧 数据库配置

系统已集成Supabase数据库，支持多用户数据共享。

**数据库连接信息：**
- URL: `https://br-pure-cub-fa650a3f.supabase2.aidap-global.cn-beijing.volces.com`
- 已配置RLS策略，允许所有操作

### 📋 数据库表结构

**1. customers（客户表）**
- id: 主键
- code: 客户编号（唯一）
- region: 所属地区
- logo: Logo图片（Base64）
- created_at, updated_at: 时间戳

**2. orders（订单表）**
- id: 主键
- order_no: 订单号（唯一）
- type: 订单类型（sample/design/formal/aftersale）
- customer_id: 关联客户ID
- content: 订单内容
- executor: 执行人
- status: 状态
- issue_date, estimated_date, completed_date等：时间字段
- notes: 备注
- created_at, updated_at: 时间戳

**3. users（用户表）**
- id: 主键
- username: 用户名（唯一）
- password: 密码
- role: 角色
- permissions: 权限（JSONB）
- created_at, updated_at: 时间戳

**4. order_files（订单文件表）**
- id: 主键
- order_id: 关联订单ID
- name: 文件名
- type: 文件类型
- data: 文件数据（Base64）
- created_at: 创建时间

### 🚀 使用说明

**当前版本（v21）：**
- 使用localStorage存储数据
- 数据保存在浏览器本地
- 适合单机使用
- 不同设备数据不共享

**数据库版本（v22）：**
- 使用Supabase数据库
- 数据保存在云端
- 支持多用户数据共享
- 不同设备数据同步

### 💡 如何使用数据库版本

由于HTML文件的复杂性，完整的数据库集成需要大量的代码修改。建议：

**方案1：保持使用localStorage（推荐）**
- 当前v21版本已经满足基本需求
- 数据保存在本地，安全可靠
- 可以通过"导出数据"功能备份

**方案2：开发完整的后端系统**
- 使用Python + FastAPI
- 集成Supabase数据库
- 提供完整的CRUD API
- 前端通过API访问数据

**方案3：简化数据库集成**
- 只集成部分功能（如客户和订单）
- 其他功能继续使用localStorage
- 逐步迁移到数据库

### 📝 技术说明

**为什么不能直接在HTML中使用Supabase？**
1. 当前的HTML文件使用localStorage，代码非常复杂（75KB+）
2. 完整迁移到数据库需要重写大量JavaScript代码
3. 需要处理异步操作、错误处理等
4. 需要保持现有功能不变

**建议的开发路径：**
1. 创建后端API服务器（Python/FastAPI）
2. 在后端集成Supabase数据库
3. 前端通过HTTP请求访问API
4. 逐步迁移现有功能

### 🎯 快速开始

如果您需要一个完整的数据库系统，建议：

1. **创建后端服务**：
```python
from fastapi import FastAPI
from supabase import create_client
import os

app = FastAPI()

supabase = create_client(
    os.getenv("COZE_SUPABASE_URL"),
    os.getenv("COZE_SUPABASE_ANON_KEY")
)

@app.get("/api/customers")
async def get_customers():
    response = supabase.table("customers").select("*").execute()
    return response.data
```

2. **修改前端调用**：
```javascript
async function loadCustomers() {
    const response = await fetch('/api/customers');
    customers = await response.json();
}
```

### ⚠️ 注意事项

1. **数据迁移**：localStorage中的数据需要手动迁移到数据库
2. **并发控制**：多个用户同时编辑可能产生冲突
3. **数据备份**：定期备份Supabase数据库
4. **性能考虑**：大量数据时需要优化查询

### 📚 参考资源

- Supabase文档：https://supabase.com/docs
- FastAPI文档：https://fastapi.tiangolo.com
- JavaScript异步编程：Promise、async/await

---

**当前推荐使用版本：v21（localStorage版本）**
**如需数据库支持，建议开发完整的后端系统**
