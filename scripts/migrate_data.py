#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nobel订单管理系统 - 数据迁移工具
将localStorage数据迁移到Supabase数据库
"""

import os
import json
from supabase import create_client

# 配置Supabase客户端
supabase = create_client(
    os.getenv("COZE_SUPABASE_URL"),
    os.getenv("COZE_SUPABASE_ANON_KEY")
)

def migrate_from_json(json_file):
    """
    从JSON文件迁移数据到Supabase数据库
    """
    print(f"📤 正在读取数据文件: {json_file}")

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 迁移客户数据
    if 'customers' in data:
        print(f"👥 开始迁移客户数据...")
        for customer in data['customers']:
            try:
                supabase.table('customers').insert({
                    'code': customer.get('code', ''),
                    'region': customer.get('region', ''),
                    'logo': customer.get('logo', '')
                }).execute()
                print(f"  ✅ 客户 {customer.get('code')} 迁移成功")
            except Exception as e:
                print(f"  ❌ 客户 {customer.get('code')} 迁移失败: {e}")

    # 迁移订单数据
    if 'orders' in data:
        print(f"📦 开始迁移订单数据...")
        for order in data['orders']:
            try:
                # 查找客户ID
                customer_code = None
                if 'customerId' in order:
                    # 通过ID查找客户
                    customers_resp = supabase.table('customers').select('*').eq('id', order['customerId']).execute()
                    if customers_resp.data:
                        customer_code = customers_resp.data[0]['code']

                supabase.table('orders').insert({
                    'order_no': order.get('orderNo', ''),
                    'type': order.get('type', ''),
                    'customer_id': order.get('customerId'),
                    'content': order.get('content', ''),
                    'executor': order.get('executor', ''),
                    'status': order.get('status', 'pending'),
                    'issue_date': order.get('issueDate'),
                    'estimated_date': order.get('estimatedDate'),
                    'completed_date': order.get('completedDate'),
                    'split_date': order.get('splitDate'),
                    'ordered_date': order.get('orderedDate'),
                    'produce_date': order.get('produceDate'),
                    'notes': order.get('notes', '')
                }).execute()
                print(f"  ✅ 订单 {order.get('orderNo')} 迁移成功")
            except Exception as e:
                print(f"  ❌ 订单 {order.get('orderNo')} 迁移失败: {e}")

    # 迁移用户数据（跳过admin，避免冲突）
    if 'users' in data:
        print(f"👤 开始迁移用户数据...")
        for user in data['users']:
            if user.get('username') == 'admin':
                print(f"  ⏭️  跳过admin用户")
                continue
            try:
                supabase.table('users').insert({
                    'username': user.get('username', ''),
                    'password': user.get('password', ''),
                    'role': user.get('role', ''),
                    'permissions': user.get('permissions', {})
                }).execute()
                print(f"  ✅ 用户 {user.get('username')} 迁移成功")
            except Exception as e:
                print(f"  ❌ 用户 {user.get('username')} 迁移失败: {e}")

    print("\n✅ 数据迁移完成！")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python scripts/migrate_data.py <json文件路径>")
        print("示例: python scripts/migrate_data.py /tmp/backup.json")
        sys.exit(1)

    json_file = sys.argv[1]
    if not os.path.exists(json_file):
        print(f"❌ 文件不存在: {json_file}")
        sys.exit(1)

    migrate_from_json(json_file)
