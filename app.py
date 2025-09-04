# app.py —— 安全版（先兼容你现有文件名）
import os
import json
import streamlit as st
import gspread
from google.oauth2 import service_account

# ====== 配置 ======
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
SHEET_NAME = "menu-order"
FINAL_SHEET_TITLE = "final-menu"

# ====== 构建凭据 ======
def build_credentials():
    # 1) Streamlit secrets
    try:
        if "gcp_service_account" in st.secrets:
            info = dict(st.secrets["gcp_service_account"])
            return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    except Exception:
        pass

    # 2) 环境变量
    key_json = os.environ.get("GCP_KEY_JSON")
    if key_json:
        info = json.loads(key_json)
        return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

    # 3) 本地文件（你当前用的文件名）
    key_path = "menu-order-451315-b0213b6ad336.json"
    if os.path.exists(key_path):
        return service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)

    raise RuntimeError("找不到 GCP 凭据，请检查文件或 secrets 设置。")

creds = build_credentials()
gc = gspread.authorize(creds)

# ====== 管理员密码（先写死，后面可以迁移到 secrets） ======
ADMIN_PASSWORD = "stone6681"

# ====== 连接工作表 ======
sh = gc.open(SHEET_NAME)
sheet = sh.sheet1
final_sheet = sh.worksheet(FINAL_SHEET_TITLE)

# ====== UI 部分 ======
st.title("🍽 Menu Order")
st.header("✅ Finalized Menu")

# 管理员登录
password_input = st.text_input("管理员密码：", type="password", value="")
is_admin = (password_input == ADMIN_PASSWORD and ADMIN_PASSWORD != "")

# ---- Finalized Menu 显示与删除 ----
final_menu = final_sheet.col_values(1)
if final_menu:
    for i, item in enumerate(final_menu, start=1):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{i}. {item}")
        with col2:
            if is_admin and st.button(f"Delete {item}", key=f"final_delete_{i}"):
                final_sheet.delete_rows(i)
                st.success(f"❌ Deleted: {item}")
                st.rerun()
else:
    st.write("暂无最终确定的菜品。")

# ---- Finalized Menu 添加 ----
if is_admin:
    st.success("管理员已登录")
    final_item = st.text_input("添加最终确定的菜品：", key="final_input")
    if st.button("添加到最终菜单"):
        if final_item.strip():
            final_sheet.append_row([final_item.strip()])
            st.success(f"✅ {final_item.strip()} 已添加到最终菜单")
            st.rerun()
else:
    st.info("如需添加或删除最终菜单，请输入管理员密码。")

st.divider()

# ====== 普通菜单管理 ======
st.subheader("📜 Current Menu")
dish = st.text_input("Enter the dish you want:")
if st.button("Add"):
    if dish.strip():
        sheet.append_row([dish.strip()])
        st.success(f"✅ Added: {dish.strip()}")
        st.rerun()

menu_list = sheet.col_values(1)
if menu_list:
    for i, dish_name in enumerate(menu_list, start=1):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{i}. {dish_name}")
        with col2:
            if st.button(f"Delete {dish_name}", key=f"menu_delete_{i}"):
                sheet.delete_rows(i)
                st.success(f"❌ Deleted: {dish_name}")
                st.rerun()
else:
    st.write("No menu items yet.")
