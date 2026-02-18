import requests
import feedparser

def debug_redirect():
    # Fetch a fresh link
    rss_url = "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print("No entries found.")
        return

    test_link = feed.entries[0].link
    print(f"Original Link: {test_link}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(test_link, headers=headers, timeout=10, allow_redirects=True)
        print(f"Final URL: {response.url}")
        print(f"Status Code: {response.status_code}")
        print(f"History: {[r.url for r in response.history]}")
        
        if "google.com" in response.url:
            print("WARNING: Still on Google domain. Redirection might have failed.")
        else:
            print("SUCCESS: Redirected to publisher domain.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_redirect()
