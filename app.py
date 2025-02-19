import gspread
import streamlit as st
from google.auth import exceptions
from google.oauth2.service_account import Credentials

# 🔹 Google Sheets API Scopes
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# 🔹 Path to your service account credentials file
creds_file = '/path/to/menu-order-451315-b0213b6ad336.json'

# 🔹 Load credentials from the service account file
try:
    creds = Credentials.from_service_account_file(creds_file, scopes=scope)
    client = gspread.authorize(creds)
    st.success("Successfully connected to Google Sheets!")
except exceptions.GoogleAuthError as auth_error:
    st.error(f"Authentication failed: {auth_error}")
    st.stop()

# 🔹 Open the Google Sheets document
try:
    sheet = client.open("menu-order").sheet1  # Ensure the sheet is named `menu-order`
    st.success("Successfully opened the Google Sheets file!")
except gspread.exceptions.SpreadsheetNotFound:
    st.error("The specified spreadsheet was not found.")
    st.stop()

# 🔹 Reading the current menu (first column)
menu_list = sheet.col_values(1)
if menu_list:
    st.subheader("📜 Current Menu")
    st.table(menu_list)
else:
    st.write("The menu is currently empty. Please add some dishes!")

# Page title
st.title("🍽️ Menu Order")

# Input field for adding new dish
dish = st.text_input("Enter the dish you want:")

# Add button
if st.button("Add"):
    if dish:
        try:
            sheet.append_row([dish])  # Append new dish to the Google Sheets
            st.success(f"✅ Added: {dish}")
            menu_list.append(dish)  # Update menu list displayed
        except Exception as e:
            st.error(f"Error adding dish to Google Sheets: {e}")
    else:
        st.warning("Please enter a dish name.")
