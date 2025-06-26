#import openai
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
def translate_text_gemmini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = { "Content-Type": "application/json" }
    prompt = f"""
If the following text is already in Korean, just repeat it as is.
Otherwise, translate it into Korean.

Text: {text}

Translation:
"""
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    translation = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    return translation


import requests


def translate_to_korean(text: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    prompt = f"""
Translate the following text into Korean. If the text is already in Korean, just return it as is.

Text: {text}
"""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }

    response = requests.post(url, headers=headers, json=data)
    print("📦 응답 상태코드:", response.status_code)
    print("📦 응답 본문:", response.text)
    return response.json()["choices"][0]["message"]["content"].strip()



def summarize_with_mixtral(title, content):
    prompt = f"""
당신은 보안/클라우드 뉴스 요약봇입니다.

아래 뉴스의 제목과 내용을 바탕으로 "클라우드 보안", "침해사고 원인과 결과", "주요내용" 중심으로 요약해줘.

형식:
- 문장 1줄 (침해사고 원인이나 클라우드 보안 이슈)
- 문장 1줄 (결과나 조치 사항)

제목: {title}
내용: {content}

요약:
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4
        }
    )
    print(response)
    #response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
def summarize_news_gemmini(title, content):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = { "Content-Type": "application/json" }
    prompt = f"""
당신은 보안/클라우드 뉴스 요약봇입니다.

다음 뉴스의 제목과 내용을 바탕으로 **"클라우드 보안", "침해사고 원인과 결과", "주요내용"** 중심으로 요약해줘.

요약 형식은 아래처럼 해줘:
 문장 1줄 (침해사고 원인이나 클라우드 보안 이슈)
 문장 1줄 (결과나 조치 사항)

제목: {title}
내용: {content}

요약:
"""
    data = {
        "contents": [
            {
                "parts": [
                    { "text": prompt }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()

def build_email_body(news_items):
    result = []

    for item in news_items:
        title = translate_to_korean(item['title'])
        content = item['description']
        link = item['link']
        summary = summarize_with_mixtral(title, content)

        formatted = f"""o  {title}

{summary.replace('\n', '- \n')}

{link}\n"""
        result.append(formatted)


    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"]


    today = datetime.today()


    formatted_date = today.strftime(f"%Y년 %m월 %d일({weekday_kr[today.weekday()]})")


    email_body = f"안녕하세요. 클라우드 인증팀 나경준입니다.\n\n{formatted_date} 뉴스 동향공유드립니다.\n\n" \
             "## 클라우드 보안 및 사이버 공격 관련\n\n" + "\n".join(result) + \
             "\n\n일일동향 전체 자료 위치 : T:\\10000 개인 백업\\나경준\\일일 클라우드_보안_관련_동향조사\n\n감사합니다."

    
    return email_body
