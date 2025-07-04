# main.py
import streamlit as st
from utils.drive_utils import list_pdfs_from_drive, download_pdf
from views.summarizer import summarize_text
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="📄 合約摘要系統")
st.title("📄 合約摘要系統")

# 讀取 secrets
folder_id = st.secrets["GOOGLE_DRIVE_FOLDER_ID"]
groq_api_key = st.secrets["GROQ_API_KEY"]

# 從 Google Drive 取得 PDF 檔案清單
pdf_files = list_pdfs_from_drive(folder_id)

if not pdf_files:
    st.warning("找不到任何 PDF 檔案。請確認 Google Drive 資料夾內有 PDF。")
else:
    for file in pdf_files:
        with st.expander(file['name']):
            file_bytes = download_pdf(file['id'])
            reader = PdfReader(io.BytesIO(file_bytes))
            text = "".join(page.extract_text() for page in reader.pages if page.extract_text())

            st.markdown(f"[📎 查看原始檔案](https://drive.google.com/file/d/{file['id']}/view)")
            st.text_area("📃 原文預覽", text[:1000] + "...", height=200)

            if st.button("🧠 產生摘要", key=file['id']):
                with st.spinner("LLM 摘要中..."):
                    summary = summarize_text(text, groq_api_key)
                    st.markdown("### ✨ 合約摘要")
                    st.success(summary)
