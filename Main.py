# Main.py

import streamlit as st
from utils.drive_utils import list_pdfs_from_drive, download_pdf
from views.summarizer import summarize_text
import fitz  # PyMuPDF

st.set_page_config(page_title="📄 合約摘要系統", layout="wide")
st.title("📄 合約摘要系統")

# 讀取機密資訊
folder_id = st.secrets["GOOGLE_DRIVE_FOLDER_ID"]
groq_api_key = st.secrets["GROQ_API_KEY"]

# 讀取 Google Drive 裡的所有 PDF 檔案
pdf_files = list_pdfs_from_drive(folder_id)

if not pdf_files:
    st.warning("❗ 找不到任何 PDF 檔案，請確認 Google Drive 資料夾中有檔案。")
else:
    with st.sidebar:
        selected_file = st.selectbox("選擇檔案", pdf_files, format_func=lambda x: x['name'])

    st.subheader(f"合約：{selected_file['name']}")
    st.markdown(f"[查看原始檔案（Google Drive）](https://drive.google.com/file/d/{selected_file['id']}/view)")

    # 載入 PDF 檔案
    file_bytes = download_pdf(selected_file['id'])
    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")

    # 顯示 PDF 頁面（以圖片呈現）
    for page_num in range(len(pdf_doc)):
        page = pdf_doc[page_num]
        image = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 高解析度
        st.image(image.tobytes("png"), caption=f"第 {page_num + 1} 頁", use_column_width=True)

    st.divider()

    # 產生摘要按鈕
    st.subheader("合約摘要")
    if st.button("摘要"):
        with st.spinner("LLM 正在產生摘要..."):
            full_text = "\n".join(page.get_text() for page in pdf_doc)
            summary = summarize_text(full_text, groq_api_key)
            st.success(summary)
