import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import gspread

# 🔹 设置 Google Sheets API 凭证
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 从环境变量中读取 Google OAuth 凭证
credentials_info = os.getenv("GOOGLE_CREDENTIALS")

if credentials_info is None:
    st.error("Google credentials are not set in environment variables!")
else:
    try:
        # 将凭证字符串转换为字典
        credentials_dict = json.loads(credentials_info)
        # 使用凭证字典进行授权
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

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

    except Exception as e:
        st.error(f"Error loading Google credentials or connecting to Google Sheets: {e}")
