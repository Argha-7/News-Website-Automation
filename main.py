import os
import json
import time
import logging
from dotenv import load_dotenv
from news_fetcher_rss import fetch_trending_news
from content_generator import generate_blog_post
from blogger_poster import post_to_blogger
import firebase_db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

POSTED_ARTICLES_FILE = 'posted_articles.json'

def load_posted_articles():
    if os.path.exists(POSTED_ARTICLES_FILE):
        with open(POSTED_ARTICLES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_posted_article(url):
    posted = load_posted_articles()
    posted.append(url)
    with open(POSTED_ARTICLES_FILE, 'w') as f:
        json.dump(posted, f)

def main():
    load_dotenv()
    
    # Configuration
    NEWS_CATEGORY = os.getenv('NEWS_CATEGORY', 'technology')
    NEWS_COUNTRY = os.getenv('NEWS_COUNTRY', 'us')
    BLOG_ID = os.getenv('BLOGGER_BLOG_ID')
    
    if not BLOG_ID:
        logging.error("BLOGGER_BLOG_ID is missing in .env")
        return

    logging.info("Starting automated news posting cycle...")
    
    # Topics to cover in each cycle
    # Format: (query, category, country, label_name)
    # Topics to cover in each cycle
    # Format: (query, category, country, label_name)
    TOPICS = [
        ("West Bengal", None, "in", "Local News"),    # Local (Newest)
        ("technology", None, "in", "Technology"),     # Tech (Newest)
        ("business", None, "in", "Business"),         # Business (Newest)
        ("science", None, "in", "Science"),           # Science (Newest)
        (None, "general", "in", "National News"),     # National (Top)
        (None, "general", "us", "World News")         # International (Top)
    ]
    
    posted_urls = load_posted_articles()
    posts_count = 0
    MAX_POSTS_PER_CYCLE = 2
    
    for query, category, country, label_text in TOPICS:
        if posts_count >= MAX_POSTS_PER_CYCLE:
            break
            
        logging.info(f"Fetching news for: {label_text}")
        articles = fetch_trending_news(query=query, category=category, country=country)
        
        # Take top 2 articles from each topic to balance the feed
        for article in articles[:2]:
            if posts_count >= MAX_POSTS_PER_CYCLE:
                break

            url = article['url']
            
            # Check if already posted
            if url in posted_urls:
                logging.info(f"Skipping duplicate article: {article['title']}")
                continue
                
            logging.info(f"Processing ({label_text}): {article['title']}")
            
            # 2. Generate Content
            generated_content = generate_blog_post(
                article['title'], 
                article['description'], 
                url,
                article.get('urlToImage')
            )
            
            if not generated_content:
                continue
                
            # OPTIONAL: Save to Firebase (if key exists)
            firebase_db.save_article(generated_content)
                
            # 3. Post to Blogger
            # Ensure labels is a list
            labels = generated_content.get('labels', [])
            if isinstance(labels, str):
                labels = [l.strip() for l in labels.split(',')]
                
            # Add specific section label
            labels.append(label_text)
            
            final_content = generated_content['content']
            
            post_result = post_to_blogger(
                BLOG_ID,
                generated_content['title'],
                final_content,
                labels
            )
            
            if post_result:
                logging.info(f"Successfully posted: {generated_content['title']}")
                save_posted_article(url)
                posted_urls.append(url) # Update in-memory list immediately
                posts_count += 1
                
                # Rate limiting to be safe
                logging.info("Waiting 60 seconds before next post...")
                time.sleep(60)
            else:
                logging.error("Failed to post to Blogger.")

    logging.info(f"Cycle completed. Posted {posts_count} articles.")

if __name__ == "__main__":
    daily_requests = 0
    
    while True:
        # Check daily limit (NewsAPI Developer Plan usually 100 or 1000/day)
        if daily_requests >= 950:
            logging.warning("Daily request limit reached (950). Stopping to prevent overage.")
            # Sleep for 24 hours or until manually restarted
            time.sleep(86400) 
            daily_requests = 0 
            
        try:
            main()
            # Each 'main()' call makes len(TOPICS) API requests. Currently 6 topics.
            daily_requests += 6 
        except Exception as e:
            logging.error(f"Critical Error in main loop: {e}")
        
        logging.info("Cycle finished. Sleeping for 5 minutes (Balanced Mode) to fit daily quota...")
        time.sleep(300) # 5 minutes sleep (Approx 14 hours runtime/day)
