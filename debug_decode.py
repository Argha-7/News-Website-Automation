from googlenewsdecoder import new_decoderv1
import feedparser

def debug_decoder():
    # Fetch a fresh link
    rss_url = "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print("No entries found.")
        return

    test_link = feed.entries[0].link
    print(f"Original Link: {test_link}")
    
    try:
        decoded_url = new_decoderv1(test_link)
        if decoded_url.get("status"):
            print(f"Decoded URL: {decoded_url['decoded_url']}")
        else:
            print("Failed to decode.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_decoder()
