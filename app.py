import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread.exceptions

# 🔹 连接 Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("menu-order-451315-b0213b6ad336.json", scope)
client = gspread.authorize(creds)

# 🔹 打开待选菜谱工作表 (sheet1)
sheet = client.open("menu-order").sheet1

# 🔹 尝试打开最终菜谱工作表 ("final-menu"); 如果不存在则创建
try:
    final_sheet = client.open("menu-order").worksheet("final-menu")
except gspread.exceptions.WorksheetNotFound:
    final_sheet = client.open("menu-order").add_worksheet(title="final-menu", rows="100", cols="2")

# 🔹 获取当前数据
menu_list = sheet.col_values(1)        # 普通菜谱列表
final_menu = final_sheet.col_values(1)   # 最终确定菜谱列表

# ─────────────────────────────
# 1. 显示最终确定菜谱（顶部）
st.header("✅ Finalized Menu")
if final_menu:
    for i, item in enumerate(final_menu, start=1):
        st.write(f"{i}. {item}")
else:
    st.write("暂无最终确定的菜品。")

# ─────────────────────────────
# 2. 管理员区域：只有管理员才能添加最终确定的菜品
admin_password = "stone6681"  # 请替换成你的管理员密码
password_input = st.text_input("管理员密码：", type="password")

if password_input == admin_password:
    st.success("管理员已登录")
    final_item = st.text_input("添加最终确定的菜品：", key="final_input")
    if st.button("添加到最终菜谱"):
        if final_item:
            final_sheet.append_row([final_item])
            st.success(f"✅ {final_item} 已添加到最终菜谱")
            final_menu = final_sheet.col_values(1)  # 更新最终菜谱数据
else:
    st.warning("请输入管理员密码以添加最终菜谱。")

# ─────────────────────────────
# 3. 普通用户区：添加和删除普通菜品
st.title("🍽️ Menu Order")

# 添加菜品
dish = st.text_input("Enter the dish you want:", key="dish_input")
if st.button("Add"):
    if dish:
        sheet.append_row([dish])
        st.success(f"✅ Added: {dish}")

# 显示当前待选菜单并提供删除按钮
st.subheader("📜 Current Menu")
if menu_list:
    # 使用 for 循环展示每个菜品，并添加删除按钮
    for i, dish_name in enumerate(menu_list, start=1):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{i}. {dish_name}")
        with col2:
            # 按钮的 key 使用 "delete_菜品序号" 保证唯一性
            if st.button(f"Delete", key=f"delete_{i}"):
                sheet.delete_rows(i)
                st.success(f"❌ Deleted: {dish_name}")
                # 删除后更新菜单数据
                menu_list = sheet.col_values(1)
else:
    st.write("No menu items yet.")
