import requests
import streamlit as st  # 用於顯示錯誤（開發階段）

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def summarize_text(text, api_key):
    if not text.strip():
        return "❌ 無法摘要：輸入內容為空。"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "你是一位專業法律助理，請閱讀以下合約內容，並用條列式方式摘要重點，包含：合約目的、雙方義務、關鍵期限、金額、特殊條款。"
            },
            {
                "role": "user",
                "content": text[:8000]  # 避免超過 Groq token 限制
            }
        ],
        "temperature": 0.4
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # 若不是 2xx，會拋出 HTTPError

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.HTTPError as http_err:
        # 顯示詳細錯誤資訊（便於除錯）
        st.error("❌ HTTP 錯誤")
        st.error(f"狀態碼：{http_err.response.status_code}")
        st.error(f"錯誤訊息：{http_err.response.text}")

        print("🚨 HTTP Error:")
        print(f"Status Code: {http_err.response.status_code}")
        print(f"Response Text: {http_err.response.text}")
        print(f"API Key Prefix: {api_key[:6]}... (已隱藏其餘部分)")
        print(f"URL: {GROQ_API_URL}")

        return f"❌ 摘要失敗：{http_err.response.status_code} - {http_err.response.text}"

    except Exception as e:
        # 其他未知錯誤
        st.error("❌ 發生其他錯誤")
        st.error(str(e))
        print("❌ Unknown Error:", repr(e))
        return f"❌ 摘要失敗：{e}"
