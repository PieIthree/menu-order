import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# 🔹 获取 Google Sheets API 凭证
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 从环境变量中读取 Google OAuth 凭证
credentials_info = os.getenv("GOOGLE_CREDENTIALS")

if credentials_info is None:
    print("Google credentials are not set in environment variables!")
else:
    try:
        credentials_dict = json.loads(credentials_info)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        
        # 🔹 连接 Google Sheets
        client = gspread.authorize(creds)
        print("Successfully connected to Google Sheets!")
        
        # 🔹 打开 Google Sheets
        sheet = client.open("menu-order").sheet1  # 确保名字是 `menu-order`
        print("Successfully opened the Google Sheets file!")
        
        # 🔹 读取已有菜单
        menu_list = sheet.col_values(1)  # 读取第一列（菜品列表）
        print("Current Menu:", menu_list)
    except Exception as e:
        print(f"Error loading Google credentials or connecting to Google Sheets: {e}")
