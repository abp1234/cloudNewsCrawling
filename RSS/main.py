from local_test import fetch_recent_news
from summarize import build_email_body
from send_email import send_email
if __name__ == "__main__":
    news_items = fetch_recent_news()
    email_text = build_email_body(news_items)
    print("\n\n===== ✉️ 최종 이메일 내용 =====\n")
    print(email_text)
    send_email("클라우드 보안 일일 뉴스 동향", email_text)

