-- Nobel订单管理系统 - 数据库初始化脚本
-- 在 Supabase SQL Editor 中执行此脚本

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

-- 插入默认用户（密码: admin123，实际使用应该加密）
-- 注意：这只是示例，生产环境应该使用加密密码
INSERT INTO users (username, password, full_name, email)
VALUES ('admin', 'admin123', '系统管理员', 'admin@nobel.com')
ON CONFLICT (username) DO NOTHING;

-- 显示创建成功消息
SELECT '✅ 数据库表创建成功！' as message;
