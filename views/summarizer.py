import requests

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
                "content": (
                    "你是一位專業法律助理，請閱讀以下合約內容，並用**繁體中文（台灣用法）**條列方式摘要重點。"
                    "請依序整理以下項目：合約目的、雙方義務、關鍵期限、金額、特殊條款。請保持語氣專業、簡潔、務實。"
                )
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
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.RequestException:
        return "❌ 摘要失敗：無法連線至 Groq API，請稍後再試。"

    except Exception:
        return "❌ 摘要失敗：發生未知錯誤，請聯絡管理員。"

