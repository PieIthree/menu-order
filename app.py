import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import gspread

# 🔹 获取 Google Sheets API 凭证
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 从环境变量中读取 Google OAuth 凭证
credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)

# 🔹 连接 Google Sheets
client = None
try:
    client = gspread.authorize(creds)
    st.success("Successfully connected to Google Sheets!")
except Exception as e:
    st.error(f"Error connecting to Google Sheets: {e}")
    st.stop()  # 停止进一步的执行

# 🔹 打开 Google Sheets
try:
    sheet = client.open("menu-order").sheet1  # 确保名字是 `menu-order`
except Exception as e:
    st.error(f"Error opening the Google Sheets file: {e}")
    st.stop()  # 停止进一步的执行

# 🔹 读取已有菜单
menu_list = sheet.col_values(1)  # 读取第一列（菜品列表）

# 页面标题
st.title("🍽️ Menu Order")

# 输入框
dish = st.text_input("Enter the dish you want:")

# 添加按钮
if st.button("Add"):
    if dish:
        try:
            sheet.append_row([dish])  # 添加到 Google Sheets
            st.success(f"✅ Added: {dish}")
        except Exception as e:
            st.error(f"Error adding dish to Google Sheets: {e}")
    else:
        st.warning("Please enter a dish name.")  # 提示输入内容

# 显示当前菜单
if menu_list:
    st.subheader("📜 Current Menu")
    st.write(menu_list)
else:
    st.write("The menu is currently empty. Please add some dishes!")  # 如果菜单为空，显示提示
