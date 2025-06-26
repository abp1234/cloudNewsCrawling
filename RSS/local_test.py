import feedparser
from datetime import datetime, timedelta,timezone

# ✅ 키워드 리스트 (영/한)
keywords = [
    "클라우드", "cloud",
    "클라우드 보안", "cloud security",
    "CSAP", "csap",
    "해킹", "hacking",
    "정보보안", "information security",
    "보안", "security",
    "SaaS", "IaaS", "skt"
]

# ✅ RSS 피드 목록
rss_feeds = {
    "보안뉴스": "https://www.boannews.com/media/news_rss.xml",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
}
def fetch_recent_news():
    # 하루 전 시각 계산
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)

    print("📰 [테스트 시작] 최근 1일 이내, 키워드 포함된 뉴스만 출력합니다.\n")
    news_items = []
    # RSS 순회
    for source, url in rss_feeds.items():
        print(f"🔍 {source} RSS 분석 중...")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.get("title", "")
            content = entry.get("description", "")
            link = entry.get("link", "")

            # 날짜 필터
            if hasattr(entry, "published_parsed"):
                pub_time = datetime(*entry.published_parsed[:6]).replace(tzinfo=timezone.utc)
            elif hasattr(entry, "updated_parsed"):
                pub_time = datetime(*entry.updated_parsed[:6]).replace(tzinfo=timezone.utc)
            else:
                continue

            if pub_time < yesterday:
                continue

            # 키워드 필터
            combined = (title + content).lower()
            matched_kw = next((kw for kw in keywords if kw.lower() in combined), None)
            if not matched_kw:
                continue
            news_items.append({
                "title": title,
                "description": content,
                "link": link,
                "source": source,
                "matched_kw": matched_kw,
                "pub_time": pub_time
            })
            # 출력
            print(f"   [{source}] {title}")
            print(f"   ⏰ {pub_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   🔗 {link}")
            print(f"   📎 매칭 키워드: {matched_kw}")
            print()
    return news_items
    # GPT 요약 및 이메일 본문 생성
#email_text = build_email_body(news_items)
# print("\n\n===== ✉️ 최종 이메일 내용 (로컬 출력) =====\n")
# print(email_text)