import content_generator
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

def test_competitor_spy():
    # A sample tech article URL (using a stable one if possible, or just a generic one)
    # Let's use a known tech site like TechCrunch or The Verge, or even a Google Blog
    test_url = "https://techcrunch.com/2024/01/01/example-tech-news" # Fake URL, scraper might fail if 404
    # Better to use a real one, but links die. 
    # Let's try to just test the logic with a mocked response if we can't guarantee a live URL.
    # OR, use a very stable URL like python.org
    test_url = "https://www.python.org/" 
    topic = "Python Programming Language"
    
    print(f"Testing Competitor Spy on: {test_url}")
    
    # 1. Test Scraping
    text = content_generator.scrape_body_text(test_url)
    print(f"Scraped Text Length: {len(text)}")
    if len(text) > 100:
        print(f"Scraped Text Preview: {text[:100]}...")
    else:
        print("WARNING: Scraping returned little or no text. (Might be anti-bot or simple page)")
    
    # 2. Test Analysis
    if text:
        keywords = content_generator.analyze_keywords(topic, text)
        print(f"Extracted Competitor Keywords: {keywords}")
    else:
        print("Skipping keyword analysis due to empty scrape.")

if __name__ == "__main__":
    test_competitor_spy()
