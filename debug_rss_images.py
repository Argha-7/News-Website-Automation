import feedparser
import json

def debug_rss_structure():
    url = "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en"
    print(f"Fetching {url}...")
    feed = feedparser.parse(url)
    
    if feed.entries:
        entry = feed.entries[0]
        print("Keys in entry:", entry.keys())
        
        # Check standard image fields
        if 'media_content' in entry:
            print("media_content:", entry.media_content)
        if 'media_thumbnail' in entry:
            print("media_thumbnail:", entry.media_thumbnail)
        if 'links' in entry:
            print("links:", json.dumps(entry.links, indent=2))
        
        print("Description sample:", entry.description[:500])
    else:
        print("No entries found.")

if __name__ == "__main__":
    debug_rss_structure()
