import feedparser
import urllib.parse
import logging
import dateparser
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from googlenewsdecoder import new_decoderv1

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_og_image(url):
    """
    Fetches the Open Graph image from a URL, ensuring it meets minimum size requirements.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Helper to check size
            def is_large_enough(soup, property):
                try:
                    width_tag = soup.find("meta", property=f"{property}:width")
                    if width_tag and width_tag.get("content"):
                        return int(width_tag["content"]) >= 600
                except:
                    pass
                return True # If no width specified, assume it's okay (risk of blur, but better than nothing?)
                # Actually, if blurry is the main complaint, maybe we should be strict?
                # But strictness might mean NO images for many sites.
                # Let's trust og:image unless width says it's small.
            
            # 1. Try OG Image
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                # Check width if available
                width_tag = soup.find("meta", property="og:image:width")
                is_small = False
                if width_tag and width_tag.get("content"):
                    try:
                        if int(width_tag["content"]) < 500: # 500px threshold
                            is_small = True
                    except: pass
                
                if not is_small:
                    return og_image["content"]
            
            # 2. Fallback: Twitter image (often high res)
            twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
            if twitter_image and twitter_image.get("content"):
                return twitter_image["content"]
                
    except Exception as e:
        pass
    return None

def fetch_trending_news(query=None, category=None, country='IN', skip_heavy_ops=True):
    """
    Fetches trending news from Google News RSS.
    If skip_heavy_ops is True, it returns raw entry data without decoding or scraping images.
    """
    base_url = "https://news.google.com/rss"
    
    # Construct RSS URL
    if query:
        encoded_query = urllib.parse.quote(query)
        rss_url = f"{base_url}/search?q={encoded_query}&hl=en-{country}&gl={country}&ceid={country}:en"
    elif category:
        category_upper = category.upper()
        if category_upper in ['TECHNOLOGY', 'BUSINESS', 'SCIENCE', 'HEALTH', 'SPORTS', 'ENTERTAINMENT', 'WORLD', 'NATION']:
             rss_url = f"{base_url}/headlines/section/topic/{category_upper}?hl=en-{country}&gl={country}&ceid={country}:en"
        elif category_upper == 'GENERAL':
             rss_url = f"{base_url}?hl=en-{country}&gl={country}&ceid={country}:en"
        else:
             rss_url = f"{base_url}/search?q={category}&hl=en-{country}&gl={country}&ceid={country}:en"
    else:
        rss_url = f"{base_url}?hl=en-{country}&gl={country}&ceid={country}:en"

    logging.info(f"Fetching RSS feed from: {rss_url}")
    
    try:
        feed = feedparser.parse(rss_url)
        
        articles = []
        # Limit to 30 to fetch efficiently
        for entry in feed.entries[:30]: 
            published_date = entry.published if 'published' in entry else str(datetime.now())
            
            original_url = entry.link
            image_url = None

            # Only do heavy operations if NOT skipped
            if not skip_heavy_ops:
                # 1. Decode URL to get original publisher link
                try:
                    decoded = new_decoderv1(entry.link)
                    if decoded.get("status"):
                        original_url = decoded["decoded_url"]
                except:
                    pass
                
                # 2. Fetch Image from ORIGINAL URL
                try:
                    image_url = get_og_image(original_url)
                except:
                    pass
            
            articles.append({
                'title': entry.title,
                'description': entry.title,
                'url': original_url,
                'source': entry.source.title if 'source' in entry else 'Google News',
                'publishedAt': published_date,
                'urlToImage': image_url,
                'rss_link': entry.link # Keep RSS link for deferred decoding
            })
            
        logging.info(f"Fetched {len(articles)} articles from RSS.")
        return articles

    except Exception as e:
        logging.error(f"Error fetching RSS news: {e}")
        return []

if __name__ == "__main__":
    # Test execution
    news = fetch_trending_news(category='technology', country='IN')
    for n in news[:3]:
        print(f"Title: {n['title']}\nImage: {n['urlToImage']}\n")
