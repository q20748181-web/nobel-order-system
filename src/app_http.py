#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nobel订单管理系统 - 完整版（参考 v2.1）
支持客户管理、打样订单、设计报价、正式订单、售后服务、用户管理、数据导出
"""

import json
import os
import base64
import io
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
from typing import Dict, List, Optional
import uvicorn

app = FastAPI(title="Nobel订单管理系统 V2.1")

# 尝试连接 Supabase
SUPABASE_URL = os.getenv("COZE_SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("COZE_SUPABASE_ANON_KEY")

# 默认用户
default_users = [
    {"id": 1, "username": "admin", "password": "admin123", "role": "管理员", "permissions": {"edit": True, "delete": True, "upload": True, "download": True, "manageUsers": True}}
]

users_db = []
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
            print(f"📋 从 Supabase 加载了 {len(users_db)} 个用户")
        else:
            users_db = default_users
            print(f"📋 使用默认用户数据")

        # 加载客户
        customers_response = supabase.table('customers').select('*').execute()
        if customers_response.data:
            customers_db = customers_response.data
            print(f"📋 从 Supabase 加载了 {len(customers_db)} 个客户")

        # 加载订单
        orders_response = supabase.table('orders').select('*').execute()
        if orders_response.data:
            orders_db = orders_response.data
            print(f"📋 从 Supabase 加载了 {len(orders_db)} 个订单")

        USE_SUPABASE = True
        print(f"✅ 已连接 Supabase")
    except Exception as e:
        print(f"⚠️ Supabase 连接失败: {e}")
        USE_SUPABASE = False
else:
    USE_SUPABASE = False
    print("📝 使用本地存储模式")

# HTML 模板（基于参考系统的 v2.1 设计）
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nobel订单管理</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif; background: #f5f7fa; min-height: 100vh; color: #333; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        
        /* 登录页 */
        .login-section { background: white; padding: 50px; border-radius: 16px; max-width: 450px; margin: 80px auto; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .login-section h2 { text-align: center; color: #667eea; margin-bottom: 30px; font-size: 32px; font-weight: 700; }
        
        /* 表单 */
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #555; font-size: 14px; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 12px 16px; border: 2px solid #e1e8ed; border-radius: 8px; font-size: 14px; transition: all 0.3s; background: white; }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        .form-group textarea { height: 100px; resize: vertical; }
        .hint { color: #999; font-size: 13px; margin-top: 6px; font-style: italic; }
        
        /* 按钮 */
        .btn { padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600; transition: all 0.3s; display: inline-flex; align-items: center; gap: 8px; }
        .btn-primary { background: #667eea; color: white; }
        .btn-primary:hover { background: #5568d3; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
        .btn-danger { background: #e74c3c; color: white; }
        .btn-danger:hover { background: #c0392b; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4); }
        .btn-success { background: #2ecc71; color: white; }
        .btn-success:hover { background: #27ae60; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(46, 204, 113, 0.4); }
        .btn-secondary { background: #95a5a6; color: white; }
        .btn-secondary:hover { background: #7f8c8d; }
        
        /* 主内容 */
        .main-content { display: none; animation: fadeIn 0.3s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        /* 头部 */
        .header { background: white; padding: 25px 30px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; }
        .header h1 { color: #667eea; margin-bottom: 5px; font-size: 28px; }
        
        /* 仪表板 */
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .dashboard-card { background: white; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: all 0.3s; cursor: pointer; }
        .dashboard-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
        .dashboard-card h3 { font-size: 48px; color: #667eea; margin-bottom: 8px; font-weight: 700; }
        .dashboard-card p { color: #888; font-size: 14px; font-weight: 500; }
        
        /* 选项卡 */
        .tabs { display: flex; gap: 8px; margin-bottom: 25px; flex-wrap: wrap; background: white; padding: 10px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .tab { padding: 12px 20px; background: transparent; border-radius: 8px; cursor: pointer; transition: all 0.3s; color: #666; font-weight: 600; font-size: 14px; border: 2px solid transparent; display: flex; align-items: center; gap: 8px; }
        .tab:hover { background: #f0f0f0; color: #667eea; }
        .tab.active { background: #667eea; color: white; border-color: #667eea; }
        .tab-content { display: none; animation: fadeIn 0.3s ease-in-out; }
        .tab-content.active { display: block; }
        
        /* 卡片 */
        .card { background: white; padding: 25px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: all 0.3s; }
        .card:hover { box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .card h3 { color: #333; margin-bottom: 15px; font-size: 18px; font-weight: 600; }
        
        /* 状态标签 */
        .status-badge { padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-processing { background: #cce5ff; color: #004085; }
        .status-completed { background: #d4edda; color: #155724; }
        .status-cancelled { background: #f8d7da; color: #721c24; }
        
        /* Logo预览 */
        .logo-preview { width: 70px; height: 70px; object-fit: cover; border-radius: 8px; border: 3px solid #e1e8ed; background: #f8f9fa; }
        
        /* 搜索框 */
        .search-box { margin-bottom: 20px; }
        .search-box input { width: 100%; padding: 14px 20px; border: 2px solid #e1e8ed; border-radius: 10px; font-size: 14px; transition: all 0.3s; }
        .search-box input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        
        /* 表格 */
        .data-table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .data-table th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px; text-align: left; font-weight: 600; font-size: 14px; }
        .data-table td { padding: 16px; border-bottom: 1px solid #e1e8ed; color: #666; font-size: 14px; }
        .data-table tr:hover { background: #f8f9fa; }
        
        /* 表单弹窗 */
        .form-modal { display: none; background: rgba(0,0,0,0.5); position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 1000; align-items: center; justify-content: center; }
        .form-modal.active { display: flex; }
        .form-modal-content { background: white; padding: 30px; border-radius: 16px; width: 90%; max-width: 500px; max-height: 90vh; overflow-y: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.2); animation: slideIn 0.3s ease-in-out; }
        @keyframes slideIn { from { transform: translateY(-20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .form-modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .form-modal-header h3 { color: #667eea; font-size: 24px; font-weight: 700; }
        .close-btn { background: none; border: none; font-size: 28px; color: #999; cursor: pointer; transition: all 0.3s; }
        .close-btn:hover { color: #667eea; }
        
        /* 隐藏 */
        .hide { display: none !important; }
        
        /* 空状态 */
        .empty-state { text-align: center; padding: 60px 20px; color: #999; }
        .empty-state p { font-size: 16px; }
    </style>
</head>
<body>
    <!-- 登录页面 -->
    <div class="login-section" id="loginSection">
        <h2>🏠 Nobel订单管理</h2>
        <form id="loginForm">
            <div class="form-group">
                <label>用户名</label>
                <input type="text" id="loginUsername" required placeholder="请输入用户名" value="admin">
            </div>
            <div class="form-group">
                <label>密码</label>
                <input type="password" id="loginPassword" required placeholder="请输入密码" value="admin123">
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center;">登录</button>
        </form>
    </div>

    <!-- 主内容 -->
    <div class="main-content" id="mainContent">
        <div class="container">
            <!-- 头部 -->
            <div class="header">
                <div>
                    <h1>🏠 Nobel订单管理</h1>
                    <p id="welcomeMessage">欢迎回来，管理员</p>
                </div>
                <button class="btn btn-secondary" onclick="logout()">退出登录</button>
            </div>

            <!-- 仪表盘 -->
            <div class="dashboard">
                <div class="dashboard-card" onclick="switchTab('customers')">
                    <h3 id="totalCustomers">0</h3>
                    <p>👥 客户总数</p>
                </div>
                <div class="dashboard-card" onclick="switchTab('sample')">
                    <h3 id="totalSampleOrders">0</h3>
                    <p>🎨 打样订单</p>
                </div>
                <div class="dashboard-card" onclick="switchTab('design')">
                    <h3 id="totalDesignOrders">0</h3>
                    <p>💡 设计报价</p>
                </div>
                <div class="dashboard-card" onclick="switchTab('formal')">
                    <h3 id="totalFormalOrders">0</h3>
                    <p>📦 正式订单</p>
                </div>
            </div>

            <!-- 选项卡 -->
            <div class="tabs">
                <div class="tab active" onclick="switchTab('customers')"><span>👥</span> 客户管理</div>
                <div class="tab" onclick="switchTab('sample')"><span>🎨</span> 打样订单</div>
                <div class="tab" onclick="switchTab('design')"><span>💡</span> 设计报价</div>
                <div class="tab" onclick="switchTab('formal')"><span>📦</span> 正式订单</div>
                <div class="tab" onclick="switchTab('aftersale')"><span>🔧</span> 售后服务</div>
                <div class="tab" onclick="switchTab('users')"><span>👤</span> 用户管理</div>
                <div class="tab" onclick="switchTab('data')"><span>📊</span> 数据导出</div>
            </div>

            <!-- 客户管理 -->
            <div class="tab-content active" id="customers">
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 style="font-size: 24px; color: #333;">👥 客户列表</h2>
                        <button class="btn btn-primary" onclick="showCustomerModal()">➕ 添加客户</button>
                    </div>
                    <div class="search-box">
                        <input type="text" id="searchCustomers" placeholder="🔍 搜索客户名称或地区..." oninput="filterCustomers()">
                    </div>
                    <table class="data-table" id="customerTable">
                        <thead>
                            <tr>
                                <th>Logo</th>
                                <th>客户编号</th>
                                <th>地区</th>
                                <th>创建时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="customerList"></tbody>
                    </table>
                </div>
            </div>

            <!-- 打样订单 -->
            <div class="tab-content" id="sample">
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 style="font-size: 24px; color: #333;">🎨 打样订单</h2>
                        <button class="btn btn-primary" onclick="showOrderModal('sample')">➕ 创建订单</button>
                    </div>
                    <div class="search-box">
                        <input type="text" id="searchSample" placeholder="🔍 搜索订单号或内容..." oninput="filterOrders('sample')">
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>订单号</th>
                                <th>客户</th>
                                <th>订单内容</th>
                                <th>金额</th>
                                <th>状态</th>
                                <th>创建时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="sampleOrderList"></tbody>
                    </table>
                </div>
            </div>

            <!-- 设计报价 -->
            <div class="tab-content" id="design">
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 style="font-size: 24px; color: #333;">💡 设计报价</h2>
                        <button class="btn btn-primary" onclick="showOrderModal('design')">➕ 创建报价</button>
                    </div>
                    <div class="search-box">
                        <input type="text" id="searchDesign" placeholder="🔍 搜索报价号或内容..." oninput="filterOrders('design')">
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>报价号</th>
                                <th>客户</th>
                                <th>报价内容</th>
                                <th>金额</th>
                                <th>状态</th>
                                <th>创建时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="designOrderList"></tbody>
                    </table>
                </div>
            </div>

            <!-- 正式订单 -->
            <div class="tab-content" id="formal">
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 style="font-size: 24px; color: #333;">📦 正式订单</h2>
                        <button class="btn btn-primary" onclick="showOrderModal('formal')">➕ 创建订单</button>
                    </div>
                    <div class="search-box">
                        <input type="text" id="searchFormal" placeholder="🔍 搜索订单号或内容..." oninput="filterOrders('formal')">
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>订单号</th>
                                <th>客户</th>
                                <th>订单内容</th>
                                <th>金额</th>
                                <th>状态</th>
                                <th>创建时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="formalOrderList"></tbody>
                    </table>
                </div>
            </div>

            <!-- 售后服务 -->
            <div class="tab-content" id="aftersale">
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 style="font-size: 24px; color: #333;">🔧 售后服务</h2>
                        <button class="btn btn-primary" onclick="showOrderModal('aftersale')">➕ 创建售后</button>
                    </div>
                    <div class="search-box">
                        <input type="text" id="searchAftersale" placeholder="🔍 搜索售后号或内容..." oninput="filterOrders('aftersale')">
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>售后号</th>
                                <th>客户</th>
                                <th>售后内容</th>
                                <th>金额</th>
                                <th>状态</th>
                                <th>创建时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="aftersaleOrderList"></tbody>
                    </table>
                </div>
            </div>

            <!-- 用户管理 -->
            <div class="tab-content" id="users">
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 style="font-size: 24px; color: #333;">👤 用户管理</h2>
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>用户名</th>
                                <th>角色</th>
                                <th>创建时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="userList"></tbody>
                    </table>
                </div>
            </div>

            <!-- 数据导出 -->
            <div class="tab-content" id="data">
                <div class="card">
                    <h2 style="font-size: 24px; color: #333; margin-bottom: 20px;">📊 数据导出</h2>
                    <div style="display: flex; flex-direction: column; gap: 15px;">
                        <button class="btn btn-primary" onclick="exportData()" style="justify-content: center;">📥 导出数据（JSON）</button>
                        <p style="color: #666; font-size: 14px;">将所有客户、订单和用户数据导出为 JSON 文件</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 客户表单弹窗 -->
    <div class="form-modal" id="customerModal">
        <div class="form-modal-content">
            <div class="form-modal-header">
                <h3 id="customerModalTitle">添加客户</h3>
                <button class="close-btn" onclick="hideCustomerModal()">&times;</button>
            </div>
            <form id="customerForm">
                <input type="hidden" id="editCustomerId">
                <div class="form-group">
                    <label>客户编号 *</label>
                    <input type="text" id="customerCode" required placeholder="如：C001">
                    <p class="hint">客户唯一标识，建议使用字母+数字组合</p>
                </div>
                <div class="form-group">
                    <label>地区 *</label>
                    <input type="text" id="customerRegion" required placeholder="如：北京朝阳区">
                </div>
                <div class="form-group">
                    <label>客户Logo</label>
                    <input type="file" id="customerLogo" accept="image/*" onchange="previewLogo(this)">
                    <p class="hint">支持 JPG、PNG 格式</p>
                </div>
                <div id="logoPreviewContainer" class="hide" style="margin-bottom: 15px;">
                    <img id="logoPreview" class="logo-preview" src="" alt="Logo预览">
                </div>
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button type="submit" class="btn btn-primary" style="flex: 1; justify-content: center;">保存</button>
                    <button type="button" class="btn btn-secondary" onclick="hideCustomerModal()" style="flex: 1; justify-content: center;">取消</button>
                </div>
            </form>
        </div>
    </div>

    <!-- 订单表单弹窗 -->
    <div class="form-modal" id="orderModal">
        <div class="form-modal-content">
            <div class="form-modal-header">
                <h3 id="orderModalTitle">创建订单</h3>
                <button class="close-btn" onclick="hideOrderModal()">&times;</button>
            </div>
            <form id="orderForm">
                <input type="hidden" id="orderType">
                <input type="hidden" id="editOrderId">
                <div class="form-group">
                    <label>客户 *</label>
                    <select id="orderCustomerId" required>
                        <option value="">请选择客户</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>订单内容 *</label>
                    <textarea id="orderContent" required placeholder="请输入订单内容"></textarea>
                </div>
                <div class="form-group">
                    <label>金额 (元) *</label>
                    <input type="number" id="orderAmount" required min="0" step="0.01" placeholder="0.00">
                </div>
                <div class="form-group">
                    <label>状态</label>
                    <select id="orderStatus">
                        <option value="pending">待处理</option>
                        <option value="processing">处理中</option>
                        <option value="completed">已完成</option>
                        <option value="cancelled">已取消</option>
                    </select>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button type="submit" class="btn btn-primary" style="flex: 1; justify-content: center;">保存</button>
                    <button type="button" class="btn btn-secondary" onclick="hideOrderModal()" style="flex: 1; justify-content: center;">取消</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // 检测是否需要添加路径前缀（用于外网访问）
        const isExternal = window.location.pathname.startsWith('/nobel');
        const API_BASE = isExternal ? '/nobel' : '';

        let currentUser = null;
        let customers = [];
        let orders = [];
        let users = [];

        // 登录处理
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            const response = await fetch(API_BASE + '/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (data.success) {
                currentUser = data.user;
                document.getElementById('loginSection').style.display = 'none';
                document.getElementById('mainContent').style.display = 'block';
                document.getElementById('welcomeMessage').textContent = `欢迎回来，${currentUser.username}`;
                loadAllData();
            } else {
                alert('用户名或密码错误！');
            }
        });

        function logout() {
            currentUser = null;
            document.getElementById('mainContent').style.display = 'none';
            document.getElementById('loginSection').style.display = 'block';
        }

        // 加载所有数据
        async function loadAllData() {
            await Promise.all([
                loadCustomers(),
                loadOrders(),
                loadUsers()
            ]);
            updateDashboard();
        }

        // 切换标签页
        function switchTab(tabId) {
            // 移除所有tab的active状态
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            // 移除所有tab-content的active状态
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

            // 找到对应的tab按钮并设置为active
            const tabButton = document.querySelector('.tab[onclick="switchTab(\'' + tabId + '\')"]');
            if (tabButton) {
                tabButton.classList.add('active');
            }

            // 激活对应的tab-content
            document.getElementById(tabId).classList.add('active');

            if (tabId === 'customers') renderCustomers();
            if (['sample', 'design', 'formal', 'aftersale'].includes(tabId)) renderOrders(tabId);
            if (tabId === 'users') renderUsers();
        }

        // 加载客户
        async function loadCustomers() {
            const response = await fetch(API_BASE + '/api/customers');
            customers = await response.json();
        }

        // 加载订单
        async function loadOrders() {
            const response = await fetch(API_BASE + '/api/orders');
            orders = await response.json();
        }

        // 加载用户
        async function loadUsers() {
            const response = await fetch(API_BASE + '/api/users');
            users = await response.json();
        }

        // 更新仪表盘
        function updateDashboard() {
            document.getElementById('totalCustomers').textContent = customers.length;
            document.getElementById('totalSampleOrders').textContent = orders.filter(o => o.type === 'sample').length;
            document.getElementById('totalDesignOrders').textContent = orders.filter(o => o.type === 'design').length;
            document.getElementById('totalFormalOrders').textContent = orders.filter(o => o.type === 'formal').length;
        }

        // 渲染客户列表
        function renderCustomers(filter = '') {
            const filtered = customers.filter(c => 
                c.code.toLowerCase().includes(filter.toLowerCase()) || 
                c.region.toLowerCase().includes(filter.toLowerCase())
            );

            const tbody = document.getElementById('customerList');
            if (filtered.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="empty-state"><p>暂无客户数据</p></td></tr>';
                return;
            }

            tbody.innerHTML = filtered.map(c => {
                const logoHtml = c.logo ? `<img src="data:image/png;base64,${c.logo}" class="logo-preview">` : '<div class="logo-preview" style="display: flex; align-items: center; justify-content: center; color: #999; font-size: 12px;">无Logo</div>';
                return `
                    <tr>
                        <td>${logoHtml}</td>
                        <td>${c.code}</td>
                        <td>${c.region}</td>
                        <td>${c.created_at || '-'}</td>
                        <td>
                            <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 12px;" onclick="editCustomer(${c.id})">编辑</button>
                            <button class="btn btn-danger" style="padding: 6px 12px; font-size: 12px;" onclick="deleteCustomer(${c.id})">删除</button>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        // 渲染订单列表
        function renderOrders(type, filter = '') {
            const filtered = orders.filter(o => 
                o.type === type && 
                (o.order_no.toLowerCase().includes(filter.toLowerCase()) || 
                 o.content.toLowerCase().includes(filter.toLowerCase()))
            );

            const tbody = document.getElementById(type + 'OrderList');
            if (filtered.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><p>暂无订单数据</p></td></tr>';
                return;
            }

            const statusLabels = {
                'pending': '待处理',
                'processing': '处理中',
                'completed': '已完成',
                'cancelled': '已取消'
            };

            tbody.innerHTML = filtered.map(o => {
                const customer = customers.find(c => c.id === o.customer_id);
                return `
                    <tr>
                        <td>${o.order_no}</td>
                        <td>${customer ? customer.code : '-'}</td>
                        <td>${o.content}</td>
                        <td>¥${o.amount.toLocaleString()}</td>
                        <td><span class="status-badge status-${o.status}">${statusLabels[o.status]}</span></td>
                        <td>${o.created_at || '-'}</td>
                        <td>
                            <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 12px;" onclick="editOrder(${o.id})">编辑</button>
                            <button class="btn btn-danger" style="padding: 6px 12px; font-size: 12px;" onclick="deleteOrder(${o.id})">删除</button>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        // 渲染用户列表
        function renderUsers() {
            const tbody = document.getElementById('userList');
            tbody.innerHTML = users.map(u => `
                <tr>
                    <td>${u.id}</td>
                    <td>${u.username}</td>
                    <td>${u.role}</td>
                    <td>${u.created_at || '-'}</td>
                    <td>
                        ${u.username !== 'admin' ? `<button class="btn btn-danger" style="padding: 6px 12px; font-size: 12px;" onclick="deleteUser(${u.id})">删除</button>` : '-'}
                    </td>
                </tr>
            `).join('');
        }

        // 客户相关函数
        function showCustomerModal() {
            document.getElementById('editCustomerId').value = '';
            document.getElementById('customerCode').value = '';
            document.getElementById('customerRegion').value = '';
            document.getElementById('customerLogo').value = '';
            document.getElementById('logoPreviewContainer').classList.add('hide');
            document.getElementById('customerModalTitle').textContent = '添加客户';
            document.getElementById('customerModal').classList.add('active');
        }

        function hideCustomerModal() {
            document.getElementById('customerModal').classList.remove('active');
        }

        function previewLogo(input) {
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('logoPreview').src = e.target.result;
                    document.getElementById('logoPreviewContainer').classList.remove('hide');
                    document.getElementById('logoPreview').dataset.base64 = e.target.result.split(',')[1];
                };
                reader.readAsDataURL(input.files[0]);
            }
        }

        document.getElementById('customerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const id = document.getElementById('editCustomerId').value;
            const code = document.getElementById('customerCode').value;
            const region = document.getElementById('customerRegion').value;
            const logoPreview = document.getElementById('logoPreview');
            const logo = logoPreview.dataset.base64 || '';

            const customer = { code, region, logo };

            if (id) {
                await fetch(API_BASE + `/api/customers/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(customer)
                });
            } else {
                await fetch(API_BASE + '/api/customers', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(customer)
                });
            }

            hideCustomerModal();
            await loadCustomers();
            renderCustomers();
        });

        async function editCustomer(id) {
            const customer = customers.find(c => c.id === id);
            if (!customer) return;

            document.getElementById('editCustomerId').value = id;
            document.getElementById('customerCode').value = customer.code;
            document.getElementById('customerRegion').value = customer.region;
            document.getElementById('customerModalTitle').textContent = '编辑客户';

            if (customer.logo) {
                document.getElementById('logoPreview').src = 'data:image/png;base64,' + customer.logo;
                document.getElementById('logoPreviewContainer').classList.remove('hide');
            } else {
                document.getElementById('logoPreviewContainer').classList.add('hide');
            }

            document.getElementById('customerModal').classList.add('active');
        }

        async function deleteCustomer(id) {
            if (!confirm('确认删除此客户？')) return;
            await fetch(API_BASE + `/api/customers/${id}`, { method: 'DELETE' });
            await loadCustomers();
            renderCustomers();
        }

        // 订单相关函数
        function showOrderModal(type) {
            document.getElementById('orderType').value = type;
            document.getElementById('editOrderId').value = '';
            document.getElementById('orderCustomerId').value = '';
            document.getElementById('orderContent').value = '';
            document.getElementById('orderAmount').value = '';
            document.getElementById('orderStatus').value = 'pending';

            // 填充客户选项
            const select = document.getElementById('orderCustomerId');
            select.innerHTML = '<option value="">请选择客户</option>';
            customers.forEach(c => {
                select.innerHTML += `<option value="${c.id}">${c.code} - ${c.region}</option>`;
            });

            const titles = {
                'sample': '创建打样订单',
                'design': '创建设计报价',
                'formal': '创建正式订单',
                'aftersale': '创建售后服务'
            };
            document.getElementById('orderModalTitle').textContent = titles[type];
            document.getElementById('orderModal').classList.add('active');
        }

        function hideOrderModal() {
            document.getElementById('orderModal').classList.remove('active');
        }

        document.getElementById('orderForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const id = document.getElementById('editOrderId').value;
            const type = document.getElementById('orderType').value;
            const customer_id = parseInt(document.getElementById('orderCustomerId').value);
            const content = document.getElementById('orderContent').value;
            const amount = parseFloat(document.getElementById('orderAmount').value);
            const status = document.getElementById('orderStatus').value;

            const order = { type, customer_id, content, amount, status };

            if (id) {
                await fetch(API_BASE + `/api/orders/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(order)
                });
            } else {
                await fetch(API_BASE + '/api/orders', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(order)
                });
            }

            hideOrderModal();
            await loadOrders();
            renderOrders(type);
            updateDashboard();
        });

        async function editOrder(id) {
            const order = orders.find(o => o.id === id);
            if (!order) return;

            document.getElementById('orderType').value = order.type;
            document.getElementById('editOrderId').value = id;
            document.getElementById('orderCustomerId').value = order.customer_id;
            document.getElementById('orderContent').value = order.content;
            document.getElementById('orderAmount').value = order.amount;
            document.getElementById('orderStatus').value = order.status;

            // 填充客户选项
            const select = document.getElementById('orderCustomerId');
            select.innerHTML = '<option value="">请选择客户</option>';
            customers.forEach(c => {
                select.innerHTML += `<option value="${c.id}">${c.code} - ${c.region}</option>`;
            });

            const titles = {
                'sample': '编辑打样订单',
                'design': '编辑设计报价',
                'formal': '编辑正式订单',
                'aftersale': '编辑售后服务'
            };
            document.getElementById('orderModalTitle').textContent = titles[order.type];
            document.getElementById('orderModal').classList.add('active');
        }

        async function deleteOrder(id) {
            if (!confirm('确认删除此订单？')) return;
            await fetch(API_BASE + `/api/orders/${id}`, { method: 'DELETE' });
            await loadOrders();
            document.querySelectorAll('.tab-content.active').forEach(c => {
                if (c.id === 'sample') renderOrders('sample');
                if (c.id === 'design') renderOrders('design');
                if (c.id === 'formal') renderOrders('formal');
                if (c.id === 'aftersale') renderOrders('aftersale');
            });
            updateDashboard();
        }

        async function deleteUser(id) {
            if (!confirm('确认删除此用户？')) return;
            await fetch(API_BASE + `/api/users/${id}`, { method: 'DELETE' });
            await loadUsers();
            renderUsers();
        }

        // 搜索过滤
        function filterCustomers() {
            const filter = document.getElementById('searchCustomers').value;
            renderCustomers(filter);
        }

        function filterOrders(type) {
            const filter = document.getElementById('search' + type.charAt(0).toUpperCase() + type.slice(1)).value;
            renderOrders(type, filter);
        }

        // 数据导出
        async function exportData() {
            const response = await fetch(API_BASE + '/api/export');
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'nobel_order_system_export_' + new Date().toISOString().slice(0,10) + '.json';
            a.click();
            URL.revokeObjectURL(url);
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
        "logo": data.get("logo", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        supabase.table('customers').insert(customer).execute()
    else:
        customers_db.append(customer)

    return customer

@app.put("/api/customers/{customer_id}")
async def update_customer(customer_id: int, request: Request):
    data = await request.json()

    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        supabase.table('customers').update({
            "code": data.get("code"),
            "region": data.get("region"),
            "logo": data.get("logo", "")
        }).eq('id', customer_id).execute()
    else:
        global customers_db
        for i, c in enumerate(customers_db):
            if c["id"] == customer_id:
                customers_db[i].update(data)
                break

    return {"success": True}

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
    order_type = data.get("type", "formal")

    order = {
        "id": len(orders_db) + 1,
        "order_no": f"{order_type.upper()}{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "type": order_type,
        "customer_id": data.get("customer_id"),
        "content": data.get("content"),
        "amount": data.get("amount", 0),
        "status": data.get("status", "pending"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        supabase.table('orders').insert(order).execute()
    else:
        orders_db.append(order)

    return order

@app.put("/api/orders/{order_id}")
async def update_order(order_id: int, request: Request):
    data = await request.json()

    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        supabase.table('orders').update({
            "customer_id": data.get("customer_id"),
            "content": data.get("content"),
            "amount": data.get("amount"),
            "status": data.get("status")
        }).eq('id', order_id).execute()
    else:
        global orders_db
        for i, o in enumerate(orders_db):
            if o["id"] == order_id:
                orders_db[i].update(data)
                break

    return {"success": True}

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

@app.get("/api/users")
async def get_users():
    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        response = supabase.table('users').select('*').execute()
        return response.data
    return users_db

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    if USE_SUPABASE:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        supabase.table('users').delete().eq('id', user_id).execute()
    else:
        global users_db
        users_db = [u for u in users_db if u["id"] != user_id]

    return {"success": True}

@app.get("/api/export")
async def export_data():
    all_customers = await get_customers()
    all_orders = await get_orders()
    all_users = await get_users()

    data = {
        "customers": all_customers,
        "orders": all_orders,
        "users": all_users,
        "exportDate": datetime.now().isoformat()
    }

    return JSONResponse(
        content=data,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=nobel_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"}
    )

if __name__ == "__main__":
    print("🚀 启动 Nobel订单管理系统 V2.1 - 完整版")
    print(f"📊 使用 Supabase: {USE_SUPABASE}")
    print("🌐 访问地址: http://0.0.0.0:9002")
    print("🔐 默认账号: admin / admin123")
    uvicorn.run(app, host="0.0.0.0", port=9002)
