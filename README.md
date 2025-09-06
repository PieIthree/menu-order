# Sheet Sync

一个基于 **Python + Streamlit + Google Sheets** 的小型信息收集与管理系统。  
用户可以通过网页提交数据，管理员则可以统一整理和管理，所有内容都会实时同步到云端表格。  

## 功能 Features
- 网页端表单输入，数据即时写入 Google Sheets  
- 管理端可对收集到的信息进行增删改查  
- 实时更新，避免遗漏和统计混乱  
- 使用 `.gitignore` 与 Secrets 管理，确保数据安全  

## 技术栈 Tech Stack
- **前端**: Streamlit  
- **后端**: Google Cloud IAM Service Account + gspread  
- **存储**: Google Sheets  
- **版本管理**: GitHub  
