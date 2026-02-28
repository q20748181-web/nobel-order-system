"""
修复版订单系统HTML（包含数据迁移功能，保持链接稳定）
"""
import os

def generate_fixed_system_with_migration():
    """生成包含数据迁移功能的订单HTML代码"""
    
    html_template = '''<!DOCTYPE html>
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
        </div>
        <div class="nav">
            <button class="active" onclick="showPage('dashboard', this)">📊 仪表盘</button>
            <button onclick="showPage('customers', this)">👥 客户管理</button>
            <button onclick="showPage('orders_sample', this)">🎨 订单打样</button>
            <button onclick="showPage('orders_design', this)">💰 设计报价</button>
            <button onclick="showPage('orders_formal', this)">📝 下单管理</button>
            <button onclick="showPage('orders_aftersale', this)">🔧 售后管理</button>
        </div>
        
        <!-- 仪表盘 -->
        <div id="dashboard" class="page active">
            <div class="stats">
                <div class="stat-card" onclick="showPage('customers', document.querySelectorAll('.nav button')[1])"><h3 id="totalCustomers">0</h3><p>客户总数</p></div>
                <div class="stat-card" onclick="showPage('orders_sample', document.querySelectorAll('.nav button')[2])"><h3 id="totalSampleOrders">0</h3><p>打样订单</p></div>
                <div class="stat-card" onclick="showPage('orders_design', document.querySelectorAll('.nav button')[3])"><h3 id="totalDesignOrders">0</h3><p>设计报价</p></div>
                <div class="stat-card" onclick="showPage('orders_formal', document.querySelectorAll('.nav button')[4])"><h3 id="totalFormalOrders">0</h3><p>正式订单</p></div>
                <div class="stat-card" onclick="showPage('orders_aftersale', document.querySelectorAll('.nav button')[5])"><h3 id="totalAfterSaleOrders">0</h3><p>售后订单</p></div>
            </div>
            <h2>📈 最近订单</h2>
            <div id="recentOrders"></div>
        </div>
        
        <!-- 客户管理 -->
        <div id="customers" class="page">
            <h2>客户管理</h2>
            <button class="btn btn-primary" onclick="showAddCustomerForm()">➕ 添加客户</button>
            <div class="search-box"><input type="text" id="searchCustomer" placeholder="🔍 搜索客户代码或地区..." oninput="filterCustomers()"></div>
            <div id="customerForm" style="display: none; margin-top: 20px;">
                <h3>添加/编辑客户</h3>
                <div class="form-group"><label>客户代码 *</label><input type="text" id="customerCode" required></div>
                <div class="form-group"><label>地区 *</label><input type="text" id="customerRegion" required></div>
                <div class="form-group"><label>客户Logo</label><input type="file" id="customerLogo" accept="image/*" onchange="previewLogo(this)"></div>
                <div id="logoPreviewContainer" style="margin-bottom: 15px; display: none;"><img id="logoPreview" class="logo-preview" alt="Logo预览"></div>
                <button class="btn btn-primary" onclick="saveCustomer()">保存</button>
                <button class="btn" onclick="hideCustomerForm()">取消</button>
            </div>
            <div id="customerList" style="margin-top: 20px;"></div>
        </div>
        
        <!-- 订单打样管理 -->
        <div id="orders_sample" class="page">
            <h2>订单打样管理</h2>
            <button class="btn btn-primary" onclick="showAddOrderForm('sample')">➕ 创建打样订单</button>
            <div class="search-box"><input type="text" id="searchSample" placeholder="🔍 搜索订单..." oninput="filterOrders('sample')"></div>
            <div id="sampleOrderForm" style="display: none; margin-top: 20px;"></div>
            <div id="sampleOrderList" style="margin-top: 20px;"></div>
        </div>
        
        <!-- 订单设计报价 -->
        <div id="orders_design" class="page">
            <h2>订单设计报价</h2>
            <button class="btn btn-primary" onclick="showAddOrderForm('design')">➕ 创建设计报价</button>
            <div class="search-box"><input type="text" id="searchDesign" placeholder="🔍 搜索订单..." oninput="filterOrders('design')"></div>
            <div id="designOrderForm" style="display: none; margin-top: 20px;"></div>
            <div id="designOrderList" style="margin-top: 20px;"></div>
        </div>
        
        <!-- 下单管理 -->
        <div id="orders_formal" class="page">
            <h2>下单管理</h2>
            <button class="btn btn-primary" onclick="showAddOrderForm('formal')">➕ 创建正式订单</button>
            <div class="search-box"><input type="text" id="searchFormal" placeholder="🔍 搜索订单..." oninput="filterOrders('formal')"></div>
            <div id="formalOrderForm" style="display: none; margin-top: 20px;"></div>
            <div id="formalOrderList" style="margin-top: 20px;"></div>
        </div>
        
        <!-- 订单售后管理 -->
        <div id="orders_aftersale" class="page">
            <h2>订单售后管理</h2>
            <button class="btn btn-primary" onclick="showAddOrderForm('aftersale')">➕ 创建售后订单</button>
            <div class="search-box"><input type="text" id="searchAfterSale" placeholder="🔍 搜索订单..." oninput="filterOrders('aftersale')"></div>
            <div id="aftersaleOrderForm" style="display: none; margin-top: 20px;"></div>
            <div id="aftersaleOrderList" style="margin-top: 20px;"></div>
        </div>
    </div>
    
    <script>
        // 数据存储
        var customers = [];
        var orders = [];
        var editingCustomerId = null;
        var editingOrderId = null;
        var currentOrderType = '';
        var tempLogoUrl = '';
        var tempOrderImages = [];
        var tempSentNo = '';
        var tempEstimatedDate = '';
        var tempIsBatch = false;
        var tempBatchInfo = '';
        var tempBatchDeliveryDate = '';
        var tempExecutor = '';

        function init() {
            console.log('初始化系统...');
            loadData();
            if (customers.length === 0 && orders.length === 0) {
                console.log('加载示例数据...');
                initDemoData();
            }
            updateDashboard();
            renderCustomers();
            renderAllOrders();
            console.log('系统初始化完成');
        }

        function loadData() {
            try {
                // 先尝试加载v4数据
                customers = JSON.parse(localStorage.getItem('cabinet_customers_v4')) || [];
                orders = JSON.parse(localStorage.getItem('cabinet_orders_v4')) || [];
                
                // 如果v4没有数据，尝试从v3迁移
                if (customers.length === 0 && orders.length === 0) {
                    console.log('尝试从v3迁移数据...');
                    var v3Customers = JSON.parse(localStorage.getItem('cabinet_customers_v3')) || [];
                    var v3Orders = JSON.parse(localStorage.getItem('cabinet_orders_v3')) || [];
                    
                    if (v3Customers.length > 0 || v3Orders.length > 0) {
                        customers = v3Customers;
                        // 迁移订单，为v3订单添加executor字段（默认空字符串）
                        orders = v3Orders.map(function(o) {
                            return {
                                ...o,
                                executor: o.executor || ''
                            };
                        });
                        // 保存到v4
                        saveData();
                        console.log('已迁移', customers.length, '个客户，', orders.length, '个订单到v4');
                    }
                }
                
                console.log('已加载', customers.length, '个客户，', orders.length, '个订单');
            } catch(e) {
                console.error('加载数据失败:', e);
                customers = [];
                orders = [];
            }
        }

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

        function showPage(pageId, btnElement) {
            console.log('切换到页面:', pageId);
            document.querySelectorAll('.page').forEach(function(p) { p.classList.remove('active'); });
            document.querySelectorAll('.nav button').forEach(function(b) { b.classList.remove('active'); });
            document.getElementById(pageId).classList.add('active');
            if (btnElement) {
                btnElement.classList.add('active');
            }
            if (pageId === 'dashboard') {
                updateDashboard();
            }
        }

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

        function getStatusText(status) {
            var map = { pending: '待处理', processing: '处理中', completed: '已完成', cancelled: '已取消' };
            return map[status] || status;
        }

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
            console.log('隐藏客户表单');
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
            console.log('保存客户...');
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
                return '<div class="card" style="display: flex; align-items: center; gap: 15px;"><div>' + (c.logo ? '<img src="' + c.logo + '" class="logo-preview">' : '<div class="logo-preview" style="background: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #999;">无Logo</div>') + '</div><div style="flex: 1;"><h3>📋 ' + c.code + '</h3><p>📍 ' + c.region + '</p></div><div style="margin-top: 10px;"><button class="btn btn-primary" onclick="editCustomer(' + c.id + ')">编辑</button><button class="btn btn-danger" onclick="deleteCustomer(' + c.id + ')">删除</button></div></div>';
            }).join('');
            document.getElementById('customerList').innerHTML = html || '<p>暂无客户数据</p>';
        }

        function filterCustomers() {
            var search = document.getElementById('searchCustomer').value.toLowerCase();
            var filtered = customers.filter(function(c) { return c.code.toLowerCase().includes(search) || c.region.toLowerCase().includes(search); });
            var html = filtered.map(function(c) {
                return '<div class="card" style="display: flex; align-items: center; gap: 15px;"><div>' + (c.logo ? '<img src="' + c.logo + '" class="logo-preview">' : '<div class="logo-preview" style="background: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #999;">无Logo</div>') + '</div><div style="flex: 1;"><h3>📋 ' + c.code + '</h3><p>📍 ' + c.region + '</p></div><div style="margin-top: 10px;"><button class="btn btn-primary" onclick="editCustomer(' + c.id + ')">编辑</button><button class="btn btn-danger" onclick="deleteCustomer(' + c.id + ')">删除</button></div></div>';
            }).join('');
            document.getElementById('customerList').innerHTML = html || '<p>未找到匹配的客户</p>';
        }

        function previewOrderImages(input) {
            if (input.files) {
                tempOrderImages = [];
                for (var i = 0; i < input.files.length; i++) {
                    (function(file) {
                        var reader = new FileReader();
                        reader.onload = function(e) {
                            tempOrderImages.push(e.target.result);
                            renderOrderImagePreview();
                        }
                        reader.readAsDataURL(file);
                    })(input.files[i]);
                }
            }
        }

        function renderOrderImagePreview() {
            var container = document.getElementById('orderImagePreview');
            container.innerHTML = tempOrderImages.map(function(img) {
                return '<img src="' + img + '" class="order-image-preview">';
            }).join('');
            container.style.display = tempOrderImages.length > 0 ? 'flex' : 'none';
        }

        function showAddOrderForm(type) {
            console.log('显示添加订单表单:', type);
            currentOrderType = type;
            editingOrderId = null;
            tempOrderImages = [];
            tempSentNo = '';
            tempEstimatedDate = '';
            tempIsBatch = false;
            tempBatchInfo = '';
            tempBatchDeliveryDate = '';
            tempExecutor = '';
            
            var typeNames = { sample: '打样订单', design: '设计报价', formal: '正式订单', aftersale: '售后订单' };
            var executorLabels = { sample: '打样执行人员', design: '设计报价执行人员', formal: '下单拆单人员', aftersale: '售后订单跟进人员' };
            
            if (customers.length === 0) { alert('请先添加客户！'); return; }
            
            var html = '<h3>创建' + typeNames[type] + '</h3>';
            html += '<div class="form-group"><label>订单编码 *</label><input type="text" id="orderNo" required placeholder="请输入订单编码，例如：SAM001"></div>';
            html += '<div class="form-group"><label>选择客户 *</label><select id="orderCustomer" required>' + customers.map(function(c) { return '<option value="' + c.id + '">' + c.code + ' - ' + c.region + '</option>'; }).join('') + '</select></div>';
            html += '<div class="form-group"><label>订单内容 *</label><textarea id="orderContent" placeholder="请输入订单内容..."></textarea></div>';
            html += '<div class="form-group"><label>' + executorLabels[type] + ' *</label><input type="text" id="orderExecutor" required placeholder="请输入' + executorLabels[type] + '姓名"></div>';
            html += '<div class="form-group"><label>预计完成日期 *</label><input type="date" id="orderEstimatedDate" required></div>';
            
            if (type === 'sample') {
                html += '<div class="form-group"><label>发出单号</label><input type="text" id="orderSentNo" placeholder="请输入发出单号（选填）"></div>';
            }
            
            if (type === 'formal') {
                html += '<div class="form-group"><label>是否分批</label><select id="orderIsBatch" onchange="toggleBatchInfo()"><option value="false">否</option><option value="true">是</option></select></div>';
                html += '<div class="form-group" id="batchInfoGroup" style="display: none;"><label>分批信息</label><textarea id="orderBatchInfo" placeholder="请输入分批信息，例如：分两批，第一批80%，第二批20%"></textarea></div>';
                html += '<div class="form-group" id="batchDeliveryGroup" style="display: none;"><label>分批出货日期</label><input type="text" id="orderBatchDeliveryDate" placeholder="请输入分批出货日期，多个日期用逗号分隔，例如：2024-03-01, 2024-03-15"></textarea></div>';
            }
            
            html += '<div class="form-group"><label>上传图片</label><input type="file" id="orderImages" accept="image/*" multiple onchange="previewOrderImages(this)"></div>';
            html += '<div id="orderImagePreview" class="image-preview-container" style="display: none;"></div>';
            html += '<div class="form-group"><label>备注</label><textarea id="orderNotes" placeholder="请输入备注信息（选填）"></textarea></div>';
            html += '<button class="btn btn-primary" onclick="submitOrder()">提交订单</button><button class="btn" onclick="hideOrderForm()">取消</button>';
            
            var formId = type + 'OrderForm';
            document.getElementById(formId).innerHTML = html;
            document.getElementById(formId).style.display = 'block';
        }

        function toggleBatchInfo() {
            var isBatch = document.getElementById('orderIsBatch').value === 'true';
            document.getElementById('batchInfoGroup').style.display = isBatch ? 'block' : 'none';
            document.getElementById('batchDeliveryGroup').style.display = isBatch ? 'block' : 'none';
        }

        function showEditOrderForm(id, type) {
            console.log('显示编辑订单表单:', id, type);
            currentOrderType = type;
            editingOrderId = id;
            var order = orders.find(function(o) { return o.id === id; });
            var typeNames = { sample: '打样订单', design: '设计报价', formal: '正式订单', aftersale: '售后订单' };
            var executorLabels = { sample: '打样执行人员', design: '设计报价执行人员', formal: '下单拆单人员', aftersale: '售后订单跟进人员' };
            
            tempOrderImages = order.images || [];
            tempSentNo = order.sentNo || '';
            tempEstimatedDate = order.estimatedDate || '';
            tempIsBatch = order.isBatch || false;
            tempBatchInfo = order.batchInfo || '';
            tempBatchDeliveryDate = order.batchDeliveryDate || '';
            tempExecutor = order.executor || '';
            
            var html = '<h3>编辑' + typeNames[type] + '</h3>';
            html += '<div class="form-group"><label>订单编码 *</label><input type="text" id="orderNo" value="' + order.orderNo + '" required></div>';
            html += '<div class="form-group"><label>选择客户 *</label><select id="orderCustomer" required>' + customers.map(function(c) { return '<option value="' + c.id + '"' + (c.id === order.customerId ? ' selected' : '') + '>' + c.code + ' - ' + c.region + '</option>'; }).join('') + '</select></div>';
            html += '<div class="form-group"><label>订单内容 *</label><textarea id="orderContent" placeholder="请输入订单内容...">' + order.content + '</textarea></div>';
            html += '<div class="form-group"><label>' + executorLabels[type] + ' *</label><input type="text" id="orderExecutor" value="' + (order.executor || '') + '" required placeholder="请输入' + executorLabels[type] + '姓名"></div>';
            html += '<div class="form-group"><label>预计完成日期 *</label><input type="date" id="orderEstimatedDate" value="' + order.estimatedDate + '" required></div>';
            
            if (type === 'sample') {
                html += '<div class="form-group"><label>发出单号</label><input type="text" id="orderSentNo" value="' + (order.sentNo || '') + '" placeholder="请输入发出单号（选填）"></div>';
            }
            
            if (type === 'formal') {
                html += '<div class="form-group"><label>是否分批</label><select id="orderIsBatch" onchange="toggleBatchInfo()"><option value="false"' + (!order.isBatch ? ' selected' : '') + '>否</option><option value="true"' + (order.isBatch ? ' selected' : '') + '>是</option></select></div>';
                html += '<div class="form-group" id="batchInfoGroup" style="display: ' + (order.isBatch ? 'block' : 'none') + ';"><label>分批信息</label><textarea id="orderBatchInfo" placeholder="请输入分批信息">' + (order.batchInfo || '') + '</textarea></div>';
                html += '<div class="form-group" id="batchDeliveryGroup" style="display: ' + (order.isBatch ? 'block' : 'none') + ';"><label>分批出货日期</label><input type="text" id="orderBatchDeliveryDate" value="' + (order.batchDeliveryDate || '') + '" placeholder="请输入分批出货日期，多个日期用逗号分隔"></textarea></div>';
            }
            
            html += '<div class="form-group"><label>上传图片</label><input type="file" id="orderImages" accept="image/*" multiple onchange="previewOrderImages(this)"></div>';
            html += '<div id="orderImagePreview" class="image-preview-container"></div>';
            renderOrderImagePreview();
            
            html += '<div class="form-group"><label>状态</label><select id="orderStatus"><option value="pending"' + (order.status === 'pending' ? ' selected' : '') + '>待处理</option><option value="processing"' + (order.status === 'processing' ? ' selected' : '') + '>处理中</option><option value="completed"' + (order.status === 'completed' ? ' selected' : '') + '>已完成</option><option value="cancelled"' + (order.status === 'cancelled' ? ' selected' : '') + '>已取消</option></select></div>';
            html += '<div class="form-group"><label>备注</label><textarea id="orderNotes" placeholder="请输入备注信息（选填）">' + (order.notes || '') + '</textarea></div>';
            html += '<button class="btn btn-primary" onclick="updateOrder()">更新订单</button><button class="btn" onclick="hideOrderForm()">取消</button>';
            
            var formId = type + 'OrderForm';
            document.getElementById(formId).innerHTML = html;
            document.getElementById(formId).style.display = 'block';
        }

        function hideOrderForm() {
            var types = ['sample', 'design', 'formal', 'aftersale'];
            types.forEach(function(type) {
                document.getElementById(type + 'OrderForm').style.display = 'none';
            });
        }

        function submitOrder() {
            console.log('提交订单...');
            var orderNo = document.getElementById('orderNo').value.trim();
            var customerId = parseInt(document.getElementById('orderCustomer').value);
            var content = document.getElementById('orderContent').value.trim();
            var executor = document.getElementById('orderExecutor').value.trim();
            var estimatedDate = document.getElementById('orderEstimatedDate').value;
            var notes = document.getElementById('orderNotes').value.trim();
            
            if (!orderNo || !content || !executor || !estimatedDate) { alert('请填写所有必填项！'); return; }
            
            var sentNo = '';
            var isBatch = false;
            var batchInfo = '';
            var batchDeliveryDate = '';
            
            if (currentOrderType === 'sample') {
                sentNo = document.getElementById('orderSentNo') ? document.getElementById('orderSentNo').value.trim() : '';
            }
            
            if (currentOrderType === 'formal') {
                isBatch = document.getElementById('orderIsBatch').value === 'true';
                batchInfo = isBatch ? document.getElementById('orderBatchInfo').value.trim() : '';
                batchDeliveryDate = isBatch ? document.getElementById('orderBatchDeliveryDate').value.trim() : '';
            }
            
            orders.push({
                id: Date.now(),
                orderNo: orderNo,
                type: currentOrderType,
                customerId: customerId,
                status: 'pending',
                content: content,
                executor: executor,
                estimatedDate: estimatedDate,
                sentNo: sentNo,
                isBatch: isBatch,
                batchInfo: batchInfo,
                batchDeliveryDate: batchDeliveryDate,
                images: tempOrderImages,
                notes: notes,
                createdAt: new Date().toISOString()
            });
            
            saveData();
            renderAllOrders();
            hideOrderForm();
            alert('订单创建成功！');
        }

        function updateOrder() {
            console.log('更新订单...');
            var orderNo = document.getElementById('orderNo').value.trim();
            var customerId = parseInt(document.getElementById('orderCustomer').value);
            var content = document.getElementById('orderContent').value.trim();
            var executor = document.getElementById('orderExecutor').value.trim();
            var estimatedDate = document.getElementById('orderEstimatedDate').value;
            var status = document.getElementById('orderStatus').value;
            var notes = document.getElementById('orderNotes').value.trim();
            
            if (!orderNo || !content || !executor || !estimatedDate) { alert('请填写所有必填项！'); return; }
            
            var sentNo = '';
            var isBatch = false;
            var batchInfo = '';
            var batchDeliveryDate = '';
            
            if (currentOrderType === 'sample') {
                sentNo = document.getElementById('orderSentNo').value.trim();
            }
            
            if (currentOrderType === 'formal') {
                isBatch = document.getElementById('orderIsBatch').value === 'true';
                batchInfo = isBatch ? document.getElementById('orderBatchInfo').value.trim() : '';
                batchDeliveryDate = isBatch ? document.getElementById('orderBatchDeliveryDate').value.trim() : '';
            }
            
            var index = orders.findIndex(function(o) { return o.id === editingOrderId; });
            orders[index] = {
                ...orders[index],
                orderNo: orderNo,
                customerId: customerId,
                content: content,
                executor: executor,
                estimatedDate: estimatedDate,
                status: status,
                sentNo: sentNo,
                isBatch: isBatch,
                batchInfo: batchInfo,
                batchDeliveryDate: batchDeliveryDate,
                images: tempOrderImages,
                notes: notes
            };
            
            saveData();
            renderAllOrders();
            hideOrderForm();
            alert('订单更新成功！');
        }

        function updateOrderStatus(id, status) {
            var index = orders.findIndex(function(o) { return o.id === id; });
            orders[index].status = status;
            saveData();
            renderAllOrders();
            alert('状态更新成功！');
        }

        function deleteOrder(id) {
            if (confirm('确认删除此订单？')) {
                orders = orders.filter(function(o) { return o.id !== id; });
                saveData();
                renderAllOrders();
            }
        }

        function renderOrders(type) {
            var typeOrders = orders.filter(function(o) { return o.type === type; });
            var typeNames = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
            var executorLabels = { sample: '打样执行人', design: '设计执行人', formal: '拆单人员', aftersale: '跟进人员' };
            
            // 按状态分组
            var statusGroups = {
                pending: { label: '待处理', orders: [], color: 'pending' },
                processing: { label: '处理中', orders: [], color: 'processing' },
                completed: { label: '已完成', orders: [], color: 'completed' },
                cancelled: { label: '已取消', orders: [], color: 'cancelled' }
            };
            
            typeOrders.forEach(function(o) {
                if (statusGroups[o.status]) {
                    statusGroups[o.status].orders.push(o);
                }
            });
            
            var html = '';
            
            for (var status in statusGroups) {
                var group = statusGroups[status];
                if (group.orders.length > 0) {
                    html += '<div class="status-group">';
                    html += '<h3>' + group.label + ' <span class="status-count">' + group.orders.length + '个订单</span></h3>';
                    html += group.orders.map(function(o) {
                        var customer = customers.find(function(c) { return c.id === o.customerId; });
                        var editButton = 'onclick="showEditOrderForm(' + o.id + ', \\' + type + '\\')"';
                        
                        var executorLabel = executorLabels[type] || '执行人';
                        var executorHtml = '<div class="executor-info"><p><strong>👤 ' + executorLabel + ':</strong> ' + (o.executor || '-') + '</p></div>';
                        
                        var extraInfo = '';
                        if (o.sentNo) extraInfo += '<p>发出单号: ' + o.sentNo + '</p>';
                        if (o.isBatch) extraInfo += '<div class="batch-info"><p>📦 分批信息: ' + (o.batchInfo || '') + '</p><p>📅 分批出货日期: ' + (o.batchDeliveryDate || '') + '</p></div>';
                        
                        var imagesHtml = '';
                        if (o.images && o.images.length > 0) {
                            imagesHtml = '<div class="image-preview-container">' + o.images.slice(0, 3).map(function(img) {
                                return '<img src="' + img + '" class="order-image-preview">';
                            }).join('') + (o.images.length > 3 ? '<span style="color: #666; font-size: 14px;">等' + o.images.length + '张图片</span>' : '') + '</div>';
                        }
                        
                        return '<div class="card"><h3>📋 ' + o.orderNo + '</h3><p>客户: ' + (customer ? customer.code : '未知') + ' - ' + (customer ? customer.region : '') + '</p><p>内容: ' + o.content + '</p><p>预计完成: ' + (o.estimatedDate || '-') + '</p>' + executorHtml + extraInfo + imagesHtml + '<p>状态: <span class="status-badge status-' + o.status + '">' + getStatusText(o.status) + '</span></p><p>时间: ' + new Date(o.createdAt).toLocaleString() + '</p>' + (o.notes ? '<p>备注: ' + o.notes + '</p>' : '') + '<div style="margin-top: 10px;"><button class="btn btn-warning" ' + editButton + '>编辑</button><select onchange="updateOrderStatus(' + o.id + ', this.value); this.value=\\'\\';" style="padding: 8px; margin-left: 10px;"><option value="">更新状态...</option><option value="pending">待处理</option><option value="processing">处理中</option><option value="completed">已完成</option><option value="cancelled">已取消</option></select><button class="btn btn-danger" onclick="deleteOrder(' + o.id + ')" style="margin-left: 10px;">删除</button></div></div>';
                    }).join('');
                    html += '</div>';
                }
            }
            
            document.getElementById(type + 'OrderList').innerHTML = html || '<p>暂无订单数据</p>';
        }

        function renderAllOrders() {
            var types = ['sample', 'design', 'formal', 'aftersale'];
            types.forEach(renderOrders);
        }

        function filterOrders(type) {
            var searchId = 'search' + type.charAt(0).toUpperCase() + type.slice(1);
            var search = document.getElementById(searchId).value.toLowerCase();
            var typeOrders = orders.filter(function(o) { return o.type === type; });
            var filtered = typeOrders.filter(function(o) { 
                var customer = customers.find(function(c) { return c.id === o.customerId; });
                return o.orderNo.toLowerCase().includes(search) || o.content.toLowerCase().includes(search) || (o.executor && o.executor.toLowerCase().includes(search)) || (customer && customer.code.toLowerCase().includes(search));
            });
            
            // 按状态分组
            var statusGroups = {
                pending: { label: '待处理', orders: [], color: 'pending' },
                processing: { label: '处理中', orders: [], color: 'processing' },
                completed: { label: '已完成', orders: [], color: 'completed' },
                cancelled: { label: '已取消', orders: [], color: 'cancelled' }
            };
            
            filtered.forEach(function(o) {
                if (statusGroups[o.status]) {
                    statusGroups[o.status].orders.push(o);
                }
            });
            
            var html = '';
            var typeNames = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
            var executorLabels = { sample: '打样执行人', design: '设计执行人', formal: '拆单人员', aftersale: '跟进人员' };
            
            for (var status in statusGroups) {
                var group = statusGroups[status];
                if (group.orders.length > 0) {
                    html += '<div class="status-group">';
                    html += '<h3>' + group.label + ' <span class="status-count">' + group.orders.length + '个订单</span></h3>';
                    html += group.orders.map(function(o) {
                        var customer = customers.find(function(c) { return c.id === o.customerId; });
                        var editButton = 'onclick="showEditOrderForm(' + o.id + ', \\' + type + '\\')"';
                        
                        var executorLabel = executorLabels[type] || '执行人';
                        var executorHtml = '<div class="executor-info"><p><strong>👤 ' + executorLabel + ':</strong> ' + (o.executor || '-') + '</p></div>';
                        
                        var extraInfo = '';
                        if (o.sentNo) extraInfo += '<p>发出单号: ' + o.sentNo + '</p>';
                        if (o.isBatch) extraInfo += '<div class="batch-info"><p>📦 分批信息: ' + (o.batchInfo || '') + '</p><p>📅 分批出货日期: ' + (o.batchDeliveryDate || '') + '</p></div>';
                        
                        var imagesHtml = '';
                        if (o.images && o.images.length > 0) {
                            imagesHtml = '<div class="image-preview-container">' + o.images.slice(0, 3).map(function(img) {
                                return '<img src="' + img + '" class="order-image-preview">';
                            }).join('') + (o.images.length > 3 ? '<span style="color: #666; font-size: 14px;">等' + o.images.length + '张图片</span>' : '') + '</div>';
                        }
                        
                        return '<div class="card"><h3>📋 ' + o.orderNo + '</h3><p>客户: ' + (customer ? customer.code : '未知') + ' - ' + (customer ? customer.region : '') + '</p><p>内容: ' + o.content + '</p><p>预计完成: ' + (o.estimatedDate || '-') + '</p>' + executorHtml + extraInfo + imagesHtml + '<p>状态: <span class="status-badge status-' + o.status + '">' + getStatusText(o.status) + '</span></p><p>时间: ' + new Date(o.createdAt).toLocaleString() + '</p>' + (o.notes ? '<p>备注: ' + o.notes + '</p>' : '') + '<div style="margin-top: 10px;"><button class="btn btn-warning" ' + editButton + '>编辑</button><select onchange="updateOrderStatus(' + o.id + ', this.value); this.value=\\'\\';" style="padding: 8px; margin-left: 10px;"><option value="">更新状态...</option><option value="pending">待处理</option><option value="processing">处理中</option><option value="completed">已完成</option><option value="cancelled">已取消</option></select><button class="btn btn-danger" onclick="deleteOrder(' + o.id + ')" style="margin-left: 10px;">删除</button></div></div>';
                    }).join('');
                    html += '</div>';
                }
            }
            
            document.getElementById(type + 'OrderList').innerHTML = html || '<p>未找到匹配的订单</p>';
        }

        function saveData() {
            localStorage.setItem('cabinet_customers_v4', JSON.stringify(customers));
            localStorage.setItem('cabinet_orders_v4', JSON.stringify(orders));
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    </script>
</body>
</html>'''
    
    return html_template

if __name__ == "__main__":
    html_content = generate_fixed_system_with_migration()
    
    output_file = "/workspace/projects/assets/cabinet_system_v9_final.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ 修复版订单系统HTML文件已生成：", output_file)
    print(f"文件大小：{len(html_content)} 字符")
    print("\n✨ 新增功能：")
    print("- 数据迁移：自动从v3迁移到v4")
    print("- 保持原有数据不丢失")
