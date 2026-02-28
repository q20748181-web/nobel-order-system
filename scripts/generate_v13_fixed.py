#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复订单编辑中的状态、文件显示和下载按钮问题
"""

import re

# 读取现有HTML文件
with open('assets/cabinet_system_v12_with_auth.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 修复1: 确保状态选择框始终显示，并添加样式
html_content = re.sub(
    r'<div class="form-group"><label>状态</label><select id="orderStatus">\${statusOptions}</select></div>',
    '''<div class="form-group">
                    <label>状态 *</label>
                    <select id="orderStatus" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; width: 100%; font-size: 14px;">${statusOptions}</select>
                </div>''',
    html_content
)

# 修复2: 改进文件预览显示样式，确保下载链接可见
html_content = re.sub(
    r"return '<div class=\"file-preview\"><a href=\"' \+ f\.data \+ '\" download=\"' \+ f\.name \+ '\" class=\"action-download\">📎 ' \+ f\.name \+ ' \(下载\)</a></div>';",
    "return '<div class=\"file-preview\" style=\"display: inline-block; padding: 8px 15px; background: #e8f4fd; border-radius: 5px; margin-right: 10px; margin-bottom: 10px;\"><a href=\"' + f.data + '\" download=\"' + f.name + '\" class=\"action-download\" style=\"color: #2980b9; text-decoration: none; display: flex; align-items: center; gap: 5px;\">📎 ' + f.name + ' <span style=\"font-size: 12px; color: #3498db;\">(点击下载)</span></a></div>';",
    html_content
)

# 修复3: 确保文件上传预览容器可见
html_content = re.sub(
    r'<div id="orderFilePreview" class="file-preview-container"></div>',
    '<div id="orderFilePreview" class="file-preview-container" style="display: flex; flex-wrap: wrap; margin-top: 10px; min-height: 40px; border: 2px dashed #ddd; padding: 10px; border-radius: 5px;"></div>',
    html_content
)

# 修复4: 改进文件上传预览样式
html_content = re.sub(
    r"preview\.className = 'file-preview';\s+preview\.textContent = '📎 ' \+ file\.name;",
    """preview.className = 'file-preview';
                    preview.style.cssText = 'display: inline-block; padding: 8px 15px; background: #e8f4fd; border-radius: 5px; margin-right: 10px; margin-bottom: 10px; color: #2980b9;';
                    preview.textContent = '📎 ' + file.name;""",
    html_content
)

# 修复5: 在表单中添加文件说明
html_content = re.sub(
    r'<div class="form-group"><label>上传文件</label><input type="file" id="orderFiles" multiple class="action-upload"></div>',
    '''<div class="form-group">
                    <label>上传文件</label>
                    <input type="file" id="orderFiles" multiple class="action-upload" style="padding: 8px;">
                    <small style="color: #999; display: block; margin-top: 5px;">支持上传多个文件，上传后会显示在下方</small>
                </div>''',
    html_content
)

# 修复6: 确保权限控制不误删下载链接
# 在 editOrder 函数末尾添加延迟执行权限控制，确保DOM已渲染
html_content = re.sub(
    r"document\.getElementById\('btnCancelOrder_' \+ type\)\.addEventListener\('click', function\(\) \{[\s\S]{1,100}\}\);\s+document\.getElementById\('orderFiles'\)\.addEventListener\('change', previewOrderFiles\);",
    r"""document.getElementById('btnCancelOrder_' + type).addEventListener('click', function() {
                document.getElementById(type + 'OrderForm').style.display = 'none';
            });
            document.getElementById('orderFiles').addEventListener('change', previewOrderFiles);
            
            // 延迟执行权限控制，确保DOM已完全渲染
            setTimeout(function() {
                document.querySelectorAll('.action-download').forEach(function(btn) {
                    if (!hasPermission('download')) btn.style.display = 'none';
                });
            }, 100);
            
            // 根据权限控制下载按钮显示""",
    html_content
)

# 修复7: 在订单列表中也改进文件显示样式
html_content = re.sub(
    r'cardHtml \+= o\.files\.map\(function\(f\) \{\s+return \'<div class="file-preview"><a href="\' \+ f\.data \+ \'" download="\' \+ f\.name \+ \'" class="action-download">📎 \' \+ f\.name \+ \' \(下载\)</a></div>\';\s+\}\)\.join\(\'\'\);',
    """cardHtml += o.files.map(function(f) {
                        return '<div class="file-preview" style="display: inline-block; padding: 8px 15px; background: #e8f4fd; border-radius: 5px; margin-right: 10px; margin-bottom: 10px;"><a href="' + f.data + '" download="' + f.name + '" class="action-download" style="color: #2980b9; text-decoration: none;">📎 ' + f.name + ' <span style="font-size: 12px;">(点击下载)</span></a></div>';
                    }).join('');""",
    html_content
)

# 写入修复后的文件
with open('assets/cabinet_system_v13_fixed.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ 修复版已生成: assets/cabinet_system_v13_fixed.html")
print("\n🔧 修复内容:")
print("   ✅ 改进状态选择框样式，确保可见")
print("   ✅ 改进文件预览显示样式")
print("   ✅ 添加文件上传说明")
print("   ✅ 优化下载链接样式")
print("   ✅ 修复权限控制时机问题")
print("   ✅ 在订单列表中改进文件显示")
