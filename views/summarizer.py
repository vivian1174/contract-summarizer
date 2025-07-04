# views/summarizer.py
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def summarize_text(text, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "你是一位專業法律助理，請閱讀以下合約內容，並用條列式方式摘要重點，包含：合約目的、雙方義務、關鍵期限、金額、特殊條款。"},
            {"role": "user", "content": text[:12000]}  # 避免超長字數
        ],
        "temperature": 0.4
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ 摘要失敗：{e}"