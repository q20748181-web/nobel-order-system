#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成修复版HTML - 使用事件监听器代替onclick属性，彻底解决导航按钮点击问题
"""

html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>橱柜订单管理系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        header h1 { font-size: 32px; margin-bottom: 10px; }
        header p { opacity: 0.9; }
        .nav { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
        .nav button { flex: 1; min-width: 120px; padding: 15px 10px; border: none; background: white; cursor: pointer; font-size: 15px; border-radius: 8px; transition: all 0.3s; }
        .nav button:hover { background: #e0e0e0; }
        .nav button.active { background: #667eea; color: white; }
        .page { display: none; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .page.active { display: block; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: bold; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
        .form-group textarea { height: 80px; resize: vertical; }
        .btn { padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: all 0.3s; margin-right: 10px; }
        .btn-primary { background: #667eea; color: white; }
        .btn-primary:hover { background: #5568d3; }
        .btn-danger { background: #e74c3c; color: white; }
        .btn-danger:hover { background: #c0392b; }
        .btn-success { background: #2ecc71; color: white; }
        .btn-success:hover { background: #27ae60; }
        .btn-warning { background: #f39c12; color: white; }
        .btn-warning:hover { background: #d68910; }
        .card { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #667eea; }
        .card h3 { margin-bottom: 10px; color: #333; }
        .card p { color: #666; margin-bottom: 5px; }
        .logo-preview { width: 80px; height: 80px; object-fit: cover; border-radius: 5px; border: 2px solid #ddd; }
        .order-image-preview { width: 120px; height: 120px; object-fit: cover; border-radius: 5px; border: 2px solid #ddd; margin-right: 10px; margin-bottom: 10px; }
        .image-preview-container { display: flex; flex-wrap: wrap; margin-top: 10px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; cursor: pointer; transition: all 0.3s; }
        .stat-card:hover { transform: translateY(-5px); box-shadow: 0 5px 20px rgba(0,0,0,0.15); }
        .stat-card h3 { font-size: 40px; color: #667eea; margin-bottom: 10px; }
        .stat-card p { color: #666; font-size: 16px; }
        .search-box { margin-bottom: 20px; }
        .search-box input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
        .status-badge { padding: 5px 15px; border-radius: 20px; font-size: 12px; }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-processing { background: #d1ecf1; color: #0c5460; }
        .status-completed { background: #d4edda; color: #155724; }
        .status-cancelled { background: #f8d7da; color: #721c24; }
        .status-group { margin-bottom: 30px; }
        .status-group h3 { margin-bottom: 15px; color: #333; font-size: 18px; }
        .status-count { background: #667eea; color: white; padding: 2px 10px; border-radius: 12px; font-size: 14px; margin-left: 10px; }
        .batch-info { background: #fff9e6; padding: 15px; border-radius: 5px; margin-top: 10px; border-left: 3px solid #f39c12; }
        .executor-info { background: #e8f4fd; padding: 10px; border-radius: 5px; margin-top: 10px; border-left: 3px solid #3498db; }
        .executor-info p { margin-bottom: 5px; }
        .executor-info strong { color: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏠 橱柜订单管理系统</h1>
            <p>数据保存在浏览器本地 | 客户Logo支持上传 | 执行人员管理</p>
        </header>
        <div class="nav">
            <button id="nav-dashboard" class="active" data-page="dashboard">📊 仪表盘</button>
            <button id="nav-customers" data-page="customers">👥 客户管理</button>
            <button id="nav-sample" data-page="orders_sample">🎨 订单打样</button>
            <button id="nav-design" data-page="orders_design">💰 设计报价</button>
            <button id="nav-formal" data-page="orders_formal">📝 下单管理</button>
            <button id="nav-aftersale" data-page="orders_aftersale">🔧 售后管理</button>
        </div>
        
        <!-- 仪表盘 -->
        <div id="dashboard" class="page active">
            <div class="stats">
                <div class="stat-card" data-page="customers" data-nav="nav-customers"><h3 id="totalCustomers">0</h3><p>客户总数</p></div>
                <div class="stat-card" data-page="orders_sample" data-nav="nav-sample"><h3 id="totalSampleOrders">0</h3><p>打样订单</p></div>
                <div class="stat-card" data-page="orders_design" data-nav="nav-design"><h3 id="totalDesignOrders">0</h3><p>设计报价</p></div>
                <div class="stat-card" data-page="orders_formal" data-nav="nav-formal"><h3 id="totalFormalOrders">0</h3><p>正式订单</p></div>
                <div class="stat-card" data-page="orders_aftersale" data-nav="nav-aftersale"><h3 id="totalAfterSaleOrders">0</h3><p>售后订单</p></div>
            </div>
            <h2>📈 最近订单</h2>
            <div id="recentOrders"></div>
        </div>
        
        <!-- 客户管理 -->
        <div id="customers" class="page">
            <h2>客户管理</h2>
            <button id="btnAddCustomer" class="btn btn-primary">➕ 添加客户</button>
            <div class="search-box"><input type="text" id="searchCustomer" placeholder="🔍 搜索客户代码或地区..."></div>
            <div id="customerForm" style="display: none; margin-top: 20px;">
                <h3>添加/编辑客户</h3>
                <div class="form-group"><label>客户代码 *</label><input type="text" id="customerCode" required></div>
                <div class="form-group"><label>地区 *</label><input type="text" id="customerRegion" required></div>
                <div class="form-group"><label>客户Logo</label><input type="file" id="customerLogo" accept="image/*"></div>
                <div id="logoPreviewContainer" style="margin-bottom: 15px; display: none;"><img id="logoPreview" class="logo-preview" alt="Logo预览"></div>
                <button id="btnSaveCustomer" class="btn btn-primary">保存</button>
                <button id="btnCancelCustomer" class="btn">取消</button>
            </div>
            <div id="customerList" style="margin-top: 20px;"></div>
        </div>
        
        <!-- 订单打样 -->
        <div id="orders_sample" class="page">
            <h2>订单打样管理</h2>
            <button id="btnAddSample" class="btn btn-primary">➕ 创建打样订单</button>
            <div class="search-box"><input type="text" id="searchSample" placeholder="🔍 搜索订单..."></div>
            <div id="sampleOrderForm" style="display: none; margin-top: 20px;"></div>
            <div id="sampleOrderList" style="margin-top: 20px;"></div>
        </div>
        
        <!-- 设计报价 -->
        <div id="orders_design" class="page">
            <h2>设计报价管理</h2>
            <button id="btnAddDesign" class="btn btn-primary">➕ 创建设计报价</button>
            <div class="search-box"><input type="text" id="searchDesign" placeholder="🔍 搜索订单..."></div>
            <div id="designOrderForm" style="display: none; margin-top: 20px;"></div>
            <div id="designOrderList" style="margin-top: 20px;"></div>
        </div>
        
        <!-- 下单管理 -->
        <div id="orders_formal" class="page">
            <h2>正式订单管理</h2>
            <button id="btnAddFormal" class="btn btn-primary">➕ 创建正式订单</button>
            <div class="search-box"><input type="text" id="searchFormal" placeholder="🔍 搜索订单..."></div>
            <div id="formalOrderForm" style="display: none; margin-top: 20px;"></div>
            <div id="formalOrderList" style="margin-top: 20px;"></div>
        </div>
        
        <!-- 售后管理 -->
        <div id="orders_aftersale" class="page">
            <h2>售后服务管理</h2>
            <button id="btnAddAfterSale" class="btn btn-primary">➕ 创建售后订单</button>
            <div class="search-box"><input type="text" id="searchAfterSale" placeholder="🔍 搜索订单..."></div>
            <div id="aftersaleOrderForm" style="display: none; margin-top: 20px;"></div>
            <div id="aftersaleOrderList" style="margin-top: 20px;"></div>
        </div>
    </div>

    <script>
        // 全局变量
        var customers = [];
        var orders = [];
        var editingCustomerId = null;
        var editingOrderId = null;
        var editingOrderType = null;
        var tempLogoUrl = '';
        var tempOrderImages = [];
        var tempSentNo = '';
        var tempEstimatedDate = '';
        var tempIsBatch = false;
        var tempBatchInfo = '';
        var tempBatchDeliveryDate = '';
        var tempExecutor = '';

        // 初始化数据
        function initDemoData() {
            customers = [
                { id: 1, code: "C001", region: "北京", logo: "" },
                { id: 2, code: "C002", region: "上海", logo: "" },
                { id: 3, code: "C003", region: "广州", logo: "" }
            ];
            orders = [
                { id: 1, orderNo: "SAM001", type: "sample", customerId: 1, status: "pending", content: "客厅柜子打样", executor: "张三", sentNo: "", estimatedDate: "2024-02-01", images: [], notes: "", createdAt: "2024-01-01T00:00:00.000Z" },
                { id: 2, orderNo: "DSN001", type: "design", customerId: 2, status: "processing", content: "厨房整体设计", executor: "李四", estimatedDate: "2024-02-15", images: [], notes: "设计稿已确认", createdAt: "2024-01-02T00:00:00.000Z" },
                { id: 3, orderNo: "ORD001", type: "formal", customerId: 3, status: "completed", content: "全套橱柜定制", executor: "王五", estimatedDate: "2024-03-01", isBatch: true, batchInfo: "分两批交付", batchDeliveryDate: "2024-03-01, 2024-03-15", images: [], notes: "等待确认", createdAt: "2024-01-03T00:00:00.000Z" },
                { id: 4, orderNo: "AFT001", type: "aftersale", customerId: 1, status: "processing", content: "维修服务", executor: "赵六", estimatedDate: "2024-01-20", images: [], notes: "上门维修", createdAt: "2024-01-04T00:00:00.000Z" }
            ];
            saveData();
        }

        // 切换页面
        function showPage(pageId, navButtonId) {
            console.log('切换到页面:', pageId);
            
            // 隐藏所有页面
            document.querySelectorAll('.page').forEach(function(p) { 
                p.classList.remove('active'); 
            });
            
            // 移除所有导航按钮的激活状态
            document.querySelectorAll('.nav button').forEach(function(b) { 
                b.classList.remove('active'); 
            });
            
            // 显示目标页面
            var targetPage = document.getElementById(pageId);
            if (targetPage) {
                targetPage.classList.add('active');
            }
            
            // 激活导航按钮
            var navButton = document.getElementById(navButtonId) || 
                           document.querySelector('.nav button[data-page="' + pageId + '"]');
            if (navButton) {
                navButton.classList.add('active');
            }
            
            // 如果是仪表盘，更新数据
            if (pageId === 'dashboard') {
                updateDashboard();
            }
        }

        // 更新仪表盘
        function updateDashboard() {
            document.getElementById('totalCustomers').textContent = customers.length;
            document.getElementById('totalSampleOrders').textContent = orders.filter(function(o) { return o.type === 'sample'; }).length;
            document.getElementById('totalDesignOrders').textContent = orders.filter(function(o) { return o.type === 'design'; }).length;
            document.getElementById('totalFormalOrders').textContent = orders.filter(function(o) { return o.type === 'formal'; }).length;
            document.getElementById('totalAfterSaleOrders').textContent = orders.filter(function(o) { return o.type === 'aftersale'; }).length;
            
            var recentOrders = orders.slice(-5).reverse();
            var html = recentOrders.length ? recentOrders.map(function(o) {
                var customer = customers.find(function(c) { return c.id === o.customerId; });
                var typeNames = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
                var executorLabels = { sample: '打样执行人', design: '设计执行人', formal: '拆单人员', aftersale: '跟进人员' };
                return '<div class="card"><h3>' + o.orderNo + ' - ' + (typeNames[o.type] || o.type) + '</h3><p>客户: ' + (customer ? customer.code : '未知') + '</p><p>内容: ' + o.content + '</p><p>' + (executorLabels[o.type] || '执行人') + ': ' + (o.executor || '-') + '</p><p>预计完成: ' + (o.estimatedDate || '-') + '</p><p>状态: <span class="status-badge status-' + o.status + '">' + getStatusText(o.status) + '</span></p></div>';
            }).join('') : '<p>暂无订单数据</p>';
            document.getElementById('recentOrders').innerHTML = html;
        }

        // 获取状态文本
        function getStatusText(status) {
            var map = { pending: '待处理', processing: '处理中', completed: '已完成', cancelled: '已取消' };
            return map[status] || status;
        }

        // 加载数据
        function loadData() {
            try {
                customers = JSON.parse(localStorage.getItem('cabinet_customers_v4')) || [];
                orders = JSON.parse(localStorage.getItem('cabinet_orders_v4')) || [];
                console.log('已加载', customers.length, '个客户，', orders.length, '个订单');
            } catch(e) {
                console.error('加载数据失败:', e);
                customers = [];
                orders = [];
            }
        }

        // 保存数据
        function saveData() {
            localStorage.setItem('cabinet_customers_v4', JSON.stringify(customers));
            localStorage.setItem('cabinet_orders_v4', JSON.stringify(orders));
        }

        // 客户管理相关函数
        function showAddCustomerForm() {
            console.log('显示添加客户表单');
            editingCustomerId = null;
            tempLogoUrl = '';
            document.getElementById('customerCode').value = '';
            document.getElementById('customerRegion').value = '';
            document.getElementById('customerLogo').value = '';
            document.getElementById('logoPreviewContainer').style.display = 'none';
            document.getElementById('customerForm').style.display = 'block';
        }

        function hideCustomerForm() {
            document.getElementById('customerForm').style.display = 'none';
        }

        function previewLogo(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('logoPreview').src = e.target.result;
                    document.getElementById('logoPreviewContainer').style.display = 'block';
                    tempLogoUrl = e.target.result;
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        function saveCustomer() {
            var code = document.getElementById('customerCode').value.trim();
            var region = document.getElementById('customerRegion').value.trim();
            
            if (!code || !region) { alert('请填写所有必填项！'); return; }
            
            if (editingCustomerId) {
                var index = customers.findIndex(function(c) { return c.id === editingCustomerId; });
                customers[index] = { ...customers[index], code: code, region: region, logo: tempLogoUrl || customers[index].logo };
            } else {
                customers.push({ id: Date.now(), code: code, region: region, logo: tempLogoUrl });
            }
            
            saveData();
            renderCustomers();
            hideCustomerForm();
            alert(editingCustomerId ? '客户更新成功！' : '客户添加成功！');
        }

        function editCustomer(id) {
            var customer = customers.find(function(c) { return c.id === id; });
            editingCustomerId = id;
            tempLogoUrl = customer.logo || '';
            document.getElementById('customerCode').value = customer.code;
            document.getElementById('customerRegion').value = customer.region;
            if (customer.logo) {
                document.getElementById('logoPreview').src = customer.logo;
                document.getElementById('logoPreviewContainer').style.display = 'block';
            } else {
                document.getElementById('logoPreviewContainer').style.display = 'none';
            }
            document.getElementById('customerForm').style.display = 'block';
        }

        function deleteCustomer(id) {
            if (orders.some(function(o) { return o.customerId === id; })) { alert('无法删除：该客户存在关联订单。'); return; }
            if (confirm('确认删除此客户？')) {
                customers = customers.filter(function(c) { return c.id !== id; });
                saveData();
                renderCustomers();
            }
        }

        function renderCustomers() {
            var html = customers.map(function(c) {
                return '<div class="card" style="display: flex; align-items: center; gap: 15px;"><div>' + (c.logo ? '<img src="' + c.logo + '" class="logo-preview">' : '<div class="logo-preview" style="background: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #999;">无Logo</div>') + '</div><div style="flex: 1;"><h3>📋 ' + c.code + '</h3><p>📍 ' + c.region + '</p></div><div style="margin-top: 10px;"><button class="btn btn-primary edit-customer-btn" data-id="' + c.id + '">编辑</button><button class="btn btn-danger delete-customer-btn" data-id="' + c.id + '">删除</button></div></div>';
            }).join('');
            document.getElementById('customerList').innerHTML = html || '<p>暂无客户数据</p>';
            
            // 绑定编辑和删除按钮事件
            bindCustomerButtons();
        }

        function bindCustomerButtons() {
            document.querySelectorAll('.edit-customer-btn').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    editCustomer(parseInt(this.getAttribute('data-id')));
                });
            });
            
            document.querySelectorAll('.delete-customer-btn').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    deleteCustomer(parseInt(this.getAttribute('data-id')));
                });
            });
        }

        function filterCustomers() {
            var search = document.getElementById('searchCustomer').value.toLowerCase();
            var filtered = customers.filter(function(c) { return c.code.toLowerCase().includes(search) || c.region.toLowerCase().includes(search); });
            var html = filtered.map(function(c) {
                return '<div class="card" style="display: flex; align-items: center; gap: 15px;"><div>' + (c.logo ? '<img src="' + c.logo + '" class="logo-preview">' : '<div class="logo-preview" style="background: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #999;">无Logo</div>') + '</div><div style="flex: 1;"><h3>📋 ' + c.code + '</h3><p>📍 ' + c.region + '</p></div><div style="margin-top: 10px;"><button class="btn btn-primary edit-customer-btn" data-id="' + c.id + '">编辑</button><button class="btn btn-danger delete-customer-btn" data-id="' + c.id + '">删除</button></div></div>';
            }).join('');
            document.getElementById('customerList').innerHTML = html || '<p>未找到匹配的客户</p>';
            
            bindCustomerButtons();
        }

        // 订单管理相关函数
        function showAddOrderForm(type) {
            editingOrderId = null;
            editingOrderType = type;
            tempOrderImages = [];
            tempSentNo = '';
            tempEstimatedDate = '';
            tempIsBatch = false;
            tempBatchInfo = '';
            tempBatchDeliveryDate = '';
            tempExecutor = '';
            
            var typeLabels = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
            var executorLabels = { sample: '打样执行人', design: '设计执行人', formal: '拆单人员', aftersale: '跟进人员' };
            
            var customerOptions = customers.map(function(c) {
                return '<option value="' + c.id + '">' + c.code + ' (' + c.region + ')</option>';
            }).join('');
            
            var extraFields = '';
            if (type === 'formal') {
                extraFields = `
                    <div class="form-group">
                        <label>是否拆单</label>
                        <select id="orderIsBatch" onchange="toggleBatchFields()">
                            <option value="false">否</option>
                            <option value="true">是</option>
                        </select>
                    </div>
                    <div id="batchFields" style="display: none;">
                        <div class="form-group">
                            <label>拆单说明</label>
                            <input type="text" id="orderBatchInfo" placeholder="如：分两批交付">
                        </div>
                        <div class="form-group">
                            <label>分批交付日期</label>
                            <input type="text" id="orderBatchDeliveryDate" placeholder="如：2024-03-01, 2024-03-15">
                        </div>
                    </div>
                `;
            }
            
            var formHtml = `
                <h3>创建${typeLabels[type]}订单</h3>
                <div class="form-group">
                    <label>订单号 *</label>
                    <input type="text" id="orderNo" placeholder="如：${type.toUpperCase()}001">
                </div>
                <div class="form-group">
                    <label>客户 *</label>
                    <select id="orderCustomer">
                        <option value="">请选择客户</option>
                        ${customerOptions}
                    </select>
                </div>
                <div class="form-group">
                    <label>订单内容 *</label>
                    <textarea id="orderContent" placeholder="请输入订单内容描述"></textarea>
                </div>
                <div class="form-group">
                    <label>${executorLabels[type]} *</label>
                    <input type="text" id="orderExecutor" placeholder="请输入执行人员姓名">
                </div>
                <div class="form-group">
                    <label>预计完成日期</label>
                    <input type="date" id="orderEstimatedDate">
                </div>
                <div class="form-group">
                    <label>订单图片</label>
                    <input type="file" id="orderImages" accept="image/*" multiple>
                </div>
                <div id="orderImagePreview" class="image-preview-container"></div>
                <div class="form-group">
                    <label>备注</label>
                    <textarea id="orderNotes" placeholder="订单备注信息"></textarea>
                </div>
                ${extraFields}
                <button id="btnSaveOrder" class="btn btn-primary">保存订单</button>
                <button id="btnCancelOrder" class="btn">取消</button>
            `;
            
            document.getElementById(type + 'OrderForm').innerHTML = formHtml;
            document.getElementById(type + 'OrderForm').style.display = 'block';
            
            // 绑定订单表单按钮事件
            document.getElementById('btnSaveOrder').addEventListener('click', saveOrder);
            document.getElementById('btnCancelOrder').addEventListener('click', function() {
                document.getElementById(type + 'OrderForm').style.display = 'none';
            });
            document.getElementById('orderImages').addEventListener('change', previewOrderImages);
        }

        function toggleBatchFields() {
            var isBatch = document.getElementById('orderIsBatch').value === 'true';
            document.getElementById('batchFields').style.display = isBatch ? 'block' : 'none';
        }

        function previewOrderImages(input) {
            if (input.files) {
                tempOrderImages = [];
                var previewContainer = document.getElementById('orderImagePreview');
                previewContainer.innerHTML = '';
                
                for (var i = 0; i < input.files.length; i++) {
                    (function(file) {
                        var reader = new FileReader();
                        reader.onload = function(e) {
                            var img = document.createElement('img');
                            img.src = e.target.result;
                            img.className = 'order-image-preview';
                            previewContainer.appendChild(img);
                            tempOrderImages.push(e.target.result);
                        }
                        reader.readAsDataURL(file);
                    })(input.files[i]);
                }
            }
        }

        function saveOrder() {
            var orderNo = document.getElementById('orderNo').value.trim();
            var customerId = parseInt(document.getElementById('orderCustomer').value);
            var content = document.getElementById('orderContent').value.trim();
            var executor = document.getElementById('orderExecutor').value.trim();
            
            if (!orderNo || !customerId || !content || !executor) { alert('请填写所有必填项！'); return; }
            
            var order = {
                id: editingOrderId || Date.now(),
                orderNo: orderNo,
                type: editingOrderType,
                customerId: customerId,
                content: content,
                executor: executor,
                estimatedDate: document.getElementById('orderEstimatedDate').value,
                sentNo: document.getElementById('orderSentNo') ? document.getElementById('orderSentNo').value : '',
                images: tempOrderImages,
                notes: document.getElementById('orderNotes').value,
                status: 'pending',
                createdAt: new Date().toISOString()
            };
            
            if (editingOrderType === 'formal') {
                order.isBatch = document.getElementById('orderIsBatch').value === 'true';
                if (order.isBatch) {
                    order.batchInfo = document.getElementById('orderBatchInfo').value;
                    order.batchDeliveryDate = document.getElementById('orderBatchDeliveryDate').value;
                }
            }
            
            if (editingOrderId) {
                var index = orders.findIndex(function(o) { return o.id === editingOrderId; });
                order.status = orders[index].status;
                order.createdAt = orders[index].createdAt;
                orders[index] = order;
            } else {
                orders.push(order);
            }
            
            saveData();
            renderOrders(editingOrderType);
            document.getElementById(editingOrderType + 'OrderForm').style.display = 'none';
            updateDashboard();
            alert(editingOrderId ? '订单更新成功！' : '订单创建成功！');
        }

        function editOrder(id, type) {
            var order = orders.find(function(o) { return o.id === id; });
            editingOrderId = id;
            editingOrderType = type;
            tempOrderImages = order.images || [];
            
            var typeLabels = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
            var executorLabels = { sample: '打样执行人', design: '设计执行人', formal: '拆单人员', aftersale: '跟进人员' };
            var statusOptions = ['pending', 'processing', 'completed', 'cancelled'];
            
            var customerOptions = customers.map(function(c) {
                return '<option value="' + c.id + '">' + c.code + ' (' + c.region + ')</option>';
            }).join('');
            
            var extraFields = '';
            if (type === 'formal') {
                extraFields = `
                    <div class="form-group">
                        <label>是否拆单</label>
                        <select id="orderIsBatch" onchange="toggleBatchFields()">
                            <option value="false" ${!order.isBatch ? 'selected' : ''}>否</option>
                            <option value="true" ${order.isBatch ? 'selected' : ''}>是</option>
                        </select>
                    </div>
                    <div id="batchFields" style="display: ${order.isBatch ? 'block' : 'none'};">
                        <div class="form-group">
                            <label>拆单说明</label>
                            <input type="text" id="orderBatchInfo" value="${order.batchInfo || ''}">
                        </div>
                        <div class="form-group">
                            <label>分批交付日期</label>
                            <input type="text" id="orderBatchDeliveryDate" value="${order.batchDeliveryDate || ''}">
                        </div>
                    </div>
                `;
            }
            
            var imagePreview = '';
            if (tempOrderImages.length > 0) {
                imagePreview = '<div id="orderImagePreview" class="image-preview-container">' + 
                    tempOrderImages.map(function(img) {
                        return '<img src="' + img + '" class="order-image-preview">';
                    }).join('') + 
                '</div>';
            }
            
            var formHtml = `
                <h3>编辑${typeLabels[type]}订单</h3>
                <div class="form-group">
                    <label>订单号 *</label>
                    <input type="text" id="orderNo" value="${order.orderNo}">
                </div>
                <div class="form-group">
                    <label>客户 *</label>
                    <select id="orderCustomer">
                        ${customerOptions}
                    </select>
                </div>
                <div class="form-group">
                    <label>订单内容 *</label>
                    <textarea id="orderContent">${order.content}</textarea>
                </div>
                <div class="form-group">
                    <label>${executorLabels[type]} *</label>
                    <input type="text" id="orderExecutor" value="${order.executor || ''}">
                </div>
                <div class="form-group">
                    <label>状态</label>
                    <select id="orderStatus">
                        ${statusOptions.map(function(s) {
                            return '<option value="' + s + '" ' + (order.status === s ? 'selected' : '') + '>' + getStatusText(s) + '</option>';
                        }).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label>预计完成日期</label>
                    <input type="date" id="orderEstimatedDate" value="${order.estimatedDate || ''}">
                </div>
                <div class="form-group">
                    <label>订单图片</label>
                    <input type="file" id="orderImages" accept="image/*" multiple>
                </div>
                ${imagePreview}
                <div class="form-group">
                    <label>备注</label>
                    <textarea id="orderNotes">${order.notes || ''}</textarea>
                </div>
                ${extraFields}
                <button id="btnSaveOrder" class="btn btn-primary">保存订单</button>
                <button id="btnCancelOrder" class="btn">取消</button>
            `;
            
            document.getElementById(type + 'OrderForm').innerHTML = formHtml;
            document.getElementById(type + 'OrderForm').style.display = 'block';
            
            // 设置选中的客户
            document.getElementById('orderCustomer').value = order.customerId;
            
            // 绑定订单表单按钮事件
            document.getElementById('btnSaveOrder').addEventListener('click', saveOrder);
            document.getElementById('btnCancelOrder').addEventListener('click', function() {
                document.getElementById(type + 'OrderForm').style.display = 'none';
            });
            document.getElementById('orderImages').addEventListener('change', previewOrderImages);
        }

        function deleteOrder(id, type) {
            if (confirm('确认删除此订单？')) {
                orders = orders.filter(function(o) { return o.id !== id; });
                saveData();
                renderOrders(type);
                updateDashboard();
            }
        }

        function renderOrders(type) {
            var typeLabels = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
            var executorLabels = { sample: '打样执行人', design: '设计执行人', formal: '拆单人员', aftersale: '跟进人员' };
            
            var typeOrders = orders.filter(function(o) { return o.type === type; });
            
            // 按状态分组
            var statuses = ['pending', 'processing', 'completed', 'cancelled'];
            var html = '';
            
            statuses.forEach(function(status) {
                var statusOrders = typeOrders.filter(function(o) { return o.status === status; });
                if (statusOrders.length > 0) {
                    html += '<div class="status-group"><h3>' + getStatusText(status) + ' <span class="status-count">' + statusOrders.length + '</span></h3>';
                    html += statusOrders.map(function(o) {
                        var customer = customers.find(function(c) { return c.id === o.customerId; });
                        var cardHtml = '<div class="card"><h3>' + o.orderNo + '</h3>';
                        cardHtml += '<p>客户: ' + (customer ? customer.code : '未知') + '</p>';
                        cardHtml += '<p>内容: ' + o.content + '</p>';
                        cardHtml += '<div class="executor-info"><p><strong>' + executorLabels[type] + ':</strong> ' + (o.executor || '-') + '</p></div>';
                        cardHtml += '<p>预计完成: ' + (o.estimatedDate || '-') + '</p>';
                        
                        if (type === 'formal' && o.isBatch) {
                            cardHtml += '<div class="batch-info"><p><strong>拆单信息:</strong> ' + (o.batchInfo || '-') + '</p>';
                            cardHtml += '<p><strong>交付日期:</strong> ' + (o.batchDeliveryDate || '-') + '</p></div>';
                        }
                        
                        cardHtml += '<p>状态: <span class="status-badge status-' + o.status + '">' + getStatusText(o.status) + '</span></p>';
                        
                        if (o.images && o.images.length > 0) {
                            cardHtml += '<div class="image-preview-container">' + o.images.map(function(img) {
                                return '<img src="' + img + '" class="order-image-preview">';
                            }).join('') + '</div>';
                        }
                        
                        cardHtml += '<div style="margin-top: 15px;">';
                        cardHtml += '<button class="btn btn-primary edit-order-btn" data-id="' + o.id + '" data-type="' + type + '">编辑</button>';
                        cardHtml += '<button class="btn btn-danger delete-order-btn" data-id="' + o.id + '" data-type="' + type + '">删除</button>';
                        cardHtml += '</div></div>';
                        
                        return cardHtml;
                    }).join('');
                    html += '</div>';
                }
            });
            
            document.getElementById(type + 'OrderList').innerHTML = html || '<p>暂无订单</p>';
            
            // 绑定编辑和删除按钮事件
            bindOrderButtons();
        }

        function bindOrderButtons() {
            document.querySelectorAll('.edit-order-btn').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    editOrder(parseInt(this.getAttribute('data-id')), this.getAttribute('data-type'));
                });
            });
            
            document.querySelectorAll('.delete-order-btn').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    deleteOrder(parseInt(this.getAttribute('data-id')), this.getAttribute('data-type'));
                });
            });
        }

        function filterOrders(type) {
            var search = document.getElementById('search' + type.charAt(0).toUpperCase() + type.slice(1)).value.toLowerCase();
            var typeOrders = orders.filter(function(o) { return o.type === type; });
            var filtered = typeOrders.filter(function(o) { 
                return o.orderNo.toLowerCase().includes(search) || 
                       o.content.toLowerCase().includes(search);
            });
            
            var typeLabels = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
            var executorLabels = { sample: '打样执行人', design: '设计执行人', formal: '拆单人员', aftersale: '跟进人员' };
            
            var statuses = ['pending', 'processing', 'completed', 'cancelled'];
            var html = '';
            
            statuses.forEach(function(status) {
                var statusOrders = filtered.filter(function(o) { return o.status === status; });
                if (statusOrders.length > 0) {
                    html += '<div class="status-group"><h3>' + getStatusText(status) + ' <span class="status-count">' + statusOrders.length + '</span></h3>';
                    html += statusOrders.map(function(o) {
                        var customer = customers.find(function(c) { return c.id === o.customerId; });
                        var cardHtml = '<div class="card"><h3>' + o.orderNo + '</h3>';
                        cardHtml += '<p>客户: ' + (customer ? customer.code : '未知') + '</p>';
                        cardHtml += '<p>内容: ' + o.content + '</p>';
                        cardHtml += '<div class="executor-info"><p><strong>' + executorLabels[type] + ':</strong> ' + (o.executor || '-') + '</p></div>';
                        cardHtml += '<p>预计完成: ' + (o.estimatedDate || '-') + '</p>';
                        
                        if (type === 'formal' && o.isBatch) {
                            cardHtml += '<div class="batch-info"><p><strong>拆单信息:</strong> ' + (o.batchInfo || '-') + '</p>';
                            cardHtml += '<p><strong>交付日期:</strong> ' + (o.batchDeliveryDate || '-') + '</p></div>';
                        }
                        
                        cardHtml += '<p>状态: <span class="status-badge status-' + o.status + '">' + getStatusText(o.status) + '</span></p>';
                        
                        if (o.images && o.images.length > 0) {
                            cardHtml += '<div class="image-preview-container">' + o.images.map(function(img) {
                                return '<img src="' + img + '" class="order-image-preview">';
                            }).join('') + '</div>';
                        }
                        
                        cardHtml += '<div style="margin-top: 15px;">';
                        cardHtml += '<button class="btn btn-primary edit-order-btn" data-id="' + o.id + '" data-type="' + type + '">编辑</button>';
                        cardHtml += '<button class="btn btn-danger delete-order-btn" data-id="' + o.id + '" data-type="' + type + '">删除</button>';
                        cardHtml += '</div></div>';
                        
                        return cardHtml;
                    }).join('');
                    html += '</div>';
                }
            });
            
            document.getElementById(type + 'OrderList').innerHTML = html || '<p>未找到匹配的订单</p>';
            
            bindOrderButtons();
        }

        function renderAllOrders() {
            var types = ['sample', 'design', 'formal', 'aftersale'];
            types.forEach(renderOrders);
        }

        // 绑定所有事件
        function bindEvents() {
            // 导航按钮事件
            document.querySelectorAll('.nav button').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    var pageId = this.getAttribute('data-page');
                    showPage(pageId, this.id);
                });
            });
            
            // 统计卡片点击事件
            document.querySelectorAll('.stat-card').forEach(function(card) {
                card.addEventListener('click', function() {
                    var pageId = this.getAttribute('data-page');
                    var navId = this.getAttribute('data-nav');
                    showPage(pageId, navId);
                });
            });
            
            // 客户管理按钮
            document.getElementById('btnAddCustomer').addEventListener('click', showAddCustomerForm);
            document.getElementById('btnSaveCustomer').addEventListener('click', saveCustomer);
            document.getElementById('btnCancelCustomer').addEventListener('click', hideCustomerForm);
            document.getElementById('customerLogo').addEventListener('change', function() {
                previewLogo(this);
            });
            document.getElementById('searchCustomer').addEventListener('input', filterCustomers);
            
            // 订单管理按钮
            document.getElementById('btnAddSample').addEventListener('click', function() { showAddOrderForm('sample'); });
            document.getElementById('btnAddDesign').addEventListener('click', function() { showAddOrderForm('design'); });
            document.getElementById('btnAddFormal').addEventListener('click', function() { showAddOrderForm('formal'); });
            document.getElementById('btnAddAfterSale').addEventListener('click', function() { showAddOrderForm('aftersale'); });
            
            document.getElementById('searchSample').addEventListener('input', function() { filterOrders('sample'); });
            document.getElementById('searchDesign').addEventListener('input', function() { filterOrders('design'); });
            document.getElementById('searchFormal').addEventListener('input', function() { filterOrders('formal'); });
            document.getElementById('searchAfterSale').addEventListener('input', function() { filterOrders('aftersale'); });
        }

        // 初始化系统
        function init() {
            console.log('初始化系统...');
            loadData();
            
            if (customers.length === 0 && orders.length === 0) {
                console.log('加载示例数据...');
                initDemoData();
            }
            
            // 绑定所有事件
            bindEvents();
            
            // 更新仪表盘和渲染数据
            updateDashboard();
            renderCustomers();
            renderAllOrders();
            
            console.log('系统初始化完成');
        }

        // 页面加载完成后初始化
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    </script>
</body>
</html>
"""

# 写入文件
with open('assets/cabinet_system_v11_fixed.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✅ 修复版HTML已生成: assets/cabinet_system_v11_fixed.html")
print("修复内容:")
print("- 使用 addEventListener 代替 onclick 属性")
print("- 导航按钮点击事件改为事件监听器绑定")
print("- 所有按钮都使用 data-* 属性传递参数")
print("- 统一的事件绑定机制，避免转义问题")
