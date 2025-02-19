import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 连接 Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("menu-order-451315-b0213b6ad336.json", scope)
client = gspread.authorize(creds)

# 🔹 打开 Google Sheets
sheet = client.open("menu-order").sheet1  # 使用表格名 menu-order

# 🔹 读取已有菜单
menu_list = sheet.col_values(1)  # 读取第一列（菜品列表）

st.title("🍽️ Menu Order")  # 页面标题

# 输入框
dish = st.text_input("Enter the dish you want:")

# 添加按钮
if st.button("Add"):
    if dish:
        sheet.append_row([dish])  # 添加到 Google Sheets
        st.success(f"✅ Added: {dish}")

# 删除按钮
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

