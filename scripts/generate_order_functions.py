#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成完整的v15版本HTML文件 - 第二部分"""

import os

def generate_order_functions():
    """生成订单管理相关函数"""
    return '''
        // ==================== 订单管理 ====================
        function showAddOrderForm(type) {
            console.log('显示创建订单表单：', type);
            if (!hasPermission('edit')) { 
                alert('❌ 没有编辑权限！'); 
                return; 
            }
            
            editingOrderId = null;
            editingOrderType = type;
            tempOrderFiles = [];

            var typeLabels = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
            var statuses = orderStatusConfig[type];

            // 生成客户选项
            var customerOptions = '<option value="">请选择客户</option>';
            if (customers && customers.length > 0) {
                customerOptions += customers.map(function(c) {
                    return '<option value="' + c.id + '">' + c.code + ' (' + (c.region || '') + ')</option>';
                }).join('');
            } else {
                customerOptions += '<option value="" disabled>暂无客户数据</option>';
            }

            // 生成状态选项
            var statusOptions = statuses.map(function(s) {
                return '<option value="' + s + '">' + statusLabels[s] + '</option>';
            }).join('');

            // 生成时间字段
            var timeFields = '';
            if (type === 'sample' || type === 'design') {
                timeFields = `
                    <div class="form-group">
                        <label>订单下发时间</label>
                        <input type="date" id="orderIssueDate">
                    </div>
                    <div class="form-group">
                        <label>预计完成时间</label>
                        <input type="date" id="orderEstimatedDate">
                    </div>
                    <div class="form-group">
                        <label>完成时间</label>
                        <input type="date" id="orderCompletedDate">
                    </div>
                `;
            } else if (type === 'formal') {
                timeFields = `
                    <div class="form-group">
                        <label>订单下发时间</label>
                        <input type="date" id="orderIssueDate">
                    </div>
                    <div class="form-group">
                        <label>拆单时间</label>
                        <input type="date" id="orderSplitDate">
                    </div>
                    <div class="form-group">
                        <label>下单时间</label>
                        <input type="date" id="orderOrderedDate">
                    </div>
                    <div class="form-group">
                        <label>生产时间</label>
                        <input type="date" id="orderProduceDate">
                    </div>
                    <div class="form-group">
                        <label>预计完成时间</label>
                        <input type="date" id="orderEstimatedDate">
                    </div>
                    <div class="form-group">
                        <label>完成时间</label>
                        <input type="date" id="orderCompletedDate">
                    </div>
                `;
            } else if (type === 'aftersale') {
                timeFields = `
                    <div class="form-group">
                        <label>订单下发时间</label>
                        <input type="date" id="orderIssueDate">
                    </div>
                    <div class="form-group">
                        <label>预计完成时间</label>
                        <input type="date" id="orderEstimatedDate">
                    </div>
                    <div class="form-group">
                        <label>完成时间</label>
                        <input type="date" id="orderCompletedDate">
                    </div>
                `;
            }

            var formHtml = `
                <div class="form-container">
                    <h3>创建${typeLabels[type]}</h3>
                    <div class="form-group">
                        <label>订单号 *</label>
                        <input type="text" id="orderNo" placeholder="如：${type.toUpperCase()}001">
                        <p class="hint">建议使用大写字母+数字，如：FORMAL001</p>
                    </div>
                    <div class="form-group">
                        <label>客户 *</label>
                        <select id="orderCustomer">${customerOptions}</select>
                        <p class="hint">请先在客户管理中添加客户</p>
                    </div>
                    <div class="form-group">
                        <label>订单内容 *</label>
                        <textarea id="orderContent" placeholder="请详细描述订单内容、规格要求等"></textarea>
                    </div>
                    <div class="form-group">
                        <label>${executorLabels[type]} *</label>
                        <input type="text" id="orderExecutor" placeholder="请输入执行人员姓名">
                    </div>
                    <div class="form-group">
                        <label>状态 *</label>
                        <select id="orderStatus">${statusOptions}</select>
                    </div>
                    ${timeFields}
                    <div class="form-group">
                        <label>上传文件</label>
                        <div class="upload-area" onclick="document.getElementById('orderFiles').click()">
                            <div style="font-size: 32px; color: #667eea;">📎</div>
                            <p>点击或拖拽文件到此处上传</p>
                            <p style="font-size: 12px; color: #999;">支持多个文件，上传后会显示在下方</p>
                        </div>
                        <input type="file" id="orderFiles" multiple class="action-upload hide" onchange="previewOrderFiles(this)">
                    </div>
                    <div id="orderFilePreview" class="file-preview-container"></div>
                    <div class="form-group">
                        <label>备注</label>
                        <textarea id="orderNotes" placeholder="订单备注信息、特殊要求等"></textarea>
                    </div>
                    <div style="margin-top: 25px; display: flex; gap: 10px;">
                        <button id="btnSaveOrder_${type}" class="btn btn-primary action-edit">
                            <span>💾</span> 保存订单
                        </button>
                        <button id="btnCancelOrder_${type}" class="btn btn-secondary">
                            <span>✕</span> 取消
                        </button>
                    </div>
                </div>
            `;

            document.getElementById(type + 'OrderForm').innerHTML = formHtml;
            document.getElementById(type + 'OrderForm').scrollIntoView({ behavior: 'smooth' });

            // 绑定事件
            document.getElementById('btnSaveOrder_' + type).addEventListener('click', saveOrder);
            document.getElementById('btnCancelOrder_' + type).addEventListener('click', function() {
                document.getElementById(type + 'OrderForm').innerHTML = '';
            });
        }

        function previewOrderFiles(input) {
            if (!hasPermission('upload')) { 
                alert('❌ 没有上传权限！'); 
                return; 
            }
            
            if (!input.files || input.files.length === 0) return;

            var previewContainer = document.getElementById('orderFilePreview');
            if (!previewContainer) return;

            for (var i = 0; i < input.files.length; i++) {
                (function(file) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        var fileData = {
                            name: file.name,
                            type: file.type,
                            data: e.target.result
                        };
                        tempOrderFiles.push(fileData);

                        var preview = document.createElement('div');
                        preview.className = 'file-preview';
                        preview.innerHTML = 
                            '<span>📎</span> ' + 
                            '<span>' + file.name + '</span>' +
                            '<span style="cursor: pointer; color: #e74c3c; margin-left: 8px;" onclick="removeFile(' + (tempOrderFiles.length - 1) + ')">✕</span>';
                        previewContainer.appendChild(preview);
                    };
                    reader.readAsDataURL(file);
                })(input.files[i]);
            }
        }

        function removeFile(index) {
            if (!hasPermission('edit')) { 
                alert('❌ 没有编辑权限！'); 
                return; 
            }
            tempOrderFiles.splice(index, 1);
            
            var previewContainer = document.getElementById('orderFilePreview');
            if (previewContainer) {
                previewContainer.innerHTML = tempOrderFiles.map(function(f, idx) {
                    return '<div class="file-preview">' +
                        '<span>📎</span> ' +
                        '<span>' + f.name + '</span>' +
                        '<span style="cursor: pointer; color: #e74c3c; margin-left: 8px;" onclick="removeFile(' + idx + ')">✕</span>' +
                    '</div>';
                }).join('');
            }
        }

        function saveOrder() {
            if (!hasPermission('edit')) { 
                alert('❌ 没有编辑权限！'); 
                return; 
            }
            
            var orderNo = document.getElementById('orderNo').value.trim();
            var customerId = parseInt(document.getElementById('orderCustomer').value);
            var content = document.getElementById('orderContent').value.trim();
            var executor = document.getElementById('orderExecutor').value.trim();

            if (!orderNo) { alert('❌ 请填写订单号！'); return; }
            if (!customerId) { alert('❌ 请选择客户！'); return; }
            if (!content) { alert('❌ 请填写订单内容！'); return; }
            if (!executor) { alert('❌ 请填写执行人员！'); return; }

            var order = {
                id: editingOrderId || Date.now(),
                orderNo: orderNo,
                type: editingOrderType,
                customerId: customerId,
                content: content,
                executor: executor,
                status: document.getElementById('orderStatus').value,
                issueDate: document.getElementById('orderIssueDate') ? document.getElementById('orderIssueDate').value : '',
                estimatedDate: document.getElementById('orderEstimatedDate') ? document.getElementById('orderEstimatedDate').value : '',
                completedDate: document.getElementById('orderCompletedDate') ? document.getElementById('orderCompletedDate').value : '',
                files: tempOrderFiles || [],
                notes: document.getElementById('orderNotes').value || '',
                createdAt: editingOrderId ? orders.find(function(o) { return o.id === editingOrderId; }).createdAt : new Date().toISOString()
            };

            if (editingOrderType === 'formal') {
                order.splitDate = document.getElementById('orderSplitDate') ? document.getElementById('orderSplitDate').value : '';
                order.orderedDate = document.getElementById('orderOrderedDate') ? document.getElementById('orderOrderedDate').value : '';
                order.produceDate = document.getElementById('orderProduceDate') ? document.getElementById('orderProduceDate').value : '';
            }

            if (editingOrderId) {
                var index = orders.findIndex(function(o) { return o.id === editingOrderId; });
                if (index > -1) {
                    orders[index] = order;
                }
            } else {
                orders.push(order);
            }

            saveData();
            renderOrders(editingOrderType);
            document.getElementById(editingOrderType + 'OrderForm').innerHTML = '';
            updateDashboard();
            alert(editingOrderId ? '✅ 订单更新成功！' : '✅ 订单创建成功！');
        }

        function editOrder(id, type) {
            console.log('编辑订单：', id, type);
            if (!hasPermission('edit')) { 
                alert('❌ 没有编辑权限！'); 
                return; 
            }
            
            var order = orders.find(function(o) { return o.id === id; });
            if (!order) return;

            editingOrderId = id;
            editingOrderType = type;
            tempOrderFiles = order.files || [];

            var typeLabels = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
            var statuses = orderStatusConfig[type];

            // 生成客户选项
            var customerOptions = customers.map(function(c) {
                return '<option value="' + c.id + '" ' + (order.customerId === c.id ? 'selected' : '') + '>' + c.code + ' (' + (c.region || '') + ')</option>';
            }).join('');

            // 生成状态选项
            var statusOptions = statuses.map(function(s) {
                return '<option value="' + s + '" ' + (order.status === s ? 'selected' : '') + '>' + statusLabels[s] + '</option>';
            }).join('');

            // 生成时间字段
            var timeFields = '';
            if (type === 'sample' || type === 'design') {
                timeFields = `
                    <div class="form-group">
                        <label>订单下发时间</label>
                        <input type="date" id="orderIssueDate" value="${order.issueDate || ''}">
                    </div>
                    <div class="form-group">
                        <label>预计完成时间</label>
                        <input type="date" id="orderEstimatedDate" value="${order.estimatedDate || ''}">
                    </div>
                    <div class="form-group">
                        <label>完成时间</label>
                        <input type="date" id="orderCompletedDate" value="${order.completedDate || ''}">
                    </div>
                `;
            } else if (type === 'formal') {
                timeFields = `
                    <div class="form-group">
                        <label>订单下发时间</label>
                        <input type="date" id="orderIssueDate" value="${order.issueDate || ''}">
                    </div>
                    <div class="form-group">
                        <label>拆单时间</label>
                        <input type="date" id="orderSplitDate" value="${order.splitDate || ''}">
                    </div>
                    <div class="form-group">
                        <label>下单时间</label>
                        <input type="date" id="orderOrderedDate" value="${order.orderedDate || ''}">
                    </div>
                    <div class="form-group">
                        <label>生产时间</label>
                        <input type="date" id="orderProduceDate" value="${order.produceDate || ''}">
                    </div>
                    <div class="form-group">
                        <label>预计完成时间</label>
                        <input type="date" id="orderEstimatedDate" value="${order.estimatedDate || ''}">
                    </div>
                    <div class="form-group">
                        <label>完成时间</label>
                        <input type="date" id="orderCompletedDate" value="${order.completedDate || ''}">
                    </div>
                `;
            } else if (type === 'aftersale') {
                timeFields = `
                    <div class="form-group">
                        <label>订单下发时间</label>
                        <input type="date" id="orderIssueDate" value="${order.issueDate || ''}">
                    </div>
                    <div class="form-group">
                        <label>预计完成时间</label>
                        <input type="date" id="orderEstimatedDate" value="${order.estimatedDate || ''}">
                    </div>
                    <div class="form-group">
                        <label>完成时间</label>
                        <input type="date" id="orderCompletedDate" value="${order.completedDate || ''}">
                    </div>
                `;
            }

            // 生成文件预览
            var filePreviewHtml = '';
            if (tempOrderFiles.length > 0) {
                filePreviewHtml = tempOrderFiles.map(function(f, index) {
                    return '<div class="file-preview">' +
                        '<a href="' + f.data + '" download="' + f.name + '" class="action-download">' +
                            '<span>📎</span> <span>' + f.name + '</span>' +
                        '</a>' +
                        '<span style="cursor: pointer; color: #e74c3c; margin-left: 8px;" onclick="removeFile(' + index + ')">✕</span>' +
                    '</div>';
                }).join('');
            }

            var formHtml = `
                <div class="form-container">
                    <h3>编辑${typeLabels[type]}</h3>
                    <div class="form-group">
                        <label>订单号 *</label>
                        <input type="text" id="orderNo" value="${order.orderNo}">
                    </div>
                    <div class="form-group">
                        <label>客户 *</label>
                        <select id="orderCustomer">${customerOptions}</select>
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
                        <label>状态 *</label>
                        <select id="orderStatus">${statusOptions}</select>
                    </div>
                    ${timeFields}
                    <div class="form-group">
                        <label>上传文件</label>
                        <div class="upload-area" onclick="document.getElementById('orderFiles').click()">
                            <div style="font-size: 32px; color: #667eea;">📎</div>
                            <p>点击上传新文件（追加到现有文件）</p>
                        </div>
                        <input type="file" id="orderFiles" multiple class="action-upload hide" onchange="previewOrderFiles(this)">
                    </div>
                    <div id="orderFilePreview" class="file-preview-container">${filePreviewHtml}</div>
                    <div class="form-group">
                        <label>备注</label>
                        <textarea id="orderNotes">${order.notes || ''}</textarea>
                    </div>
                    <div style="margin-top: 25px; display: flex; gap: 10px;">
                        <button id="btnSaveOrder_${type}" class="btn btn-primary action-edit">
                            <span>💾</span> 保存修改
                        </button>
                        <button id="btnCancelOrder_${type}" class="btn btn-secondary">
                            <span>✕</span> 取消
                        </button>
                    </div>
                </div>
            `;

            document.getElementById(type + 'OrderForm').innerHTML = formHtml;
            document.getElementById(type + 'OrderForm').scrollIntoView({ behavior: 'smooth' });

            document.getElementById('btnSaveOrder_' + type).addEventListener('click', saveOrder);
            document.getElementById('btnCancelOrder_' + type).addEventListener('click', function() {
                document.getElementById(type + 'OrderForm').innerHTML = '';
            });
        }

        function deleteOrder(id, type) {
            if (!hasPermission('delete')) { 
                alert('❌ 没有删除权限！'); 
                return; 
            }
            if (confirm('⚠️ 确认删除此订单？此操作不可恢复！')) {
                orders = orders.filter(function(o) { return o.id !== id; });
                saveData();
                renderOrders(type);
                updateDashboard();
                alert('✅ 订单删除成功！');
            }
        }

        function renderOrders(type) {
            console.log('渲染订单列表：', type);
            var typeLabels = { sample: '打样', design: '设计报价', formal: '正式订单', aftersale: '售后服务' };
            var typeOrders = orders.filter(function(o) { return o.type === type; });

            if (typeOrders.length === 0) {
                document.getElementById(type + 'Orders').innerHTML = 
                    '<div class="empty-state"><p>暂无订单数据</p></div>';
                return;
            }

            var statuses = orderStatusConfig[type];
            var html = '';

            statuses.forEach(function(status) {
                var statusOrders = typeOrders.filter(function(o) { return o.status === status; });
                if (statusOrders.length > 0) {
                    html += '<div class="status-group">' +
                        '<h3>' + statusLabels[status] + ' <span class="status-count">' + statusOrders.length + '</span></h3>';
                    
                    html += statusOrders.map(function(o) {
                        var customer = customers.find(function(c) { return c.id === o.customerId; });
                        
                        var cardHtml = '<div class="card">' +
                            '<h3 style="font-size: 18px;">📋 ' + o.orderNo + '</h3>' +
                            '<p><strong>客户：</strong>' + (customer ? customer.code : '未知') + '</p>' +
                            '<p><strong>内容：</strong>' + o.content + '</p>' +
                            '<div class="executor-info">' +
                                '<p><strong>' + executorLabels[type] + '：</strong>' + (o.executor || '-') + '</p>' +
                            '</div>';

                        // 时间信息
                        var timeHtml = '<div class="time-info">';
                        if (o.issueDate) timeHtml += '<p>📅 下发时间：' + o.issueDate + '</p>';
                        if (type === 'formal') {
                            if (o.splitDate) timeHtml += '<p>📅 拆单时间：' + o.splitDate + '</p>';
                            if (o.orderedDate) timeHtml += '<p>📅 下单时间：' + o.orderedDate + '</p>';
                            if (o.produceDate) timeHtml += '<p>📅 生产时间：' + o.produceDate + '</p>';
                        }
                        if (o.estimatedDate) timeHtml += '<p>📅 预计完成：' + o.estimatedDate + '</p>';
                        if (o.completedDate) timeHtml += '<p>📅 完成时间：' + o.completedDate + '</p>';
                        timeHtml += '</div>';
                        cardHtml += timeHtml;

                        cardHtml += '<p><strong>状态：</strong><span class="status-badge status-' + o.status + '">' + statusLabels[o.status] + '</span></p>';

                        // 文件列表
                        if (o.files && o.files.length > 0) {
                            cardHtml += '<div style="margin-top: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea;">' +
                                '<p style="margin-bottom: 10px; font-weight: 600; color: #666;">📎 附件文件：</p>';
                            cardHtml += o.files.map(function(f) {
                                return '<div class="file-preview">' +
                                    '<a href="' + f.data + '" download="' + f.name + '" class="action-download">' +
                                        '<span>📎</span> <span>' + f.name + '</span>' +
                                    '</a>' +
                                '</div>';
                            }).join('');
                            cardHtml += '</div>';
                        }

                        if (o.notes) {
                            cardHtml += '<p style="margin-top: 15px; padding: 10px; background: #fff3cd; border-radius: 8px; color: #856404;">📝 ' + o.notes + '</p>';
                        }

                        // 操作按钮
                        var statusOptions = orderStatusConfig[type].map(function(s) {
                            return '<option value="' + s + '" ' + (o.status === s ? 'selected' : '') + '>' + statusLabels[s] + '</option>';
                        }).join('');

                        cardHtml += '<div style="margin-top: 20px; display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">' +
                            '<button class="btn btn-primary action-edit" data-id="' + o.id + '" data-type="' + type + '">' +
                                '<span>✏️</span> 编辑' +
                            '</button>' +
                            '<button class="btn btn-danger action-delete" data-id="' + o.id + '" data-type="' + type + '">' +
                                '<span>🗑️</span> 删除' +
                            '</button>' +
                            '<select class="status-select action-edit" data-order-id="' + o.id + '" data-order-type="' + type + '" style="padding: 10px; border: 2px solid #e1e8ed; border-radius: 8px; font-size: 14px;">' +
                                statusOptions +
                            '</select>' +
                        '</div>';

                        cardHtml += '</div>';
                        return cardHtml;
                    }).join('');
                    
                    html += '</div>';
                }
            });

            document.getElementById(type + 'Orders').innerHTML = html;
            bindOrderButtons(type);
        }

        function bindOrderButtons(type) {
            // 编辑按钮
            document.querySelectorAll('#' + type + 'Orders .action-edit').forEach(function(btn) {
                if (btn.classList.contains('status-select')) {
                    // 状态下拉框
                    var orderId = parseInt(btn.getAttribute('data-order-id'));
                    var orderType = btn.getAttribute('data-order-type');
                    
                    btn.addEventListener('change', function() {
                        if (!hasPermission('edit')) {
                            alert('❌ 没有编辑权限！');
                            this.value = orders.find(function(o) { return o.id === orderId && o.type === orderType; }).status;
                            return;
                        }
                        
                        var newStatus = this.value;
                        var orderIndex = orders.findIndex(function(o) { return o.id === orderId && o.type === orderType; });
                        
                        if (orderIndex > -1) {
                            orders[orderIndex].status = newStatus;
                            saveData();
                            renderOrders(orderType);
                            updateDashboard();
                            alert('✅ 状态已更新为：' + statusLabels[newStatus]);
                        }
                    });
                    
                    if (!hasPermission('edit')) btn.style.display = 'none';
                } else {
                    // 编辑按钮
                    btn.addEventListener('click', function() {
                        editOrder(parseInt(this.getAttribute('data-id')), this.getAttribute('data-type'));
                    });
                    
                    if (!hasPermission('edit')) btn.style.display = 'none';
                }
            });

            // 删除按钮
            document.querySelectorAll('#' + type + 'Orders .action-delete').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    deleteOrder(parseInt(this.getAttribute('data-id')), this.getAttribute('data-type'));
                });
                
                if (!hasPermission('delete')) btn.style.display = 'none';
            });

            // 下载按钮
            setTimeout(function() {
                document.querySelectorAll('#' + type + 'Orders .action-download').forEach(function(btn) {
                    if (!hasPermission('download')) btn.style.display = 'none';
                });
            }, 100);
        }

        function filterOrders(type) {
            var searchInput = document.getElementById('search' + type.charAt(0).toUpperCase() + type.slice(1));
            if (!searchInput) return;

            var search = searchInput.value.toLowerCase().trim();
            if (!search) {
                renderOrders(type);
                return;
            }

            var typeOrders = orders.filter(function(o) { return o.type === type; });
            var filtered = typeOrders.filter(function(o) {
                return o.orderNo.toLowerCase().includes(search) ||
                       o.content.toLowerCase().includes(search);
            });

            // 临时替换数据渲染
            var originalOrders = orders;
            orders = filtered;
            renderOrders(type);
            orders = originalOrders;
        }

        function renderAllOrders() {
            var types = ['sample', 'design', 'formal', 'aftersale'];
            types.forEach(renderOrders);
        }
    '''

if __name__ == "__main__":
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    output_file = os.path.join(workspace_path, "tmp", "order_functions.js")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(generate_order_functions())
    
    print(f"✅ 订单管理函数已生成: {output_file}")
