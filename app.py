import os  # 导入 os 模块
import json
import gspread
import streamlit as st
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# 🔹 设置 Google Sheets API 凭证
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 从 Streamlit Secrets 中读取 Google OAuth 凭证
google_credentials = st.secrets["google_credentials"]

# 保存凭证信息到本地文件
creds_file = 'token.json'  # 用于存储用户的 OAuth 2.0 凭证

# 将凭证信息转换为字典格式并保存为 json 文件
credentials_dict = {
    "installed": {
        "client_id": google_credentials["client_id"],
        "project_id": google_credentials["project_id"],
        "auth_uri": google_credentials["auth_uri"],
        "token_uri": google_credentials["token_uri"],
        "auth_provider_x509_cert_url": google_credentials["auth_provider_x509_cert_url"],
        "client_secret": google_credentials["client_secret"],
        "redirect_uris": google_credentials["redirect_uris"],
        "javascript_origins": google_credentials["javascript_origins"]
    }
}

# 写入文件
with open(creds_file, 'w') as f:
    json.dump(credentials_dict, f)

# 从文件加载 OAuth 2.0 凭证
creds = None

# 如果 token.json 存在，加载凭证
if creds_file and os.path.exists(creds_file):
    creds = Credentials.from_authorized_user_file(creds_file, scope)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

# 如果没有凭证或凭证过期，则执行授权流程
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            creds_file, scope)
        creds = flow.run_local_server(port=0)

    # 保存凭证，以便下次使用
    with open(creds_file, 'w') as token:
        token.write(creds.to_json())

# 🔹 连接到 Google Sheets
client = gspread.authorize(creds)
st.success("Successfully connected to Google Sheets!")

# 🔹 打开 Google Sheets
sheet = client.open("menu-order").sheet1  # 确保文件名为 `menu-order`
st.success("Successfully opened the Google Sheets file!")

# 🔹 读取已有菜单
menu_list = sheet.col_values(1)  # 读取第一列（菜品列表）
if menu_list:
    st.subheader("📜 Current Menu")
    st.table(menu_list)  # 使用表格形式展示菜单
else:
    st.write("The menu is currently empty. Please add some dishes!")

# 页面标题
st.title("🍽️ Menu Order")

# 输入框
dish = st.text_input("Enter the dish you want:")

# 添加按钮
if st.button("Add"):
    if dish:
        try:
            sheet.append_row([dish])  # 将新菜品添加到 Google Sheets
            st.success(f"✅ Added: {dish}")
            menu_list.append(dish)  # 更新菜单列表
        except Exception as e:
            st.error(f"Error adding dish to Google Sheets: {e}")
    else:
        st.warning("Please enter a dish name.")  # 提示输入内容
