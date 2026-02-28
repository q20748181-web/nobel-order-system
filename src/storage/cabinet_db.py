"""
数据库管理模块 - 橱柜订单系统
使用 SQLite 数据库存储客户、产品、订单等信息
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self, db_path: str = "assets/cabinet_orders.db"):
        """初始化数据库连接"""
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_tables()
    
    def _ensure_db_directory(self):
        """确保数据库目录存在"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 允许通过列名访问
        return conn
    
    def _init_tables(self):
        """初始化数据表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 创建客户表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    address TEXT NOT NULL,
                    email TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 创建产品表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    unit TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 创建订单表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_no TEXT UNIQUE NOT NULL,
                    customer_id INTEGER NOT NULL,
                    status TEXT DEFAULT '待处理',
                    total_amount REAL DEFAULT 0,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                )
            """)
            
            # 创建订单明细表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity REAL NOT NULL,
                    unit_price REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """)
            
            # 创建索引以提高查询性能
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_no ON orders(order_no)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_customer_id ON orders(customer_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)")
            
            conn.commit()
    
    # ==================== 客户管理 ====================
    
    def add_customer(self, name: str, phone: str, address: str, email: str = None) -> int:
        """添加客户"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (name, phone, address, email)
                VALUES (?, ?, ?, ?)
            """, (name, phone, address, email))
            conn.commit()
            return cursor.lastrowid
    
    def get_customer(self, customer_id: int) -> Optional[Dict]:
        """获取单个客户"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_customers(self) -> List[Dict]:
        """获取所有客户"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]
    
    def update_customer(self, customer_id: int, name: str, phone: str, address: str, email: str = None):
        """更新客户信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers 
                SET name = ?, phone = ?, address = ?, email = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (name, phone, address, email, customer_id))
            conn.commit()
    
    def delete_customer(self, customer_id: int) -> bool:
        """删除客户（检查是否有关联订单）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 检查是否有订单
            cursor.execute("SELECT COUNT(*) FROM orders WHERE customer_id = ?", (customer_id,))
            if cursor.fetchone()[0] > 0:
                return False
            cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            conn.commit()
            return True
    
    # ==================== 产品管理 ====================
    
    def add_product(self, name: str, category: str, price: float, unit: str, description: str = None) -> int:
        """添加产品"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (name, category, price, unit, description)
                VALUES (?, ?, ?, ?, ?)
            """, (name, category, price, unit, description))
            conn.commit()
            return cursor.lastrowid
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """获取单个产品"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_products(self) -> List[Dict]:
        """获取所有产品"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]
    
    def update_product(self, product_id: int, name: str, category: str, price: float, unit: str, description: str = None):
        """更新产品信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products 
                SET name = ?, category = ?, price = ?, unit = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (name, category, price, unit, description, product_id))
            conn.commit()
    
    def delete_product(self, product_id: int) -> bool:
        """删除产品（检查是否有关联订单）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 检查是否有订单明细
            cursor.execute("SELECT COUNT(*) FROM order_items WHERE product_id = ?", (product_id,))
            if cursor.fetchone()[0] > 0:
                return False
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return True
    
    # ==================== 订单管理 ====================
    
    def generate_order_no(self) -> str:
        """生成订单编号：ORD + 年月日 + 序号"""
        today = datetime.now().strftime("%Y%m%d")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 查询今天已有订单数
            cursor.execute("""
                SELECT COUNT(*) FROM orders 
                WHERE order_no LIKE ?
            """, (f"ORD{today}%",))
            count = cursor.fetchone()[0]
            # 生成序号（4位，前面补0）
            seq = str(count + 1).zfill(4)
            return f"ORD{today}{seq}"
    
    def create_order(self, customer_id: int, items: List[Dict], notes: str = None) -> Tuple[bool, str, Optional[int]]:
        """
        创建订单
        items: [{"product_id": 1, "quantity": 2}, ...]
        返回: (success, message, order_id)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # 计算总金额
                total_amount = 0
                order_items_data = []
                
                for item in items:
                    product = self.get_product(item['product_id'])
                    if not product:
                        return False, f"产品 ID {item['product_id']} 不存在", None
                    
                    quantity = item['quantity']
                    subtotal = product['price'] * quantity
                    total_amount += subtotal
                    
                    order_items_data.append({
                        'product_id': item['product_id'],
                        'quantity': quantity,
                        'unit_price': product['price'],
                        'subtotal': subtotal
                    })
                
                # 生成订单编号
                order_no = self.generate_order_no()
                
                # 插入订单
                cursor.execute("""
                    INSERT INTO orders (order_no, customer_id, total_amount, notes)
                    VALUES (?, ?, ?, ?)
                """, (order_no, customer_id, total_amount, notes))
                order_id = cursor.lastrowid
                
                # 插入订单明细
                for item_data in order_items_data:
                    cursor.execute("""
                        INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                        VALUES (?, ?, ?, ?, ?)
                    """, (order_id, item_data['product_id'], item_data['quantity'], 
                          item_data['unit_price'], item_data['subtotal']))
                
                conn.commit()
                return True, f"订单 {order_no} 创建成功", order_id
                
            except Exception as e:
                conn.rollback()
                return False, f"订单创建失败: {str(e)}", None
    
    def get_order(self, order_id: int) -> Optional[Dict]:
        """获取订单详情（包含客户和订单明细）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 获取订单基本信息
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            order = cursor.fetchone()
            if not order:
                return None
            
            order_dict = dict(order)
            
            # 获取客户信息
            customer = self.get_customer(order_dict['customer_id'])
            order_dict['customer'] = customer
            
            # 获取订单明细
            cursor.execute("""
                SELECT oi.*, p.name as product_name, p.category, p.unit
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = ?
            """, (order_id,))
            order_dict['items'] = [dict(row) for row in cursor.fetchall()]
            
            return order_dict
    
    def get_all_orders(self) -> List[Dict]:
        """获取所有订单"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, c.name as customer_name, c.phone as customer_phone
                FROM orders o
                JOIN customers c ON o.customer_id = c.id
                ORDER BY o.id DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """更新订单状态"""
        valid_statuses = ['待处理', '已确认', '生产中', '已完成', '已取消']
        if status not in valid_statuses:
            return False
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE orders 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, order_id))
            conn.commit()
            return True
    
    def update_order_notes(self, order_id: int, notes: str):
        """更新订单备注"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE orders 
                SET notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (notes, order_id))
            conn.commit()
    
    def delete_order(self, order_id: int):
        """删除订单（级联删除订单明细）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
            cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            conn.commit()
    
    # ==================== 统计查询 ====================
    
    def get_order_stats(self) -> Dict:
        """获取订单统计信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            stats = {}
            
            # 总订单数
            cursor.execute("SELECT COUNT(*) FROM orders")
            stats['total_orders'] = cursor.fetchone()[0]
            
            # 各状态订单数
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM orders
                GROUP BY status
            """)
            stats['by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # 总销售额
            cursor.execute("SELECT SUM(total_amount) FROM orders WHERE status != '已取消'")
            total_sales = cursor.fetchone()[0]
            stats['total_sales'] = float(total_sales) if total_sales else 0
            
            return stats


# 全局数据库实例
db = DatabaseManager()
