#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成优化后的HTML文件，修复所有UI和功能问题"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def generate_html():
    """生成完整的优化HTML文件"""
    
    # Part 1/3 - HTML头部和样式
    html_part1 = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>橱柜订单管理系统 v15</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif; 
            background: #f5f7fa; 
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        
        /* 登录页面 */
        .login-section { 
            background: white; 
            padding: 40px; 
            border-radius: 10px; 
            max-width: 420px; 
            margin: 80px auto; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }
        .login-section h2 {
            text-align: center; 
            color: #667eea; 
            margin-bottom: 30px; 
            font-size: 28px;
        }
        
        /* 表单样式 */
        .form-group { margin-bottom: 20px; }
        .form-group label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600; 
            color: #555;
            font-size: 14px;
        }
        .form-group input, 
        .form-group select, 
        .form-group textarea {
            width: 100%; 
            padding: 12px 15px; 
            border: 2px solid #e1e8ed; 
            border-radius: 8px; 
            font-size: 14px;
            transition: all 0.3s;
            background: white;
        }
        .form-group input:focus, 
        .form-group select:focus, 
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .form-group textarea { height: 100px; resize: vertical; }
        
        /* 按钮样式 */
        .btn { 
            padding: 12px 24px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 14px; 
            font-weight: 600;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn-primary { 
            background: #667eea; 
            color: white; 
        }
        .btn-primary:hover { 
            background: #5568d3; 
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .btn-danger { 
            background: #e74c3c; 
            color: white; 
        }
        .btn-danger:hover { 
            background: #c0392b; 
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
        }
        .btn-success { 
            background: #2ecc71; 
            color: white; 
        }
        .btn-success:hover { 
            background: #27ae60; 
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(46, 204, 113, 0.4);
        }
        .btn-secondary {
            background: #95a5a6;
            color: white;
        }
        .btn-secondary:hover {
            background: #7f8c8d;
        }
        
        /* 主内容区域 */
        .main-content { display: none; }
        
        /* 头部 */
        .header { 
            background: white; 
            padding: 25px 30px; 
            border-radius: 12px; 
            margin-bottom: 25px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { 
            color: #667eea; 
            margin-bottom: 5px; 
            font-size: 28px;
        }
        .header p { 
            color: #888; 
            font-size: 14px;
        }
        .header a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        .header a:hover {
            text-decoration: underline;
        }
        
        /* 仪表板 */
        .dashboard { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .dashboard-card { 
            background: white; 
            padding: 25px; 
            border-radius: 12px; 
            text-align: center; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s;
        }
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        .dashboard-card h3 { 
            font-size: 48px; 
            color: #667eea; 
            margin-bottom: 8px;
            font-weight: 700;
        }
        .dashboard-card p { 
            color: #888; 
            font-size: 14px;
            font-weight: 500;
        }
        
        /* 选项卡 */
        .tabs { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 25px; 
            flex-wrap: wrap;
            background: white;
            padding: 8px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .tab { 
            padding: 12px 20px; 
            background: transparent;
            border-radius: 8px; 
            cursor: pointer; 
            transition: all 0.3s; 
            color: #666;
            font-weight: 600;
            font-size: 14px;
            border: 2px solid transparent;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .tab:hover { 
            background: #f0f0f0; 
            color: #667eea;
        }
        .tab.active { 
            background: #667eea; 
            color: white; 
            border-color: #667eea;
        }
        .tab-content { 
            display: none; 
            animation: fadeIn 0.3s ease-in-out;
        }
        .tab-content.active { 
            display: block; 
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* 卡片样式 */
        .card { 
            background: white; 
            padding: 25px; 
            border-radius: 12px; 
            margin-bottom: 20px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s;
        }
        .card:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .card h3 { 
            color: #333; 
            margin-bottom: 15px; 
            font-size: 18px;
            font-weight: 600;
        }
        .card p { 
            color: #666; 
            margin-bottom: 8px;
            font-size: 14px;
            line-height: 1.6;
        }
        
        /* 状态标签 */
        .status-badge { 
            padding: 6px 16px; 
            border-radius: 20px; 
            font-size: 12px; 
            font-weight: 600;
            display: inline-block;
        }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-processing { background: #cce5ff; color: #004085; }
        .status-splitting { background: #d4edda; color: #155724; }
        .status-ordered { background: #d1ecf1; color: #0c5460; }
        .status-producing { background: #e2e3e5; color: #383d41; }
        .status-completed { background: #d4edda; color: #155724; }
        .status-cancelled { background: #f8d7da; color: #721c24; }
        
        /* 状态组 */
        .status-group { 
            margin-bottom: 25px;
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .status-group h3 { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px; 
            border-radius: 8px; 
            margin-bottom: 15px;
            font-size: 16px;
            font-weight: 600;
        }
        .status-count { 
            background: rgba(255,255,255,0.3);
            color: white; 
            padding: 4px 12px; 
            border-radius: 15px; 
            font-size: 12px; 
            margin-left: 10px;
            font-weight: 700;
        }
        
        /* Logo预览 */
        .logo-preview { 
            width: 70px; 
            height: 70px; 
            object-fit: cover; 
            border-radius: 8px; 
            border: 3px solid #e1e8ed; 
            background: #f8f9fa;
        }
        
        /* 文件预览 */
        .file-preview-container { 
            display: flex; 
            flex-wrap: wrap; 
            gap: 10px;
            margin-top: 10px;
        }
        .file-preview { 
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 18px; 
            background: #e8f4fd; 
            border-radius: 8px;
            color: #2980b9;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s;
        }
        .file-preview:hover {
            background: #d4e8f8;
            transform: translateY(-2px);
        }
        .file-preview a {
            color: #2980b9;
            text-decoration: none;
        }
        .file-preview a:hover {
            text-decoration: underline;
        }
        
        /* 执行人信息 */
        .executor-info { 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 8px; 
            margin-top: 15px;
            border-left: 4px solid #667eea;
        }
        
        /* 时间信息 */
        .time-info { 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 8px; 
            margin-top: 15px;
            border-left: 4px solid #2ecc71;
        }
        .time-info p { 
            color: #666; 
            font-size: 13px;
            margin-bottom: 6px;
        }
        .time-info p:last-child {
            margin-bottom: 0;
        }
        
        /* 搜索框 */
        .search-box { 
            margin-bottom: 20px;
        }
        .search-box input { 
            width: 100%; 
            padding: 15px 20px; 
            border: 2px solid #e1e8ed; 
            border-radius: 10px;
            font-size: 15px;
            transition: all 0.3s;
        }
        .search-box input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        /* 隐藏元素 */
        .hide { display: none !important; }
        
        /* 表单区域 */
        .form-container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-top: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .form-container h3 {
            color: #333;
            margin-bottom: 25px;
            font-size: 22px;
            font-weight: 600;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        /* 文件上传区域 */
        .upload-area {
            border: 2px dashed #667eea;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            background: #f8f9fa;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-area:hover {
            background: #f0f4ff;
            border-color: #5568d3;
        }
        .upload-area p {
            color: #666;
            margin-top: 10px;
            font-size: 14px;
        }
        
        /* 提示信息 */
        .hint {
            color: #888;
            font-size: 13px;
            margin-top: 8px;
            font-style: italic;
        }
        
        /* 空状态 */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }
        .empty-state img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            margin-bottom: 20px;
            opacity: 0.5;
        }
        .empty-state p {
            font-size: 16px;
            color: #888;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .tabs {
                gap: 8px;
            }
            .tab {
                padding: 10px 15px;
                font-size: 13px;
            }
            .dashboard {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <!-- 登录页面 -->
    <div class="login-section" id="loginSection">
        <h2>🏠 橱柜订单管理系统</h2>
        <div class="form-group">
            <label>用户名</label>
            <input type="text" id="username" placeholder="请输入用户名" autocomplete="username">
        </div>
        <div class="form-group">
            <label>密码</label>
            <input type="password" id="password" placeholder="请输入密码" autocomplete="current-password">
        </div>
        <button class="btn btn-primary" style="width: 100%; justify-content: center;" onclick="login()">
            <span>🔐</span> 登录
        </button>
        <p style="text-align: center; margin-top: 20px; color: #999; font-size: 13px;">
            默认账号：admin / admin
        </p>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content" id="mainContent">
        <div class="container">
            <!-- 头部 -->
            <div class="header">
                <div>
                    <h1>🏠 橱柜订单管理系统 v15</h1>
                    <p>专业的橱柜生产订单管理解决方案</p>
                </div>
                <div>
                    <span style="color: #888; font-size: 14px;">欢迎，<strong id="currentUser" style="color: #667eea;">管理员</strong>！</span>
                    <a href="#" onclick="logout()" style="margin-left: 15px;">
                        <span>🚪</span> 退出登录
                    </a>
                </div>
            </div>

            <!-- 仪表板 -->
            <div class="dashboard">
                <div class="dashboard-card">
                    <h3 id="totalCustomers">0</h3>
                    <p>👥 客户总数</p>
                </div>
                <div class="dashboard-card">
                    <h3 id="totalSampleOrders">0</h3>
                    <p>🎨 打样订单</p>
                </div>
                <div class="dashboard-card">
                    <h3 id="totalDesignOrders">0</h3>
                    <p>💡 设计报价</p>
                </div>
                <div class="dashboard-card">
                    <h3 id="totalFormalOrders">0</h3>
                    <p>📦 正式订单</p>
                </div>
                <div class="dashboard-card">
                    <h3 id="totalAfterSaleOrders">0</h3>
                    <p>🔧 售后服务</p>
                </div>
            </div>

            <!-- 选项卡导航 -->
            <div class="tabs">
                <div class="tab active" onclick="switchTab('customers')">
                    <span>👥</span> 客户管理
                </div>
                <div class="tab" onclick="switchTab('sample')">
                    <span>🎨</span> 打样订单
                </div>
                <div class="tab" onclick="switchTab('design')">
                    <span>💡</span> 设计报价
                </div>
                <div class="tab" onclick="switchTab('formal')">
                    <span>📦</span> 正式订单
                </div>
                <div class="tab" onclick="switchTab('aftersale')">
                    <span>🔧</span> 售后服务
                </div>
                <div class="tab" onclick="switchTab('users')">
                    <span>👤</span> 用户管理
                </div>
                <div class="tab" onclick="switchTab('data')">
                    <span>📊</span> 数据导出
                </div>
            </div>
'''
    
    # Part 2/3 - 功能区域
    html_part2 = '''
            <!-- 客户管理 -->
            <div class="tab-content active" id="customers">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="font-size: 24px; color: #333;">👥 客户列表</h2>
                    <button class="btn btn-primary action-add" onclick="showAddCustomerForm()">
                        <span>➕</span> 添加客户
                    </button>
                </div>
                <div class="search-box">
                    <input type="text" id="searchCustomers" placeholder="🔍 搜索客户名称或地区..." oninput="filterCustomers()">
                </div>
                <div id="customerList"></div>
                
                <!-- 客户表单 -->
                <div id="customerForm" class="form-container hide">
                    <h3 id="customerFormTitle">添加客户</h3>
                    <div class="form-group">
                        <label>客户编号 *</label>
                        <input type="text" id="customerCode" placeholder="如：C001">
                        <p class="hint">客户唯一标识，建议使用字母+数字组合</p>
                    </div>
                    <div class="form-group">
                        <label>所属地区 *</label>
                        <input type="text" id="customerRegion" placeholder="如：北京朝阳区">
                    </div>
                    <div class="form-group">
                        <label>客户Logo</label>
                        <input type="file" id="customerLogo" accept="image/*" class="action-upload" onchange="previewLogo(this)">
                        <p class="hint">支持 JPG、PNG 格式，建议尺寸 200x200px</p>
                    </div>
                    <div id="logoPreviewContainer" class="hide" style="margin-top: 15px;">
                        <img id="logoPreview" class="logo-preview" src="" alt="Logo预览">
                    </div>
                    <div style="margin-top: 25px; display: flex; gap: 10px;">
                        <button class="btn btn-primary action-edit" onclick="saveCustomer()">
                            <span>💾</span> 保存
                        </button>
                        <button class="btn btn-secondary" onclick="hideCustomerForm()">
                            <span>✕</span> 取消
                        </button>
                    </div>
                </div>
            </div>

            <!-- 打样订单 -->
            <div class="tab-content" id="sample">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="font-size: 24px; color: #333;">🎨 打样订单</h2>
                    <button class="btn btn-primary action-add" onclick="showAddOrderForm('sample')">
                        <span>➕</span> 创建订单
                    </button>
                </div>
                <div class="search-box">
                    <input type="text" id="searchSample" placeholder="🔍 搜索订单号或内容..." oninput="filterOrders('sample')">
                </div>
                <div id="sampleOrders"></div>
                <div id="sampleOrderForm"></div>
            </div>

            <!-- 设计报价 -->
            <div class="tab-content" id="design">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="font-size: 24px; color: #333;">💡 设计报价</h2>
                    <button class="btn btn-primary action-add" onclick="showAddOrderForm('design')">
                        <span>➕</span> 创建报价
                    </button>
                </div>
                <div class="search-box">
                    <input type="text" id="searchDesign" placeholder="🔍 搜索报价号或内容..." oninput="filterOrders('design')">
                </div>
                <div id="designOrders"></div>
                <div id="designOrderForm"></div>
            </div>

            <!-- 正式订单 -->
            <div class="tab-content" id="formal">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="font-size: 24px; color: #333;">📦 正式订单</h2>
                    <button class="btn btn-primary action-add" onclick="showAddOrderForm('formal')">
                        <span>➕</span> 创建订单
                    </button>
                </div>
                <div class="search-box">
                    <input type="text" id="searchFormal" placeholder="🔍 搜索订单号或内容..." oninput="filterOrders('formal')">
                </div>
                <div id="formalOrders"></div>
                <div id="formalOrderForm"></div>
            </div>

            <!-- 售后服务 -->
            <div class="tab-content" id="aftersale">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="font-size: 24px; color: #333;">🔧 售后服务</h2>
                    <button class="btn btn-primary action-add" onclick="showAddOrderForm('aftersale')">
                        <span>➕</span> 创建售后
                    </button>
                </div>
                <div class="search-box">
                    <input type="text" id="searchAftersale" placeholder="🔍 搜索售后单号或内容..." oninput="filterOrders('aftersale')">
                </div>
                <div id="aftersaleOrders"></div>
                <div id="aftersaleOrderForm"></div>
            </div>

            <!-- 用户管理 -->
            <div class="tab-content" id="users">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="font-size: 24px; color: #333;">👤 用户列表</h2>
                    <button class="btn btn-primary action-manageUsers" onclick="showAddUserForm()">
                        <span>➕</span> 添加用户
                    </button>
                </div>
                <div id="userList"></div>
                
                <!-- 用户表单 -->
                <div id="userForm" class="form-container hide">
                    <h3 id="userFormTitle">添加用户</h3>
                    <div class="form-group">
                        <label>用户名 *</label>
                        <input type="text" id="userName" placeholder="请输入用户名">
                    </div>
                    <div class="form-group">
                        <label>密码 <span id="passwordLabel">*</span></label>
                        <input type="password" id="userPassword" placeholder="请输入密码">
                        <p class="hint" id="passwordHint">新用户必须设置密码</p>
                    </div>
                    <div class="form-group">
                        <label>角色 *</label>
                        <input type="text" id="userRole" placeholder="如：设计员、生产经理">
                    </div>
                    <div class="form-group">
                        <label>权限设置</label>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 10px;">
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                                <input type="checkbox" id="permEdit" style="width: auto;"> 编辑权限
                            </label>
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                                <input type="checkbox" id="permDelete" style="width: auto;"> 删除权限
                            </label>
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                                <input type="checkbox" id="permUpload" style="width: auto;"> 上传权限
                            </label>
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                                <input type="checkbox" id="permDownload" style="width: auto;"> 下载权限
                            </label>
                        </div>
                    </div>
                    <div style="margin-top: 25px; display: flex; gap: 10px;">
                        <button class="btn btn-primary action-manageUsers" onclick="saveUser()">
                            <span>💾</span> 保存
                        </button>
                        <button class="btn btn-secondary" onclick="document.getElementById('userForm').classList.add('hide')">
                            <span>✕</span> 取消
                        </button>
                    </div>
                </div>
            </div>

            <!-- 数据导出 -->
            <div class="tab-content" id="data">
                <h2 style="font-size: 24px; color: #333; margin-bottom: 20px;">📊 数据管理</h2>
                
                <div class="card">
                    <h3 style="display: flex; align-items: center; gap: 10px;">
                        <span>📥</span> 数据导出
                    </h3>
                    <p style="color: #666; margin-bottom: 15px;">
                        将所有数据导出为JSON文件，用于备份或迁移到其他环境。
                    </p>
                    <button class="btn btn-primary" onclick="exportData()">
                        <span>📥</span> 导出数据
                    </button>
                </div>
                
                <div class="card">
                    <h3 style="display: flex; align-items: center; gap: 10px;">
                        <span>📤</span> 数据导入
                    </h3>
                    <p style="color: #666; margin-bottom: 15px;">
                        从JSON文件导入数据，<strong style="color: #e74c3c;">将会覆盖现有数据</strong>，请谨慎操作。
                    </p>
                    <div class="form-group">
                        <label>选择JSON文件</label>
                        <input type="file" id="importFile" accept=".json" class="action-upload">
                    </div>
                    <button class="btn btn-success" onclick="importData()">
                        <span>📤</span> 导入数据
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ==================== 全局变量 ====================
        var customers = [];
        var orders = [];
        var users = [];
        var currentUser = null;
        var editingCustomerId = null;
        var editingOrderId = null;
        var editingOrderType = null;
        var editingUserId = null;
        var tempLogoUrl = '';
        var tempOrderFiles = [];

        // ==================== 配置数据 ====================
        var defaultUsers = [
            {
                id: 1,
                username: 'admin',
                password: 'admin',
                role: '管理员',
                permissions: {
                    edit: true,
                    delete: true,
                    upload: true,
                    download: true,
                    manageUsers: true
                }
            }
        ];

        var orderStatusConfig = {
            sample: ['pending', 'processing', 'completed', 'cancelled'],
            design: ['pending', 'processing', 'completed', 'cancelled'],
            formal: ['pending', 'splitting', 'ordered', 'producing', 'completed', 'cancelled'],
            aftersale: ['pending', 'processing', 'completed', 'cancelled']
        };

        var statusLabels = {
            pending: '待处理',
            processing: '进行中',
            splitting: '拆单中',
            ordered: '已下单',
            producing: '生产中',
            completed: '已完成',
            cancelled: '已取消'
        };

        var executorLabels = {
            sample: '设计员',
            design: '设计师',
            formal: '生产经理',
            aftersale: '售后人员'
        };

        // ==================== 初始化 ====================
        function init() {
            console.log('系统初始化中...');
            loadData();
            renderAllOrders();
            renderCustomers();
            renderUsers();
            updateDashboard();
            console.log('系统初始化完成');
        }

        // ==================== 认证模块 ====================
        function login() {
            var username = document.getElementById('username').value.trim();
            var password = document.getElementById('password').value.trim();

            if (!username || !password) { 
                alert('❌ 请输入用户名和密码！'); 
                return; 
            }

            var user = users.find(function(u) { 
                return u.username === username && u.password === password; 
            });

            if (user) {
                currentUser = user;
                document.getElementById('loginSection').style.display = 'none';
                document.getElementById('mainContent').style.display = 'block';
                document.getElementById('currentUser').textContent = user.role;
                applyPermissions();
                saveData();
                console.log('用户登录成功：', user.username);
            } else {
                alert('❌ 用户名或密码错误！');
                console.log('登录失败');
            }
        }

        function logout() {
            currentUser = null;
            document.getElementById('mainContent').style.display = 'none';
            document.getElementById('loginSection').style.display = 'block';
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
            console.log('用户已退出');
        }

        function hasPermission(permission) {
            if (!currentUser) return false;
            if (currentUser.username === 'admin') return true;
            return currentUser.permissions[permission] === true;
        }

        function applyPermissions() {
            document.querySelectorAll('.action-add, .action-edit, .action-delete, .action-upload, .action-download, .action-manageUsers').forEach(function(el) {
                var action = el.classList.contains('action-add') ? 'edit' :
                              el.classList.contains('action-edit') ? 'edit' :
                              el.classList.contains('action-delete') ? 'delete' :
                              el.classList.contains('action-upload') ? 'upload' :
                              el.classList.contains('action-download') ? 'download' :
                              el.classList.contains('action-manageUsers') ? 'manageUsers' : null;
                if (action && !hasPermission(action)) {
                    el.style.display = 'none';
                } else {
                    el.style.display = '';
                }
            });
            console.log('权限应用完成');
        }

        // ==================== 导航模块 ====================
        function switchTab(tabId) {
            console.log('切换到标签页：', tabId);
            document.querySelectorAll('.tab').forEach(function(t) { 
                t.classList.remove('active'); 
            });
            document.querySelectorAll('.tab-content').forEach(function(c) { 
                c.classList.remove('active'); 
            });
            
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
            
            // 重新渲染数据确保最新
            if (tabId === 'customers') renderCustomers();
            if (['sample', 'design', 'formal', 'aftersale'].includes(tabId)) renderOrders(tabId);
            if (tabId === 'users') renderUsers();
        }
'''
    
    # Part 3/3 - 数据存储、业务逻辑和客户管理
    html_part3 = '''
        // ==================== 数据存储 ====================
        function saveData() {
            localStorage.setItem('cabinet_customers', JSON.stringify(customers));
            localStorage.setItem('cabinet_orders', JSON.stringify(orders));
            localStorage.setItem('cabinet_users', JSON.stringify(users));
            console.log('数据已保存');
        }

        function loadData() {
            var savedCustomers = localStorage.getItem('cabinet_customers');
            var savedOrders = localStorage.getItem('cabinet_orders');
            var savedUsers = localStorage.getItem('cabinet_users');

            if (savedCustomers) {
                customers = JSON.parse(savedCustomers);
            } else {
                // 演示数据
                customers = [
                    { id: 1, code: 'C001', region: '北京朝阳区', logo: '' },
                    { id: 2, code: 'C002', region: '上海浦东新区', logo: '' },
                    { id: 3, code: 'C003', region: '广州天河区', logo: '' }
                ];
            }

            if (savedOrders) {
                orders = JSON.parse(savedOrders);
            } else {
                // 演示数据
                orders = [
                    { id: 1, orderNo: 'SAMPLE001', type: 'sample', customerId: 1, content: '厨房橱柜打样-现代简约风格', executor: '张三', status: 'completed', files: [{name: '设计图.png', type: 'image/png', data: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='}], createdAt: '2025-01-01' },
                    { id: 2, orderNo: 'SAMPLE002', type: 'sample', customerId: 2, content: '卧室橱柜打样-北欧风格', executor: '李四', status: 'processing', files: [], createdAt: '2025-01-02' },
                    { id: 3, orderNo: 'DESIGN001', type: 'design', customerId: 1, content: '厨房设计方案-包含三维效果图', executor: '王五', status: 'pending', files: [], createdAt: '2025-01-03' }
                ];
            }

            if (savedUsers) {
                users = JSON.parse(savedUsers);
            } else {
                users = defaultUsers;
            }
            
            console.log('数据加载完成 - 客户:', customers.length, '订单:', orders.length, '用户:', users.length);
        }

        function exportData() {
            var data = {
                customers: customers,
                orders: orders,
                users: users,
                exportDate: new Date().toISOString()
            };
            var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'cabinet_system_backup_' + new Date().toISOString().slice(0,10) + '.json';
            a.click();
            URL.revokeObjectURL(url);
            alert('✅ 数据导出成功！');
        }

        function importData() {
            var fileInput = document.getElementById('importFile');
            if (!fileInput.files || !fileInput.files[0]) { 
                alert('❌ 请选择要导入的文件！'); 
                return; 
            }

            var reader = new FileReader();
            reader.onload = function(e) {
                try {
                    var data = JSON.parse(e.target.result);
                    if (data.customers) customers = data.customers;
                    if (data.orders) orders = data.orders;
                    if (data.users) users = data.users;
                    saveData();
                    renderAllOrders();
                    renderCustomers();
                    renderUsers();
                    updateDashboard();
                    alert('✅ 数据导入成功！');
                } catch (err) {
                    alert('❌ 导入失败：文件格式错误！');
                    console.error('导入错误：', err);
                }
            };
            reader.readAsText(fileInput.files[0]);
        }

        // ==================== 仪表板 ====================
        function updateDashboard() {
            document.getElementById('totalCustomers').textContent = customers.length;
            document.getElementById('totalSampleOrders').textContent = orders.filter(function(o) { return o.type === 'sample'; }).length;
            document.getElementById('totalDesignOrders').textContent = orders.filter(function(o) { return o.type === 'design'; }).length;
            document.getElementById('totalFormalOrders').textContent = orders.filter(function(o) { return o.type === 'formal'; }).length;
            document.getElementById('totalAfterSaleOrders').textContent = orders.filter(function(o) { return o.type === 'aftersale'; }).length;
        }

        // ==================== 客户管理 ====================
        function showAddCustomerForm() {
            console.log('显示添加客户表单');
            editingCustomerId = null;
            tempLogoUrl = '';
            document.getElementById('customerCode').value = '';
            document.getElementById('customerRegion').value = '';
            document.getElementById('customerLogo').value = '';
            document.getElementById('logoPreviewContainer').classList.add('hide');
            document.getElementById('customerFormTitle').textContent = '添加客户';
            document.getElementById('customerForm').classList.remove('hide');
        }

        function hideCustomerForm() {
            document.getElementById('customerForm').classList.add('hide');
        }

        function previewLogo(input) {
            if (!hasPermission('upload')) { 
                alert('❌ 没有上传权限！'); 
                return; 
            }
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('logoPreview').src = e.target.result;
                    document.getElementById('logoPreviewContainer').classList.remove('hide');
                    tempLogoUrl = e.target.result;
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        function saveCustomer() {
            if (!hasPermission('edit')) { 
                alert('❌ 没有编辑权限！'); 
                return; 
            }
            var code = document.getElementById('customerCode').value.trim();
            var region = document.getElementById('customerRegion').value.trim();

            if (!code || !region) { 
                alert('❌ 请填写所有必填项！'); 
                return; 
            }

            var customer = {
                id: editingCustomerId || Date.now(),
                code: code,
                region: region,
                logo: tempLogoUrl
            };

            if (editingCustomerId) {
                var index = customers.findIndex(function(c) { return c.id === editingCustomerId; });
                customers[index] = customer;
            } else {
                customers.push(customer);
            }

            saveData();
            renderCustomers();
            hideCustomerForm();
            alert(editingCustomerId ? '✅ 客户更新成功！' : '✅ 客户添加成功！');
        }

        function editCustomer(id) {
            if (!hasPermission('edit')) { 
                alert('❌ 没有编辑权限！'); 
                return; 
            }
            var customer = customers.find(function(c) { return c.id === id; });
            if (!customer) return;
            
            editingCustomerId = id;
            tempLogoUrl = customer.logo || '';
            document.getElementById('customerCode').value = customer.code;
            document.getElementById('customerRegion').value = customer.region;
            document.getElementById('customerFormTitle').textContent = '编辑客户';
            
            if (customer.logo) {
                document.getElementById('logoPreview').src = customer.logo;
                document.getElementById('logoPreviewContainer').classList.remove('hide');
            } else {
                document.getElementById('logoPreviewContainer').classList.add('hide');
            }
            document.getElementById('customerForm').classList.remove('hide');
        }

        function deleteCustomer(id) {
            if (!hasPermission('delete')) { 
                alert('❌ 没有删除权限！'); 
                return; 
            }
            if (orders.some(function(o) { return o.customerId === id; })) { 
                alert('❌ 无法删除：该客户存在关联订单。'); 
                return; 
            }
            if (confirm('⚠️ 确认删除此客户？此操作不可恢复！')) {
                customers = customers.filter(function(c) { return c.id !== id; });
                saveData();
                renderCustomers();
                alert('✅ 客户删除成功！');
            }
        }

        function renderCustomers() {
            if (customers.length === 0) {
                document.getElementById('customerList').innerHTML = 
                    '<div class="empty-state"><p>暂无客户数据</p></div>';
                return;
            }

            var html = customers.map(function(c) {
                var logoHtml = c.logo ? 
                    '<img src="' + c.logo + '" class="logo-preview">' : 
                    '<div class="logo-preview" style="display: flex; align-items: center; justify-content: center; color: #999; font-size: 12px;">无Logo</div>';
                
                return '<div class="card" style="display: flex; align-items: center; gap: 20px;">' +
                    '<div>' + logoHtml + '</div>' +
                    '<div style="flex: 1;">' +
                        '<h3 style="font-size: 16px; color: #333;">📋 ' + c.code + '</h3>' +
                        '<p>📍 ' + c.region + '</p>' +
                    '</div>' +
                    '<div>' +
                        '<button class="btn btn-primary action-edit" data-id="' + c.id + '">' +
                            '<span>✏️</span> 编辑' +
                        '</button> ' +
                        '<button class="btn btn-danger action-delete" data-id="' + c.id + '">' +
                            '<span>🗑️</span> 删除' +
                        '</button>' +
                    '</div>' +
                '</div>';
            }).join('');
            
            document.getElementById('customerList').innerHTML = html;
            bindCustomerButtons();
        }

        function bindCustomerButtons() {
            document.querySelectorAll('#customerList .action-edit').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    editCustomer(parseInt(this.getAttribute('data-id')));
                });
                if (!hasPermission('edit')) btn.style.display = 'none';
            });

            document.querySelectorAll('#customerList .action-delete').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    deleteCustomer(parseInt(this.getAttribute('data-id')));
                });
                if (!hasPermission('delete')) btn.style.display = 'none';
            });
        }

        function filterCustomers() {
            var search = document.getElementById('searchCustomers').value.toLowerCase();
            var filtered = customers.filter(function(c) {
                return c.code.toLowerCase().includes(search) || 
                       c.region.toLowerCase().includes(search);
            });
            
            if (filtered.length === 0) {
                document.getElementById('customerList').innerHTML = 
                    '<div class="empty-state"><p>未找到匹配的客户</p></div>';
                return;
            }

            var html = filtered.map(function(c) {
                var logoHtml = c.logo ? 
                    '<img src="' + c.logo + '" class="logo-preview">' : 
                    '<div class="logo-preview" style="display: flex; align-items: center; justify-content: center; color: #999; font-size: 12px;">无Logo</div>';
                
                return '<div class="card" style="display: flex; align-items: center; gap: 20px;">' +
                    '<div>' + logoHtml + '</div>' +
                    '<div style="flex: 1;">' +
                        '<h3 style="font-size: 16px; color: #333;">📋 ' + c.code + '</h3>' +
                        '<p>📍 ' + c.region + '</p>' +
                    '</div>' +
                    '<div>' +
                        '<button class="btn btn-primary action-edit" data-id="' + c.id + '">' +
                            '<span>✏️</span> 编辑' +
                        '</button> ' +
                        '<button class="btn btn-danger action-delete" data-id="' + c.id + '">' +
                            '<span>🗑️</span> 删除' +
                        '</button>' +
                    '</div>' +
                '</div>';
            }).join('');
            
            document.getElementById('customerList').innerHTML = html;
            bindCustomerButtons();
        }
'''
    
    # 保存到临时文件
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    
    with open(os.path.join(workspace_path, "assets", "cabinet_system_v15.html"), 'w', encoding='utf-8') as f:
        f.write(html_part1)
        f.write(html_part2)
        f.write(html_part3)
    
    print(f"✅ Part 1/3 完成 - HTML头部和样式")
    print(f"✅ Part 2/3 完成 - 功能区域")
    print(f"✅ Part 3/3 完成 - 数据存储和客户管理")
    print(f"📝 完整文件已保存到: assets/cabinet_system_v15.html")
