import os
import feedparser
from supabase import create_client, Client
from datetime import datetime

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# rss_feeds ={
#     "보안뉴스" : "https://www.boannews.com/media/news_rss.xml",
#     "The Hacker News" : "https://feeds.feedburner.com/TheHackersNews"
# }
def get_or_create_keyword_id(kw_name):
    kw_check = supabase.table("keyword").select("*").eq("keyword_name",kw_name).execute()
    if kw_check.data:
        return kw_check.data[0]["keyword_id"]
    else:
        new_kw=supabase.table("keyword").insert({
            "keyword_name":kw_name,
            "create_at":datetime.utcnow().isoformat()
        }).execute()
        return new_kw.data[0]["keyword_id"]
    

def get_or_create_rsskeyword_id(source_name):
    check = supabase.table("rsskeyword").select("*").eq("rsskeyword_name", source_name).execute()
    if check.data:
        return check.data[0]["rsskeyword_id"]
    else:
        new_row = supabase.table("rsskeyword").insert({
            "rsskeyword_name":source_name,
            "created_at":datetime.utcnow().isoformat()
        }).execute()
        return new_row.data[0]["rsskeyword_id"]



for entry in feed.entries:
    title = entry.get("title", "")
    content = entry.get("description","")
    link = entry.get("link","")
    crawled_at = datetime.utcnow().isoformat()


    keyword_id = get_or_create_keyword_id(matched_kw)
    rsskeyword_id = get_or_create_rsskeyword_id(source)
    
    exists = supabase.table("newsRss").select("newsrss_id").eq("link", link).execute()
    if exists.data:
        continue

    supabase.table("newsRss").insert({
        "title":title,
        "description":content,
        "link":link,
        "created_at":crawled_at,
        "keyword_id":keyword_id,
        "rsskeyword_id":rsskeyword_id
    }).execute()
