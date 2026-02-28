#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nobel订单管理系统 - Streamlit后端服务
支持多用户、多设备数据共享
"""

import os
import json
from datetime import datetime
from supabase import create_client

import streamlit as st
import pandas as pd

# 配置Supabase客户端
supabase = create_client(
    os.getenv("COZE_SUPABASE_URL"),
    os.getenv("COZE_SUPABASE_ANON_KEY")
)

# 页面配置
st.set_page_config(
    page_title="Nobel订单管理 API",
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
    try:
        response = supabase.table('users').select('*').eq('username', username).execute()

        if not response.data:
            return False, "用户不存在"

        user = response.data[0]
        if user['password'] != password:
            return False, "密码错误"

        st.session_state.current_user = user
        return True, "登录成功"
    except Exception as e:
        return False, f"登录失败：{str(e)}"

# 登录页面
if st.session_state.current_user is None:
    st.markdown("""
    <div style='max-width: 450px; margin: 80px auto; padding: 50px; background: white; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);'>
        <h2 style='text-align: center; color: #667eea; margin-bottom: 30px; font-size: 32px;'>🏠 Nobel订单管理</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col2:
        username = st.text_input("用户名", key="login_username")
        password = st.text_input("密码", type="password", key="login_password")

        if st.button("🔐 登录", use_container_width=True):
            success, message = login(username, password)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

        st.info("默认账号：admin / admin")
else:
    # 已登录，显示主界面
    user = st.session_state.current_user

    # 侧边栏
    with st.sidebar:
        st.markdown(f"""
        <div style='padding: 20px; background: white; border-radius: 12px; margin-bottom: 20px;'>
            <h3 style='color: #667eea;'>👤 {user['role']}</h3>
            <p style='color: #888;'>{user['username']}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 退出登录", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()

    # 主内容
    st.markdown(f"""
    <h1 style='color: #667eea;'>🏠 Nobel订单管理（网络同步版）</h1>
    <p style='color: #888;'>数据已同步到云端，所有用户实时共享</p>
    """, unsafe_allow_html=True)

    # 仪表板
    col1, col2, col3, col4, col5 = st.columns(5)

    try:
        # 统计数据
        customers_response = supabase.table('customers').select('*').execute()
        orders_response = supabase.table('orders').select('*').execute()
        users_response = supabase.table('users').select('*').execute()

        customers_data = customers_response.data
        orders_data = orders_response.data
        users_data = users_response.data

        with col1:
            st.metric("👥 客户总数", len(customers_data))

        with col2:
            sample_count = len([o for o in orders_data if o['type'] == 'sample'])
            st.metric("🎨 打样订单", sample_count)

        with col3:
            design_count = len([o for o in orders_data if o['type'] == 'design'])
            st.metric("💡 设计报价", design_count)

        with col4:
            formal_count = len([o for o in orders_data if o['type'] == 'formal'])
            st.metric("📦 正式订单", formal_count)

        with col5:
            aftersale_count = len([o for o in orders_data if o['type'] == 'aftersale'])
            st.metric("🔧 售后服务", aftersale_count)

    except Exception as e:
        st.error(f"数据加载失败：{str(e)}")

    st.markdown("---")

    # 标签页
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["👥 客户管理", "🎨 打样订单", "💡 设计报价", "📦 正式订单", "🔧 售后服务", "👤 用户管理"])

    # 客户管理
    with tab1:
        st.subheader("客户列表")

        try:
            customers_response = supabase.table('customers').select('*').execute()
            customers_data = customers_response.data

            if customers_data:
                df = pd.DataFrame(customers_data)
                df_display = df[['code', 'region']]
                df_display.columns = ['客户编号', '所属地区']
                st.dataframe(df_display, use_container_width=True)
            else:
                st.info("暂无客户数据")
        except Exception as e:
            st.error(f"加载客户数据失败：{str(e)}")

        st.markdown("---")
        st.subheader("添加客户")
        with st.form("add_customer"):
            code = st.text_input("客户编号 *")
            region = st.text_input("所属地区 *")

            if st.form_submit_button("💾 保存"):
                if code and region:
                    try:
                        supabase.table('customers').insert({
                            'code': code,
                            'region': region,
                            'logo': ''
                        }).execute()
                        st.success("客户添加成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"添加失败：{str(e)}")
                else:
                    st.warning("请填写所有必填项")

    # 打样订单
    with tab2:
        st.subheader("打样订单列表")

        try:
            orders_response = supabase.table('orders').select('*, customers(code)').eq('type', 'sample').execute()
            sample_orders = orders_response.data

            if sample_orders:
                df = pd.DataFrame(sample_orders)
                if not df.empty:
                    df_display = df[['order_no', 'content', 'executor', 'status']]
                    df_display.columns = ['订单号', '内容', '执行人', '状态']
                    st.dataframe(df_display, use_container_width=True)
            else:
                st.info("暂无打样订单")
        except Exception as e:
            st.error(f"加载订单数据失败：{str(e)}")

        st.markdown("---")
        st.subheader("创建订单")
        with st.form("add_sample_order"):
            try:
                customers_response = supabase.table('customers').select('*').execute()
                customers_data = customers_response.data
                customer_options = {c['code']: c['id'] for c in customers_data}
            except:
                customer_options = {}

            order_no = st.text_input("订单号 *")
            customer_code = st.selectbox("客户 *", list(customer_options.keys())) if customer_options else st.selectbox("客户", ["无客户数据"])
            content = st.text_area("订单内容 *")
            executor = st.text_input("执行人 *")
            status = st.selectbox("状态", ["pending", "processing", "completed", "cancelled"])

            if st.form_submit_button("💾 保存"):
                if order_no and content and executor:
                    if customer_options:
                        try:
                            supabase.table('orders').insert({
                                'order_no': order_no,
                                'type': 'sample',
                                'customer_id': customer_options[customer_code],
                                'content': content,
                                'executor': executor,
                                'status': status
                            }).execute()
                            st.success("订单创建成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"创建失败：{str(e)}")
                    else:
                        st.warning("请先添加客户数据")
                else:
                    st.warning("请填写所有必填项")

    # 其他标签页的简化实现
    with tab3:
        st.info("设计报价功能开发中...")

    with tab4:
        st.info("正式订单功能开发中...")

    with tab5:
        st.info("售后服务功能开发中...")

    # 用户管理（仅admin可见）
    if user['username'] == 'admin':
        with tab6:
            st.subheader("用户列表")

            try:
                users_response = supabase.table('users').select('*').execute()
                users_data = users_response.data

                if users_data:
                    df = pd.DataFrame(users_data)
                    df_display = df[['username', 'role', 'permissions']]
                    df_display.columns = ['用户名', '角色', '权限']
                    st.dataframe(df_display, use_container_width=True)
                else:
                    st.info("暂无用户数据")
            except Exception as e:
                st.error(f"加载用户数据失败：{str(e)}")
    else:
        # 隐藏用户管理标签页
        tab6.empty()
