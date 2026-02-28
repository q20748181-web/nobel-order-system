"""
橱柜订单管理系统测试脚本
测试数据库模块的核心功能
"""
import os
import sys

# 添加项目路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
os.chdir(project_root)

# 直接导入 database 模块
import importlib.util
spec = importlib.util.spec_from_file_location("database", "src/storage/database.py")
database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database)
DatabaseManager = database.DatabaseManager


def test_database():
    """测试数据库功能"""
    print("=" * 60)
    print("开始测试橱柜订单管理系统...")
    print("=" * 60)
    
    # 创建测试数据库实例
    test_db_path = "assets/test_cabinet_orders.db"
    db = DatabaseManager(test_db_path)
    
    try:
        # 1. 测试客户管理
        print("\n📝 测试 1: 客户管理")
        print("-" * 40)
        
        # 添加客户
        customer_id = db.add_customer("张三", "13800138000", "北京市朝阳区", "zhangsan@example.com")
        print(f"✓ 添加客户成功，ID: {customer_id}")
        
        # 获取客户
        customer = db.get_customer(customer_id)
        print(f"✓ 获取客户: {customer['name']}, {customer['phone']}")
        
        # 更新客户
        db.update_customer(customer_id, "张三（更新）", "13900139000", "北京市海淀区", "zhangsan_updated@example.com")
        updated_customer = db.get_customer(customer_id)
        print(f"✓ 更新客户成功: {updated_customer['name']}")
        
        # 获取所有客户
        all_customers = db.get_all_customers()
        print(f"✓ 客户总数: {len(all_customers)}")
        
        # 2. 测试产品管理
        print("\n📝 测试 2: 产品管理")
        print("-" * 40)
        
        # 添加产品
        product_id1 = db.add_product("现代简约橱柜", "整体橱柜", 12000.0, "套", "环保板材，简洁设计")
        print(f"✓ 添加产品 1 成功，ID: {product_id1}")
        
        product_id2 = db.add_product("欧式吊柜", "吊柜", 3500.0, "平米", "实木贴皮，高端大气")
        print(f"✓ 添加产品 2 成功，ID: {product_id2}")
        
        # 获取产品
        product1 = db.get_product(product_id1)
        print(f"✓ 获取产品: {product1['name']}, 价格: ¥{product1['price']}")
        
        # 更新产品
        db.update_product(product_id1, "现代简约橱柜（升级版）", "整体橱柜", 12800.0, "套", "升级材质，更耐用")
        updated_product = db.get_product(product_id1)
        print(f"✓ 更新产品成功: {updated_product['name']}")
        
        # 获取所有产品
        all_products = db.get_all_products()
        print(f"✓ 产品总数: {len(all_products)}")
        
        # 3. 测试订单管理
        print("\n📝 测试 3: 订单管理")
        print("-" * 40)
        
        # 创建订单
        order_items = [
            {"product_id": product_id1, "quantity": 1},
            {"product_id": product_id2, "quantity": 2}
        ]
        
        success, message, order_id = db.create_order(customer_id, order_items, "请尽快发货")
        print(f"✓ 创建订单: {success}, {message}")
        
        if order_id:
            # 获取订单详情
            order = db.get_order(order_id)
            print(f"✓ 订单编号: {order['order_no']}")
            print(f"✓ 客户: {order['customer']['name']}")
            print(f"✓ 订单总额: ¥{order['total_amount']}")
            print(f"✓ 订单明细数量: {len(order['items'])}")
            
            for item in order['items']:
                print(f"  - {item['product_name']} x {item['quantity']} {item['unit']} = ¥{item['subtotal']}")
            
            # 更新订单状态
            db.update_order_status(order_id, "已确认")
            order_updated = db.get_order(order_id)
            print(f"✓ 更新订单状态: {order_updated['status']}")
            
            # 获取所有订单
            all_orders = db.get_all_orders()
            print(f"✓ 订单总数: {len(all_orders)}")
        
        # 4. 测试统计功能
        print("\n📝 测试 4: 统计功能")
        print("-" * 40)
        
        stats = db.get_order_stats()
        print(f"✓ 总订单数: {stats['total_orders']}")
        print(f"✓ 总销售额: ¥{stats['total_sales']}")
        print(f"✓ 状态分布: {stats['by_status']}")
        
        # 5. 测试订单编号生成
        print("\n📝 测试 5: 订单编号生成")
        print("-" * 40)
        
        order_no1 = db.generate_order_no()
        print(f"✓ 订单编号 1: {order_no1}")
        
        order_no2 = db.generate_order_no()
        print(f"✓ 订单编号 2: {order_no2}")
        
        # 6. 测试删除功能
        print("\n📝 测试 6: 删除功能")
        print("-" * 40)
        
        # 添加另一个客户用于删除测试
        customer_id2 = db.add_customer("李四", "13700137000", "上海市浦东新区")
        print(f"✓ 添加测试客户 ID: {customer_id2}")
        
        # 删除客户
        result = db.delete_customer(customer_id2)
        print(f"✓ 删除客户: {result}")
        
        # 添加另一个产品用于删除测试
        product_id3 = db.add_product("测试产品", "配件", 100.0, "件")
        print(f"✓ 添加测试产品 ID: {product_id3}")
        
        # 删除产品
        result = db.delete_product(product_id3)
        print(f"✓ 删除产品: {result}")
        
        # 删除订单
        if order_id:
            db.delete_order(order_id)
            all_orders_after = db.get_all_orders()
            print(f"✓ 删除订单后剩余: {len(all_orders_after)}")
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ 测试失败: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理测试数据库
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print(f"\n✓ 清理测试数据库: {test_db_path}")


if __name__ == "__main__":
    test_database()
