#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nobel订单管理系统 - Streamlit后端服务（本地版本）
使用本地文件存储，无需配置数据库
"""

import os
import json
from datetime import datetime
import streamlit as st
import pandas as pd

# 数据文件路径
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# 初始化数据文件
def init_data():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([{"id": 1, "username": "admin", "password": "admin123", "role": "管理员"}], f, ensure_ascii=False, indent=2)

    if not os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

# 读取数据
def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存数据
def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 初始化数据
init_data()

# 页面配置
st.set_page_config(
    page_title="Nobel订单管理系统",
    page_icon="🏠",
    layout="wide"
)

# 自定义CSS
st.markdown("""
<style>
    .main {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }
    .stButton>button {
        width: 100%;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# 登录函数
def login(username, password):
    users = load_data(USERS_FILE)

    for user in users:
        if user['username'] == username and user['password'] == password:
            st.session_state.current_user = user
            return True, "登录成功"

    return False, "用户名或密码错误"

# 登录页面
if st.session_state.current_user is None:
    st.markdown("""
    <div style='max-width: 450px; margin: 80px auto; padding: 50px; background: white; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);'>
        <h2 style='text-align: center; color: #667eea; margin-bottom: 30px; font-size: 32px;'>🏠 Nobel订单管理系统</h2>
        <p style='text-align: center; color: #888; margin-bottom: 20px;'>欢迎使用订单管理系统</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 用户名", key="login_username")
        password = st.text_input("🔒 密码", type="password", key="login_password")

        col_login1, col_login2, col_login3 = st.columns([1, 2, 1])
        with col_login2:
            if st.button("🔐 登录", use_container_width=True):
                success, message = login(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        st.info("📌 默认账号：admin / admin123")

else:
    # 已登录，显示主界面
    user = st.session_state.current_user

    # 侧边栏
    with st.sidebar:
        st.markdown(f"""
        <div style='padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; margin-bottom: 20px;'>
            <h3 style='color: white; margin: 0;'>👤 {user['username']}</h3>
            <p style='color: rgba(255,255,255,0.8); margin: 5px 0 0 0;'>{user['role']}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 退出登录", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()

        st.divider()

        # 页面导航
        page = st.radio("📋 功能菜单", ["📊 仪表盘", "👥 客户管理", "📦 订单管理"], label_visibility="collapsed")

    # 主内容区域
    if page == "📊 仪表盘":
        st.title("📊 仪表盘")
        st.markdown("---")

        # 统计数据
        customers = load_data(CUSTOMERS_FILE)
        orders = load_data(ORDERS_FILE)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👥 客户总数", len(customers))
        with col2:
            st.metric("📦 订单总数", len(orders))
        with col3:
            pending_orders = [o for o in orders if o.get('status') == 'pending']
            st.metric("⏳ 待处理订单", len(pending_orders))
        with col4:
            completed_orders = [o for o in orders if o.get('status') == 'completed']
            st.metric("✅ 已完成订单", len(completed_orders))

        st.markdown("---")

        # 图表
        if orders:
            orders_df = pd.DataFrame(orders)

            # 订单状态分布
            status_counts = orders_df['status'].value_counts()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 订单状态分布")
                st.bar_chart(status_counts)

            with col2:
                st.subheader("📊 最新订单")
                st.dataframe(
                    orders_df.tail(5)[['order_number', 'customer_name', 'status', 'total_amount']],
                    use_container_width=True
                )

    elif page == "👥 客户管理":
        st.title("👥 客户管理")
        st.markdown("---")

        # 添加客户
        with st.expander("➕ 添加新客户", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("客户姓名 *", key="new_customer_name")
                phone = st.text_input("联系电话", key="new_customer_phone")
            with col2:
                email = st.text_input("电子邮箱", key="new_customer_email")
                company = st.text_input("公司名称", key="new_customer_company")
            address = st.text_area("地址", key="new_customer_address")

            if st.button("💾 保存客户", use_container_width=True):
                if name:
                    customers = load_data(CUSTOMERS_FILE)
                    new_customer = {
                        "id": len(customers) + 1,
                        "name": name,
                        "phone": phone,
                        "email": email,
                        "company": company,
                        "address": address,
                        "created_at": datetime.now().isoformat()
                    }
                    customers.append(new_customer)
                    save_data(CUSTOMERS_FILE, customers)
                    st.success("✅ 客户添加成功！")
                    st.rerun()
                else:
                    st.error("❌ 请填写客户姓名")

        st.markdown("---")

        # 客户列表
        customers = load_data(CUSTOMERS_FILE)

        if customers:
            st.subheader("📋 客户列表")

            # 搜索
            search = st.text_input("🔍 搜索客户", key="search_customers")

            if search:
                customers = [c for c in customers if search.lower() in c['name'].lower()]

            customers_df = pd.DataFrame(customers)
            st.dataframe(customers_df, use_container_width=True)
        else:
            st.info("📭 暂无客户数据，请添加客户")

    elif page == "📦 订单管理":
        st.title("📦 订单管理")
        st.markdown("---")

        # 添加订单
        with st.expander("➕ 创建新订单", expanded=True):
            customers = load_data(CUSTOMERS_FILE)

            col1, col2 = st.columns(2)
            with col1:
                order_number = st.text_input("订单号 *", key="new_order_number", value=f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}")
                if customers:
                    customer_names = [c['name'] for c in customers]
                    customer_name = st.selectbox("选择客户 *", customer_names, key="new_order_customer")
                else:
                    st.warning("⚠️ 请先添加客户")
                    customer_name = None
            with col2:
                order_type = st.selectbox("订单类型", ["打样", "正式订单"], key="new_order_type")
                order_status = st.selectbox("订单状态", ["待处理", "进行中", "已完成", "已取消"], key="new_order_status")
                total_amount = st.number_input("订单金额（元）", min_value=0.0, step=100.0, key="new_order_amount")

            notes = st.text_area("备注说明", key="new_order_notes")

            if st.button("💾 创建订单", use_container_width=True):
                if order_number and customer_name:
                    orders = load_data(ORDERS_FILE)

                    # 查找客户ID
                    customer_id = None
                    for c in customers:
                        if c['name'] == customer_name:
                            customer_id = c['id']
                            break

                    new_order = {
                        "id": len(orders) + 1,
                        "order_number": order_number,
                        "customer_id": customer_id,
                        "customer_name": customer_name,
                        "type": order_type,
                        "status": order_status,
                        "total_amount": total_amount,
                        "notes": notes,
                        "created_at": datetime.now().isoformat()
                    }
                    orders.append(new_order)
                    save_data(ORDERS_FILE, orders)
                    st.success("✅ 订单创建成功！")
                    st.rerun()
                else:
                    st.error("❌ 请填写订单号和选择客户")

        st.markdown("---")

        # 订单列表
        orders = load_data(ORDERS_FILE)

        if orders:
            st.subheader("📋 订单列表")

            # 搜索和筛选
            col1, col2 = st.columns(2)
            with col1:
                search = st.text_input("🔍 搜索订单", key="search_orders")
            with col2:
                status_filter = st.selectbox("📊 状态筛选", ["全部", "待处理", "进行中", "已完成", "已取消"], key="filter_status")

            filtered_orders = orders

            if search:
                filtered_orders = [o for o in filtered_orders if search.lower() in o.get('order_number', '').lower()]

            if status_filter != "全部":
                status_map = {
                    "待处理": "pending",
                    "进行中": "in_progress",
                    "已完成": "completed",
                    "已取消": "cancelled"
                }
                filtered_orders = [o for o in filtered_orders if o.get('status') == status_map[status_filter]]

            orders_df = pd.DataFrame(filtered_orders)
            st.dataframe(orders_df, use_container_width=True)

            # 导出数据
            if filtered_orders:
                if st.button("📥 导出订单数据", use_container_width=True):
                    csv = orders_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="⬇️ 下载 CSV 文件",
                        data=csv,
                        file_name=f"orders_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
        else:
            st.info("📭 暂无订单数据，请创建订单")
