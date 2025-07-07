import streamlit as st
from utils.drive_utils import list_pdfs_from_drive, download_pdf
from views.summarizer import summarize_text
from PyPDF2 import PdfReader
import io
import base64

st.set_page_config(page_title="📄 合約摘要系統", layout="wide")
st.title("📄 合約摘要系統")

# 🔐 讀取 secrets
folder_id = st.secrets["GOOGLE_DRIVE_FOLDER_ID"]
groq_api_key = st.secrets["GROQ_API_KEY"]

# 📂 取得 PDF 清單
pdf_files = list_pdfs_from_drive(folder_id)

if not pdf_files:
    st.warning("找不到任何 PDF 檔案，請確認資料夾中是否有 PDF。")
    st.stop()

# 📑 選擇要檢視的 PDF
file_names = [file["name"] for file in pdf_files]
selected_file_name = st.selectbox("📁 選擇要檢視的合約：", file_names)

# 取得選定檔案的 ID
selected_file = next(file for file in pdf_files if file["name"] == selected_file_name)
file_id = selected_file["id"]

# 產生 Google Drive PDF Viewer 的嵌入網址
viewer_url = f"https://drive.google.com/file/d/{file_id}/preview"

# 📄 顯示 PDF 原始檔案（可滾輪瀏覽）
st.markdown("### 📄 合約原文")
st.components.v1.iframe(viewer_url, height=600, width=900)

# 🧠 顯示產生摘要按鈕
if st.button("🧠 產生摘要"):
    with st.spinner("AI 摘要生成中，請稍候..."):
        file_bytes = download_pdf(file_id)
        reader = PdfReader(io.BytesIO(file_bytes))
        full_text = "".join(page.extract_text() for page in reader.pages if page.extract_text())

        if not full_text:
            st.error("❌ 無法擷取 PDF 文字內容，請確認檔案是否為掃描圖檔。")
        else:
            summary = summarize_text(full_text, groq_api_key)
            st.markdown("### ✨ 合約摘要")
            st.success(summary)

