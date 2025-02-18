import os
import toml
import json
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import gspread

# 🔹 获取 Google Sheets API 凭证
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 从环境变量中读取 Google OAuth 凭证（TOML 格式）
credentials_info = os.getenv("GOOGLE_CREDENTIALS")
if credentials_info is None:
    st.error("Google credentials are not set in environment variables!")
    st.stop()  # 停止执行

# 解析 TOML 格式并转换为字典
try:
    credentials_dict = toml.loads(credentials_info)
    # 如果需要，可以在这里检查字典的结构是否符合 Google API 的要求
except toml.TomlDecodeError:
    st.error("Error decoding the TOML credentials!")
    st.stop()  # 停止执行

# 将 TOML 数据转换为 JSON 格式
try:
    credentials_json = json.dumps(credentials_dict)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(credentials_json), scope)
except json.JSONDecodeError:
    st.error("Error encoding credentials to JSON format!")
    st.stop()  # 停止执行

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
            menu_list.append(dish)  # 实时更新菜单
        except Exception as e:
            st.error(f"Error adding dish to Google Sheets: {e}")
    else:
        st.warning("Please enter a dish name.")  # 提示输入内容

# 显示当前菜单
if menu_list:
    st.subheader("📜 Current Menu")
    st.table(menu_list)  # 使用表格形式展示菜单
else:
    st.write("The menu is currently empty. Please add some dishes!")  # 如果菜单为空，显示提示
