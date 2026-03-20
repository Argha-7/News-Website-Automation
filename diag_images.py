import requests
from news_fetcher_rss import fetch_trending_news, get_og_image
import logging

logging.basicConfig(level=logging.INFO)

def diag_images():
    print("--- Image Fetching Diagnostic ---")
    
    # Fetch some news
    articles = fetch_trending_news(category='technology', country='IN', skip_heavy_ops=False)
    
    print(f"\nFound {len(articles)} articles.")
    for i, art in enumerate(articles[:10]):
        title = art['title']
        img_url = art['urlToImage']
        orig_url = art['url']
        
        print(f"\n[{i+1}] Title: {title[:60]}...")
        print(f"    Original URL: {orig_url}")
        
        if img_url:
            print(f"    Image URL: {img_url}")
            try:
                # Check if image is accessible
                res = requests.head(img_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                print(f"    Image Status: {res.status_code}")
                if res.status_code != 200:
                    print(f"    WARNING: Image URL is not returning 200 OK.")
            except Exception as e:
                print(f"    ERROR checking image: {e}")
        else:
            print("    Image URL: MISSING (None)")

if __name__ == "__main__":
    diag_images()
