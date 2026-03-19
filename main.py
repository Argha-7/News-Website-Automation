# Diagnostic Run - Verifying CI/CD Flow
import os
import json
import time
import logging
from dotenv import load_dotenv
from news_fetcher_rss import fetch_trending_news, get_og_image
from googlenewsdecoder import new_decoderv1
from content_generator import generate_blog_post
from blogger_poster import post_to_blogger
from social_poster import post_to_facebook
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
        # Fetch FAST (skip decoding/images)
        articles = fetch_trending_news(query=query, category=category, country=country, skip_heavy_ops=True)
        
        # Take top 2 articles from each topic to balance the feed
        for article in articles[:2]:
            if posts_count >= MAX_POSTS_PER_CYCLE:
                break

            # 1. Deferred Decoding and Image Search
            # We do this BEFORE duplicate check to get the real URL
            rss_link = article.get('rss_link')
            actual_url = article['url']
            title = article['title']

            # Only decode if it's a google news link
            if "news.google.com" in actual_url and rss_link:
                try:
                    decoded = new_decoderv1(rss_link)
                    if decoded.get("status"):
                        actual_url = decoded["decoded_url"]
                except: pass

            # Update article with real URL
            article['url'] = actual_url
            
            # Check if already posted (Local + Firebase + Title check)
            if actual_url in posted_urls or firebase_db.is_article_posted(actual_url, title):
                # logging.debug(f"Skipping duplicate: {title}")
                continue
                
            logging.info(f"Article selected: {title}")
            
            # Now fetch image ONLY for this selected article
            image_url = None
            try:
                image_url = get_og_image(actual_url)
            except: pass
            article['urlToImage'] = image_url

            logging.info(f"Processing ({label_text}): {title}")
            
            # 2. Generate Content
            try:
                generated_content = generate_blog_post(
                    title, 
                    article['description'], 
                    actual_url,
                    image_url
                )
            except Exception as e:
                logging.error(f"Generation failed for {title}: {e}")
                continue
            
            if not generated_content:
                continue
            
            # Add original URL to generated content for Firebase logging
            generated_content['url'] = actual_url
            
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
            
            result = post_to_blogger(
                BLOG_ID,
                generated_content['title'],
                final_content,
                labels
            )
            
            if result:
                post_url = result.get('url')
                logging.info(f"Successfully posted! URL: {post_url}")
                # Save to history
                save_posted_article(actual_url)
                posted_urls.append(actual_url) 
                posts_count += 1
                
                # Cross-post to Facebook
                if post_url:
                    logging.info(f"Attempting to cross-post to Facebook: {title}")
                    try:
                        post_to_facebook(generated_content['title'], post_url)
                    except Exception as fb_err:
                        logging.warning(f"Facebook cross-post failed: {fb_err}")
                
                # Rate limiting
                time.sleep(10)
            else:
                is_gh = os.getenv('GITHUB_ACTIONS') == 'true'
                logging.error(f"Failed to post to Blogger ({'GitHub' if is_gh else 'Local'}). This is likely an authentication or quota issue.")
                if posts_count == 0:
                     if is_gh:
                         logging.error("CRITICAL: GitHub Authentication failed. Check BLOGGER_REFRESH_TOKEN secret.")
                     else:
                         logging.error("CRITICAL: Authentication failed (invalid_grant?). Please regenerate your token using blogger_setup.py.")
                     return # Exit early

    logging.info(f"Cycle completed. Posted {posts_count} articles.")

if __name__ == "__main__":
    # In GitHub Actions mode, we run ONCE and exit.
    try:
        main()
    except Exception as e:
        logging.error(f"Critical Error in main execution: {e}")
