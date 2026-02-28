"""
橱柜订单管理系统 - Streamlit 主应用
"""
import streamlit as st
import pandas as pd
from io import BytesIO
from storage.database import db


# ==================== 页面配置 ====================
st.set_page_config(
    page_title="橱柜订单管理系统",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== 通用函数 ====================

def format_price(price):
    """格式化价格显示"""
    return f"¥{price:,.2f}"


def display_success(message):
    """显示成功消息"""
    st.success(message)


def display_error(message):
    """显示错误消息"""
    st.error(message)


def display_warning(message):
    """显示警告消息"""
    st.warning(message)


# ==================== 仪表盘页面 ====================

def show_dashboard():
    """显示仪表盘"""
    st.title("📊 仪表盘")
    
    stats = db.get_order_stats()
    
    # 统计卡片
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总订单数", stats['total_orders'])
    with col2:
        st.metric("总销售额", format_price(stats['total_sales']))
    with col3:
        pending_orders = stats['by_status'].get('待处理', 0)
        st.metric("待处理订单", pending_orders)
    
    st.markdown("---")
    
    # 订单状态分布
    st.subheader("📈 订单状态分布")
    if stats['by_status']:
        status_df = pd.DataFrame(list(stats['by_status'].items()), columns=['状态', '数量'])
        st.bar_chart(status_df.set_index('状态'))
    else:
        st.info("暂无订单数据")


# ==================== 客户管理页面 ====================

def show_customer_management():
    """显示客户管理页面"""
    st.title("👥 客户管理")
    
    # 添加客户表单
    with st.expander("➕ 添加新客户", expanded=False):
        with st.form("add_customer_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("客户姓名 *", placeholder="请输入客户姓名")
                phone = st.text_input("联系电话 *", placeholder="请输入联系电话")
            with col2:
                email = st.text_input("邮箱", placeholder="选填")
                address = st.text_input("地址 *", placeholder="请输入详细地址")
            
            if st.form_submit_button("添加客户", type="primary"):
                if name and phone and address:
                    customer_id = db.add_customer(name, phone, address, email)
                    if customer_id:
                        display_success("客户添加成功！")
                        st.rerun()
                    else:
                        display_error("添加失败，请重试。")
                else:
                    display_error("请填写所有必填项！")
    
    st.markdown("---")
    
    # 客户列表
    st.subheader("客户列表")
    customers = db.get_all_customers()
    
    if customers:
        # 添加搜索和筛选
        search = st.text_input("🔍 搜索客户", placeholder="输入姓名或电话号码搜索")
        if search:
            customers = [c for c in customers if search.lower() in c['name'].lower() or search in c['phone']]
        
        # 显示客户卡片
        for i in range(0, len(customers), 2):
            col1, col2 = st.columns(2)
            for col, customer in zip([col1, col2], customers[i:i+2]):
                with col:
                    with st.container(border=True):
                        st.markdown(f"**👤 {customer['name']}**")
                        st.caption(f"📞 {customer['phone']}")
                        st.caption(f"📍 {customer['address']}")
                        if customer['email']:
                            st.caption(f"📧 {customer['email']}")
                        
                        # 操作按钮
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.button("编辑", key=f"edit_c_{customer['id']}", use_container_width=True):
                                st.session_state[f'edit_customer_{customer["id"]}'] = True
                        with btn_col2:
                            if st.button("删除", key=f"del_c_{customer['id']}", use_container_width=True):
                                if db.delete_customer(customer['id']):
                                    display_success("客户删除成功！")
                                    st.rerun()
                                else:
                                    display_error("无法删除：该客户存在关联订单。")
                        
                        # 编辑表单
                        if st.session_state.get(f'edit_customer_{customer["id"]}', False):
                            with st.form(f"edit_customer_form_{customer['id']}"):
                                edit_name = st.text_input("客户姓名", value=customer['name'])
                                edit_phone = st.text_input("联系电话", value=customer['phone'])
                                edit_email = st.text_input("邮箱", value=customer['email'] or "")
                                edit_address = st.text_input("地址", value=customer['address'])
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    if st.form_submit_button("保存", type="primary", use_container_width=True):
                                        db.update_customer(customer['id'], edit_name, edit_phone, edit_address, edit_email)
                                        display_success("客户信息更新成功！")
                                        del st.session_state[f'edit_customer_{customer["id"]}']
                                        st.rerun()
                                with col_cancel:
                                    if st.form_submit_button("取消", use_container_width=True):
                                        del st.session_state[f'edit_customer_{customer["id"]}']
                                        st.rerun()
    else:
        st.info("暂无客户数据，请添加客户信息。")


# ==================== 产品管理页面 ====================

def show_product_management():
    """显示产品管理页面"""
    st.title("🏷️ 产品管理")
    
    # 添加产品表单
    with st.expander("➕ 添加新产品", expanded=False):
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("产品名称 *", placeholder="例如：现代简约橱柜")
                category = st.selectbox("产品类别 *", ["整体橱柜", "定制柜", "吊柜", "地柜", "台面", "配件", "其他"])
            with col2:
                price = st.number_input("单价 (元) *", min_value=0.0, step=100.0, format="%.2f")
                unit = st.selectbox("单位 *", ["套", "平米", "件", "米"])
            
            description = st.text_area("产品描述", placeholder="请输入产品详细描述、规格等信息", height=100)
            
            if st.form_submit_button("添加产品", type="primary"):
                if name and category and price >= 0:
                    product_id = db.add_product(name, category, price, unit, description)
                    if product_id:
                        display_success("产品添加成功！")
                        st.rerun()
                    else:
                        display_error("添加失败，请重试。")
                else:
                    display_error("请填写所有必填项！")
    
    st.markdown("---")
    
    # 产品列表
    st.subheader("产品列表")
    products = db.get_all_products()
    
    if products:
        # 添加搜索和筛选
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("🔍 搜索产品", placeholder="输入产品名称搜索")
        with col2:
            category_filter = st.selectbox("按类别筛选", ["全部"] + list(set(p['category'] for p in products)))
        
        filtered_products = products
        if search:
            filtered_products = [p for p in filtered_products if search.lower() in p['name'].lower()]
        if category_filter != "全部":
            filtered_products = [p for p in filtered_products if p['category'] == category_filter]
        
        # 显示产品表格
        product_data = []
        for p in filtered_products:
            product_data.append({
                "ID": p['id'],
                "产品名称": p['name'],
                "类别": p['category'],
                "单价": format_price(p['price']),
                "单位": p['unit'],
                "描述": p['description'] or "-"
            })
        
        df = pd.DataFrame(product_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 编辑和删除操作
        st.markdown("#### 操作")
        selected_product = st.selectbox(
            "选择要操作的产品",
            options=[p['id'] for p in filtered_products],
            format_func=lambda x: f"{x} - {next(p['name'] for p in filtered_products if p['id'] == x)}"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("编辑产品", use_container_width=True):
                st.session_state[f'edit_product_{selected_product}'] = True
        with col2:
            if st.button("删除产品", use_container_width=True):
                if db.delete_product(selected_product):
                    display_success("产品删除成功！")
                    st.rerun()
                else:
                    display_error("无法删除：该产品存在关联订单。")
        
        # 编辑表单
        if st.session_state.get(f'edit_product_{selected_product}', False):
            product = next(p for p in products if p['id'] == selected_product)
            with st.expander("编辑产品信息", expanded=True):
                with st.form(f"edit_product_form_{selected_product}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_name = st.text_input("产品名称", value=product['name'])
                        edit_category = st.selectbox("产品类别", ["整体橱柜", "定制柜", "吊柜", "地柜", "台面", "配件", "其他"], 
                                                     index=["整体橱柜", "定制柜", "吊柜", "地柜", "台面", "配件", "其他"].index(product['category']))
                    with col2:
                        edit_price = st.number_input("单价 (元)", min_value=0.0, step=100.0, format="%.2f", value=product['price'])
                        edit_unit = st.selectbox("单位", ["套", "平米", "件", "米"], 
                                                index=["套", "平米", "件", "米"].index(product['unit']))
                    
                    edit_description = st.text_area("产品描述", value=product['description'] or "", height=100)
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("保存", type="primary", use_container_width=True):
                            db.update_product(selected_product, edit_name, edit_category, edit_price, edit_unit, edit_description)
                            display_success("产品信息更新成功！")
                            del st.session_state[f'edit_product_{selected_product}']
                            st.rerun()
                    with col_cancel:
                        if st.form_submit_button("取消", use_container_width=True):
                            del st.session_state[f'edit_product_{selected_product}']
                            st.rerun()
    else:
        st.info("暂无产品数据，请添加产品信息。")


# ==================== 订单管理页面 ====================

def show_order_management():
    """显示订单管理页面"""
    st.title("📦 订单管理")
    
    # 标签页
    tab1, tab2 = st.tabs(["创建订单", "订单列表"])
    
    # ==================== 创建订单 ====================
    with tab1:
        st.subheader("创建新订单")
        
        # 选择客户
        customers = db.get_all_customers()
        if not customers:
            st.warning("请先添加客户信息！")
            return
        
        customer_options = {f"{c['id']} - {c['name']} ({c['phone']})": c['id'] for c in customers}
        selected_customer_key = st.selectbox("选择客户 *", options=list(customer_options.keys()))
        selected_customer_id = customer_options[selected_customer_key]
        
        # 选择产品
        products = db.get_all_products()
        if not products:
            st.warning("请先添加产品信息！")
            return
        
        st.markdown("#### 添加产品到订单")
        
        # 显示可选产品
        product_options = {f"{p['name']} - {format_price(p['price'])}/{p['unit']}": p['id'] for p in products}
        selected_product_key = st.selectbox("选择产品", options=list(product_options.keys()))
        selected_product_id = product_options[selected_product_key]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            quantity = st.number_input("数量", min_value=0.1, step=0.1, value=1.0)
        with col2:
            product_info = next(p for p in products if p['id'] == selected_product_id)
            subtotal = product_info['price'] * quantity
            st.metric("小计", format_price(subtotal))
        
        # 添加到购物车
        if st.button("添加到订单", use_container_width=True, type="primary"):
            if 'order_items' not in st.session_state:
                st.session_state.order_items = []
            
            # 检查是否已存在该产品
            existing = next((item for item in st.session_state.order_items if item['product_id'] == selected_product_id), None)
            if existing:
                existing['quantity'] += quantity
            else:
                st.session_state.order_items.append({
                    'product_id': selected_product_id,
                    'quantity': quantity
                })
            
            display_success(f"已添加 {product_info['name']} x {quantity}")
        
        # 显示购物车
        if 'order_items' in st.session_state and st.session_state.order_items:
            st.markdown("#### 订单明细")
            
            total_amount = 0
            cart_items = []
            for item in st.session_state.order_items:
                product = next(p for p in products if p['id'] == item['product_id'])
                subtotal = product['price'] * item['quantity']
                total_amount += subtotal
                cart_items.append({
                    "产品名称": product['name'],
                    "单价": format_price(product['price']),
                    "数量": item['quantity'],
                    "单位": product['unit'],
                    "小计": format_price(subtotal),
                    "删除": f"删除_{item['product_id']}"
                })
            
            df = pd.DataFrame(cart_items)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.metric("订单总额", format_price(total_amount))
            
            # 删除项目
            for item in cart_items:
                if st.button("删除", key=item['删除'], use_container_width=True):
                    product_id = int(item['删除'].split('_')[1])
                    st.session_state.order_items = [i for i in st.session_state.order_items if i['product_id'] != product_id]
                    st.rerun()
            
            # 备注和提交
            st.markdown("---")
            notes = st.text_area("订单备注", placeholder="请输入备注信息（选填）")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("提交订单", type="primary", use_container_width=True):
                    success, message, order_id = db.create_order(selected_customer_id, st.session_state.order_items, notes)
                    if success:
                        display_success(message)
                        st.session_state.order_items = []
                        st.rerun()
                    else:
                        display_error(message)
            with col2:
                if st.button("清空订单", use_container_width=True):
                    st.session_state.order_items = []
                    st.rerun()
        else:
            st.info("请选择产品添加到订单中。")
    
    # ==================== 订单列表 ====================
    with tab2:
        st.subheader("订单列表")
        
        orders = db.get_all_orders()
        
        if orders:
            # 搜索和筛选
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                search = st.text_input("🔍 搜索订单", placeholder="输入订单号或客户姓名搜索")
            with col2:
                status_filter = st.selectbox("订单状态", ["全部", "待处理", "已确认", "生产中", "已完成", "已取消"])
            with col3:
                if st.button("导出订单", use_container_width=True):
                    export_orders(orders)
            
            filtered_orders = orders
            if search:
                filtered_orders = [o for o in filtered_orders if search.lower() in o['order_no'].lower() or search.lower() in o['customer_name'].lower()]
            if status_filter != "全部":
                filtered_orders = [o for o in filtered_orders if o['status'] == status_filter]
            
            # 显示订单
            for order in filtered_orders:
                with st.expander(f"📋 {order['order_no']} - {order['customer_name']} - {format_price(order['total_amount'])} - {order['status']}"):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("**订单信息**")
                        st.write(f"📞 客户电话: {order['customer_phone']}")
                        st.write(f"📅 创建时间: {order['created_at']}")
                        st.write(f"💰 总金额: {format_price(order['total_amount'])}")
                        if order['notes']:
                            st.write(f"📝 备注: {order['notes']}")
                    
                    with col2:
                        # 状态更新
                        new_status = st.selectbox(
                            "更新状态",
                            ["待处理", "已确认", "生产中", "已完成", "已取消"],
                            index=["待处理", "已确认", "生产中", "已完成", "已取消"].index(order['status']),
                            key=f"status_{order['id']}"
                        )
                        if st.button("更新状态", key=f"update_status_{order['id']}", use_container_width=True):
                            db.update_order_status(order['id'], new_status)
                            display_success("状态更新成功！")
                            st.rerun()
                        
                        # 查看明细
                        if st.button("查看订单明细", key=f"view_detail_{order['id']}", use_container_width=True):
                            order_detail = db.get_order(order['id'])
                            if order_detail:
                                st.markdown("**订单明细**")
                                for item in order_detail['items']:
                                    st.write(f"• {item['product_name']} x {item['quantity']} {item['unit']} = {format_price(item['subtotal'])}")
                        
                        # 删除订单
                        if st.button("删除订单", key=f"delete_{order['id']}", type="secondary", use_container_width=True):
                            if st.button("确认删除", key=f"confirm_delete_{order['id']}", type="primary"):
                                db.delete_order(order['id'])
                                display_success("订单删除成功！")
                                st.rerun()
        else:
            st.info("暂无订单数据。")


# ==================== 数据导出功能 ====================

def export_orders(orders):
    """导出订单数据为 CSV"""
    if not orders:
        st.warning("没有可导出的订单数据！")
        return
    
    # 准备导出数据
    export_data = []
    for order in orders:
        export_data.append({
            "订单编号": order['order_no'],
            "客户姓名": order['customer_name'],
            "客户电话": order['customer_phone'],
            "状态": order['status'],
            "总金额": order['total_amount'],
            "创建时间": order['created_at'],
            "备注": order['notes'] or ""
        })
    
    df = pd.DataFrame(export_data)
    
    # 生成 CSV
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    # 下载按钮
    st.download_button(
        label="下载订单数据 (CSV)",
        data=output,
        file_name=f"订单导出_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==================== 主程序 ====================

def main():
    """主程序入口"""
    
    # 侧边栏导航
    with st.sidebar:
        st.title("🏠 橱柜订单系统")
        st.markdown("---")
        
        page = st.radio(
            "导航菜单",
            ["📊 仪表盘", "👥 客户管理", "🏷️ 产品管理", "📦 订单管理"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.caption("© 2024 橱柜订单管理系统")
    
    # 页面路由
    if page == "📊 仪表盘":
        show_dashboard()
    elif page == "👥 客户管理":
        show_customer_management()
    elif page == "🏷️ 产品管理":
        show_product_management()
    elif page == "📦 订单管理":
        show_order_management()


if __name__ == "__main__":
    main()
