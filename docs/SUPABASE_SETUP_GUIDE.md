# Nobel订单管理系统 - Supabase 快速设置指南

## 🚀 创建 Supabase 项目

### Step 1: 注册和登录

1. **访问**：https://supabase.com
2. **点击 "Start your project"**
3. **使用 GitHub 账号登录**（推荐）或 Email 注册
4. **登录后，点击 "New project"**

### Step 2: 创建项目

填写以下信息：

| 字段 | 填写内容 |
|------|----------|
| Name | `nobel-order-system` |
| Database Password | **设置一个强密码并记住它！** |
| Region | 选择 `Southeast Asia (Singapore)` 或离您最近的地区 |
| Pricing Plan | 选择 **Free**（免费，足够使用） |

3. **点击 "Create new project"**
4. **等待 1-2 分钟**，项目创建完成

---

## 🔧 初始化数据库

### Step 1: 访问 SQL 编辑器

1. **在 Supabase 控制台**，点击左侧菜单的 `SQL Editor`
2. **点击 "New query"`

### Step 2: 执行初始化脚本

**复制以下 SQL 脚本，粘贴到 SQL 编辑器中，然后点击 "Run"：**

```sql
-- Nobel订单管理系统 - 数据库初始化脚本

-- 启用 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    full_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. 创建客户表
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    email VARCHAR(100),
    company VARCHAR(100),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. 创建订单表
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id UUID REFERENCES customers(id),
    type VARCHAR(50) DEFAULT 'sample', -- sample（打样）, formal（正式）
    status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed, cancelled
    total_amount DECIMAL(10, 2) DEFAULT 0,
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. 创建订单文件表
CREATE TABLE IF NOT EXISTS order_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    file_type VARCHAR(50),
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. 创建订单项表（订单详情）
CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_name VARCHAR(200),
    quantity INTEGER DEFAULT 1,
    unit_price DECIMAL(10, 2) DEFAULT 0,
    total_price DECIMAL(10, 2) DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name);
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_type ON orders(type);
CREATE INDEX IF NOT EXISTS idx_order_files_order_id ON order_files(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);

-- 插入默认用户（密码: admin123）
INSERT INTO users (username, password, full_name, email)
VALUES ('admin', 'admin123', '系统管理员', 'admin@nobel.com')
ON CONFLICT (username) DO NOTHING;

-- 显示创建成功消息
SELECT '✅ 数据库表创建成功！' as message;
```

执行成功后，您会看到消息：`✅ 数据库表创建成功！`

---

## 🔑 获取环境变量

### Step 1: 访问 API 设置

1. **在 Supabase 控制台**，点击左侧菜单的 `Settings`（设置图标）
2. **点击 `API`**

### Step 2: 复制必要信息

在 API 页面，您需要复制以下两个值：

#### 1. Project URL
- 在 `Project URL` 部分
- 复制完整的 URL，例如：
  ```
  https://abcxyz123.supabase.co
  ```

#### 2. anon public key
- 在 `Project API keys` 部分
- 找到 `anon public` 密钥
- 复制这个很长的字符串，例如：
  ```
  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```

**注意**：
- 不要复制 `service_role` 密钥（这是管理员密钥，不应该在应用中使用）
- 只需要 `anon public` 密钥

---

## ⚙️ 在 Streamlit Cloud 配置环境变量

### Step 1: 进入应用设置

1. **访问您的 Streamlit Cloud 应用**
2. **点击 "Manage app"**
3. **点击 "Settings" 标签**

### Step 2: 配置 Secrets

1. **找到 "Secrets" 部分**
2. **点击展开编辑框**
3. **粘贴以下内容**（替换为您实际的值）：

```toml
[secrets]
COZE_SUPABASE_URL = "https://您的ProjectURL.supabase.co"
COZE_SUPABASE_ANON_KEY = "您的anon key"
```

**示例**：
```toml
[secrets]
COZE_SUPABASE_URL = "https://abcxyz123.supabase.co"
COZE_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFjeHl6MTIzIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzYxMjM0NTYsImV4cCI6MTk5MTY5OTQ1Nn0.abc123def456..."
```

**注意**：
- 引号要保留
- URL 要包含 `https://`
- 每个值都要用双引号包裹

### Step 3: 保存并重新部署

1. **点击 "Save changes"**
2. **Streamlit Cloud 会自动重新部署**
3. **等待 1-2 分钟**

---

## 🎉 完成！

部署完成后，访问您的应用：

```
https://nobel-order-system.streamlit.app
```

### 默认登录信息

- **用户名**：`admin`
- **密码**：`admin123`

---

## 📝 重要提示

1. **免费额度**：Supabase 免费版提供：
   - 500MB 数据库存储
   - 2GB 文件存储
   - 50,000 次月度 API 请求
   - 2 并行连接

2. **安全性**：
   - 请修改默认密码
   - 不要在前端代码中暴露 `service_role` 密钥
   - 定期更新 API 密钥

3. **备份数据**：
   - Supabase 免费版提供自动备份
   - 可以手动导出数据

---

## ❓ 常见问题

### Q1: 执行 SQL 脚本时出错？
**A**: 确保复制了完整的脚本，从 `-- 启用 UUID 扩展` 开始到最后的 `SELECT` 语句。

### Q2: 找不到 API 设置？
**A**: 在 Supabase 控制台，点击左侧菜单的齿轮图标（Settings），然后选择 API。

### Q3: 配置环境变量后还是报错？
**A**:
1. 检查 URL 是否包含 `https://`
2. 检查 anon key 是否正确复制
3. 确认引号格式正确
4. 等待 1-2 分钟让配置生效

### Q4: 忘记数据库密码？
**A**: 在 Supabase 控制台，访问 `Settings > Database`，可以重置密码。

---

## 🚀 开始使用

配置完成后，您就可以：
- 登录系统
- 管理客户信息
- 创建订单
- 查看数据

**祝您使用愉快！** 🎉
