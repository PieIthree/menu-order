import os
import json
import toml
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 获取 Google Sheets API 凭证
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 从环境变量中读取 TOML 格式的凭证
google_credentials_toml = os.getenv("GOOGLE_CREDENTIALS")
credentials_info = toml.loads(google_credentials_toml)["GOOGLE_CREDENTIALS"]

# 将 TOML 数据转换为 JSON 格式，供 oauth2client 使用
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)

# 🔹 连接 Google Sheets
client = gspread.authorize(creds)

# 🔹 打开 Google Sheets
sheet = client.open("menu-order").sheet1  # 使用 `menu-order`

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

# 显示当前菜单
st.subheader("📜 Current Menu")
st.write(menu_list)
