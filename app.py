import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 连接 Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("menu-order-451315-b0213b6ad336.json", scope)
client = gspread.authorize(creds)

# 🔹 打开 Google Sheets
sheet = client.open("menu-order").sheet1  # 使用表格名 menu-order
final_sheet = client.open("menu-order").worksheet("final-menu")  # 使用表格名 final-menu

# 🔹 读取已有菜单
menu_list = sheet.col_values(1)  # 读取第一列（菜品列表）
final_menu = final_sheet.col_values(1)  # 读取最终菜单（第一列）

# 管理员密码配置（你可以修改这个密码）
admin_password = "stone6681"  # 请替换成你的管理员密码
password_input = st.text_input("管理员密码：", type="password")  # 输入框接收密码

# ─────────────────────────────
# 最终菜单管理
st.header("✅ Finalized Menu")
if final_menu:
    for i, item in enumerate(final_menu, start=1):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{i}. {item}")  # 显示最终菜单项
        with col2:
            if password_input == admin_password:  # 只有输入正确密码的管理员可以删除
                if st.button(f"Delete {item}", key=f"final_delete_{i}"):
                    final_sheet.delete_rows(i)  # 删除最终菜单中的该行
                    st.success(f"❌ Deleted: {item}")  # 显示删除提示
                    final_menu = final_sheet.col_values(1)  # 更新最终菜单列表
else:
    st.write("暂无最终确定的菜品。")

# ─────────────────────────────
# 管理员区域：添加最终菜单
if password_input == admin_password:
    st.success("管理员已登录")  # 显示管理员登录信息
    final_item = st.text_input("添加最终确定的菜品：", key="final_input")
    if st.button("添加到最终菜单"):
        if final_item:
            final_sheet.append_row([final_item])  # 添加到最终菜单
            st.success(f"✅ {final_item} 已添加到最终菜单")
else:
    st.warning("请输入管理员密码以添加或删除最终菜单。")

# ─────────────────────────────
# 普通菜单管理
st.title("🍽 Menu Order")  # 页面标题

# 添加待选菜品
dish = st.text_input("Enter the dish you want:")
if st.button("Add"):
    if dish:
        sheet.append_row([dish])  # 添加到 Google Sheets
        st.success(f"✅ Added: {dish}")

# 删除待选菜品
# 显示当前菜单并提供删除选项
st.subheader("📜 Current Menu")
if menu_list:
    for i, dish_name in enumerate(menu_list, start=1):  # 遍历菜单，显示索引和菜名
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{i}. {dish_name}")  # 显示菜名和索引
        with col2:
            if st.button(f"Delete {dish_name}", key=i):  # 为每道菜添加删除按钮
                # 删除菜品的操作
                sheet.delete_rows(i)  # 删除 Google Sheets 中的该行
                st.success(f"❌ Deleted: {dish_name}")  # 显示删除提示
                menu_list = sheet.col_values(1)  # 更新菜单列表
else:
    st.write("No menu items yet.")  # 如果菜单为空，显示提示信息
