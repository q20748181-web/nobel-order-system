#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nobel订单管理系统 - 简化的 Streamlit 应用
直接提供 HTTP 服务，支持外网访问
"""

import json
import os
import pandas as pd
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from datetime import datetime
from typing import Dict, List, Optional
import uvicorn

app = FastAPI(title="Nobel订单管理系统")

# 尝试连接 Supabase
SUPABASE_URL = os.getenv("COZE_SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("COZE_SUPABASE_ANON_KEY")

# 数据存储
users_db = [
    {"id": 1, "username": "admin", "password": "admin123", "role": "管理员"}
]

customers_db = []
orders_db = []

# 尝试从 Supabase 加载数据
if SUPABASE_URL and SUPABASE_ANON_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

        # 加载用户
        users_response = supabase.table('users').select('*').execute()
        if users_response.data:
            users_db = users_response.data

        # 加载客户
        customers_response = supabase.table('customers').select('*').execute()
        if customers_response.data:
            customers_db = customers_response.data

        # 加载订单
        orders_response = supabase.table('orders').select('*').execute()
        if orders_response.data:
            orders_db = orders_response.data

        USE_SUPABASE = True
    except Exception as e:
        print(f"Supabase 连接失败: {e}")
        USE_SUPABASE = False
else:
    USE_SUPABASE = False

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nobel订单管理系统</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .btn-primary { background: #FF6B35; color: white; }
        .btn-primary:hover { background: #e55a2b; }
        .card { box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; }
    </style>
</head>
<body class="bg-gray-100 min-h-screen">
    <!-- 登录页面 -->
    <div id="login-page" class="min-h-screen flex items-center justify-center">
        <div class="bg-white p-8 rounded-lg card w-96">
            <h1 class="text-2xl font-bold text-center mb-6 text-gray-800">Nobel订单管理系统</h1>
            <form id="login-form">
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">用户名</label>
                    <input type="text" id="username" class="w-full p-2 border rounded" required value="admin">
                </div>
                <div class="mb-6">
                    <label class="block text-sm font-medium mb-2">密码</label>
                    <input type="password" id="password" class="w-full p-2 border rounded" required value="admin123">
                </div>
                <button type="submit" class="w-full btn-primary py-2 rounded font-medium">登录</button>
            </form>
            <div id="login-error" class="text-red-500 text-sm mt-3 text-center hidden">用户名或密码错误</div>
        </div>
    </div>

    <!-- 主页面 -->
    <div id="main-page" class="hidden">
        <nav class="bg-white shadow-md">
            <div class="max-w-7xl mx-auto px-4">
                <div class="flex justify-between items-center py-4">
                    <h1 class="text-xl font-bold text-gray-800">Nobel订单管理系统</h1>
                    <div class="flex items-center gap-4">
                        <span id="user-info" class="text-gray-600"></span>
                        <button onclick="logout()" class="text-red-500 hover:text-red-700">退出</button>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto px-4 py-6">
            <!-- 选项卡 -->
            <div class="flex gap-4 mb-6">
                <button onclick="switchTab('dashboard')" class="tab-btn px-4 py-2 rounded bg-white" data-tab="dashboard">仪表盘</button>
                <button onclick="switchTab('customers')" class="tab-btn px-4 py-2 rounded bg-white" data-tab="customers">客户管理</button>
                <button onclick="switchTab('orders')" class="tab-btn px-4 py-2 rounded bg-white" data-tab="orders">订单管理</button>
            </div>

            <!-- 仪表盘 -->
            <div id="dashboard-content" class="tab-content">
                <div class="grid grid-cols-3 gap-4 mb-6">
                    <div class="bg-white p-6 rounded card">
                        <h3 class="text-gray-500 text-sm">客户总数</h3>
                        <p id="stat-customers" class="text-3xl font-bold text-blue-600">0</p>
                    </div>
                    <div class="bg-white p-6 rounded card">
                        <h3 class="text-gray-500 text-sm">订单总数</h3>
                        <p id="stat-orders" class="text-3xl font-bold text-green-600">0</p>
                    </div>
                    <div class="bg-white p-6 rounded card">
                        <h3 class="text-gray-500 text-sm">总金额</h3>
                        <p id="stat-amount" class="text-3xl font-bold text-orange-600">¥0</p>
                    </div>
                </div>
            </div>

            <!-- 客户管理 -->
            <div id="customers-content" class="tab-content hidden">
                <div class="bg-white rounded card p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-bold">客户列表</h2>
                        <button onclick="showAddCustomer()" class="btn-primary px-4 py-2 rounded">添加客户</button>
                    </div>
                    <table class="w-full">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-4 py-2 text-left">ID</th>
                                <th class="px-4 py-2 text-left">客户代码</th>
                                <th class="px-4 py-2 text-left">地区</th>
                                <th class="px-4 py-2 text-left">创建时间</th>
                                <th class="px-4 py-2 text-left">操作</th>
                            </tr>
                        </thead>
                        <tbody id="customers-table"></tbody>
                    </table>
                </div>
            </div>

            <!-- 订单管理 -->
            <div id="orders-content" class="tab-content hidden">
                <div class="bg-white rounded card p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-bold">订单列表</h2>
                        <button onclick="showAddOrder()" class="btn-primary px-4 py-2 rounded">添加订单</button>
                    </div>
                    <table class="w-full">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-4 py-2 text-left">订单号</th>
                                <th class="px-4 py-2 text-left">客户</th>
                                <th class="px-4 py-2 text-left">订单内容</th>
                                <th class="px-4 py-2 text-left">金额</th>
                                <th class="px-4 py-2 text-left">状态</th>
                                <th class="px-4 py-2 text-left">创建时间</th>
                                <th class="px-4 py-2 text-left">操作</th>
                            </tr>
                        </thead>
                        <tbody id="orders-table"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentUser = null;
        let customers = [];
        let orders = [];

        // 登录处理
        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (data.success) {
                currentUser = data.user;
                document.getElementById('login-page').classList.add('hidden');
                document.getElementById('main-page').classList.remove('hidden');
                document.getElementById('user-info').textContent = `欢迎, ${currentUser.username}`;
                loadDashboard();
            } else {
                document.getElementById('login-error').classList.remove('hidden');
            }
        });

        function logout() {
            currentUser = null;
            document.getElementById('main-page').classList.add('hidden');
            document.getElementById('login-page').classList.remove('hidden');
        }

        function switchTab(tab) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('bg-orange-500', 'text-white'));
            
            document.getElementById(tab + '-content').classList.remove('hidden');
            document.querySelector(`[data-tab="${tab}"]`).classList.add('bg-orange-500', 'text-white');

            if (tab === 'dashboard') loadDashboard();
            if (tab === 'customers') loadCustomers();
            if (tab === 'orders') loadOrders();
        }

        async function loadDashboard() {
            const response = await fetch('/api/stats');
            const data = await response.json();
            document.getElementById('stat-customers').textContent = data.customers;
            document.getElementById('stat-orders').textContent = data.orders;
            document.getElementById('stat-amount').textContent = '¥' + data.total_amount.toLocaleString();
        }

        async function loadCustomers() {
            const response = await fetch('/api/customers');
            customers = await response.json();
            const tbody = document.getElementById('customers-table');
            tbody.innerHTML = customers.map(c => `
                <tr class="border-b">
                    <td class="px-4 py-2">${c.id}</td>
                    <td class="px-4 py-2">${c.code}</td>
                    <td class="px-4 py-2">${c.region}</td>
                    <td class="px-4 py-2">${c.created_at}</td>
                    <td class="px-4 py-2">
                        <button onclick="deleteCustomer(${c.id})" class="text-red-500 hover:text-red-700">删除</button>
                    </td>
                </tr>
            `).join('');
        }

        async function loadOrders() {
            const response = await fetch('/api/orders');
            orders = await response.json();
            const tbody = document.getElementById('orders-table');
            tbody.innerHTML = orders.map(o => `
                <tr class="border-b">
                    <td class="px-4 py-2">${o.order_no}</td>
                    <td class="px-4 py-2">${o.customer_name || '未指定'}</td>
                    <td class="px-4 py-2">${o.content}</td>
                    <td class="px-4 py-2">¥${o.amount.toLocaleString()}</td>
                    <td class="px-4 py-2">${o.status}</td>
                    <td class="px-4 py-2">${o.created_at}</td>
                    <td class="px-4 py-2">
                        <button onclick="deleteOrder(${o.id})" class="text-red-500 hover:text-red-700">删除</button>
                    </td>
                </tr>
            `).join('');
        }

        function showAddCustomer() {
            const code = prompt('客户代码:');
            if (!code) return;
            const region = prompt('地区:');
            if (!region) return;

            fetch('/api/customers', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, region })
            }).then(() => loadCustomers());
        }

        function showAddOrder() {
            const content = prompt('订单内容:');
            if (!content) return;
            const amount = parseFloat(prompt('金额:'));
            if (isNaN(amount)) return;

            fetch('/api/orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content, amount, status: '待处理' })
            }).then(() => loadOrders());
        }

        async function deleteCustomer(id) {
            if (!confirm('确认删除?')) return;
            await fetch(`/api/customers/${id}`, { method: 'DELETE' });
            loadCustomers();
        }

        async function deleteOrder(id) {
            if (!confirm('确认删除?')) return;
            await fetch(`/api/orders/${id}`, { method: 'DELETE' });
            loadOrders();
        }
    </script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=HTML_TEMPLATE)

@app.post("/api/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    for user in users_db:
        if user["username"] == username and user["password"] == password:
            return {"success": True, "user": user}

    return {"success": False}

@app.get("/api/customers")
async def get_customers():
    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        response = supabase.table('customers').select('*').execute()
        return response.data
    return customers_db

@app.post("/api/customers")
async def create_customer(request: Request):
    data = await request.json()
    customer = {
        "id": len(customers_db) + 1,
        "code": data.get("code"),
        "region": data.get("region"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        supabase.table('customers').insert(customer).execute()
    else:
        customers_db.append(customer)

    return customer

@app.delete("/api/customers/{customer_id}")
async def delete_customer(customer_id: int):
    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        supabase.table('customers').delete().eq('id', customer_id).execute()
    else:
        global customers_db
        customers_db = [c for c in customers_db if c["id"] != customer_id]

    return {"success": True}

@app.get("/api/orders")
async def get_orders():
    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        response = supabase.table('orders').select('*').execute()
        return response.data
    return orders_db

@app.post("/api/orders")
async def create_order(request: Request):
    data = await request.json()
    order = {
        "id": len(orders_db) + 1,
        "order_no": f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "content": data.get("content"),
        "amount": data.get("amount", 0),
        "status": data.get("status", "待处理"),
        "customer_name": data.get("customer_name"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        supabase.table('orders').insert(order).execute()
    else:
        orders_db.append(order)

    return order

@app.delete("/api/orders/{order_id}")
async def delete_order(order_id: int):
    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        supabase.table('orders').delete().eq('id', order_id).execute()
    else:
        global orders_db
        orders_db = [o for o in orders_db if o["id"] != order_id]

    return {"success": True}

@app.get("/api/stats")
async def get_stats():
    all_orders = await get_orders()
    all_customers = await get_customers()

    total_amount = sum(o.get("amount", 0) for o in all_orders)

    return {
        "customers": len(all_customers),
        "orders": len(all_orders),
        "total_amount": total_amount
    }

if __name__ == "__main__":
    print("🚀 启动 Nobel订单管理系统 - HTTP服务版")
    print(f"📊 使用 Supabase: {USE_SUPABASE}")
    print("🌐 访问地址: http://0.0.0.0:9002")
    print("🔐 默认账号: admin / admin123")
    uvicorn.run(app, host="0.0.0.0", port=9002)
