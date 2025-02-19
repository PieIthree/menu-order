import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 连接 Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("你的_google_api_key.json", scope)
client = gspread.authorize(creds)

# 🔹 打开 Google Sheets
sheet = client.open("menu-order").sheet1  # ✅ 使用 `menu-order`

# 🔹 读取已有菜单
menu_list = sheet.col_values(1)  # 读取第一列（菜品列表）

st.title("🍽️ Menu Order")  # ✅ 使用 `Menu Order`

# 输入框
dish = st.text_input("Enter the dish you want:")

# 添加按钮
if st.button("Add"):
    if dish:
        sheet.append_row([dish])  # 添加到 Google Sheets
        st.success(f"✅ Added: {dish}")

# 显示当前菜单
st.subheader("📜 Current Menu")
st.write(menu_list)
