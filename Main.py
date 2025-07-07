# main.py
import streamlit as st
from utils.drive_utils import list_pdfs_from_drive, download_pdf
from views.summarizer import summarize_text
import base64

st.set_page_config(page_title="📄 合約摘要系統", layout="wide")
st.title("📄 合約摘要系統")

# 從 secrets 取得資料
folder_id = st.secrets["GOOGLE_DRIVE_FOLDER_ID"]
groq_api_key = st.secrets["GROQ_API_KEY"]

# 📂 從 Google Drive 取得所有 PDF 檔案清單
pdf_files = list_pdfs_from_drive(folder_id)

# 左側選單：選擇 PDF 檔案
st.sidebar.title("請選擇合約檔案")
if not pdf_files:
    st.sidebar.warning("找不到任何 PDF 檔案")
    st.stop()

file_names = [file["name"] for file in pdf_files]
selected_name = st.sidebar.selectbox("合約清單", file_names)

# 找到所選檔案對應的 ID
selected_file = next((f for f in pdf_files if f["name"] == selected_name), None)
if not selected_file:
    st.error("⚠️ 找不到所選檔案")
    st.stop()

# 🧾 顯示 PDF 原始檔案（使用 Google Drive 預覽或內嵌 PDF）
st.subheader(f"📎 原始合約：{selected_name}")
pdf_url = f"https://drive.google.com/file/d/{selected_file['id']}/preview"
st.markdown(
    f'<iframe src="{pdf_url}" width="100%" height="500px" frameborder="0" allow="autoplay"></iframe>',
    unsafe_allow_html=True
)

# 🧠 摘要區塊
if st.button("📌 產生合約摘要"):
    with st.spinner("LLM 摘要中，請稍候..."):
        file_bytes = download_pdf(selected_file["id"])
        # 不轉文字，僅摘要
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc if page.get_text())

        if not text.strip():
            st.warning("⚠️ 無法從 PDF 解析出有效文字內容。")
        else:
            summary = summarize_text(text, groq_api_key)
            st.subheader("🧠 合約摘要結果")
            st.success(summary)

