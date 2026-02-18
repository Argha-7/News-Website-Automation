import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_trending_news(query=None, category=None, country='in'):
    """
    Fetches trending news articles from NewsAPI based on query or category.
    """
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        logging.error("NEWS_API_KEY environment variable not found.")
        return []

    if query:
        # Search for specific topic (e.g., "West Bengal")
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=90&apiKey={api_key}"
    else:
        # Top headlines by category
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&pageSize=90&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'ok':
            logging.error(f"NewsAPI error: {data.get('message')}")
            return []
        
        articles = []
        for article in data.get('articles', []):
            # Only include articles with valid title and description
            if article.get('title') and article.get('description'):
                articles.append({
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'source': article['source']['name'],
                    'publishedAt': article['publishedAt'],
                    'urlToImage': article.get('urlToImage')
                })
        
        logging.info(f"Fetched {len(articles)} articles for category '{category}'.")
        return articles

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching news: {e}")
        return []

if __name__ == "__main__":
    # Test execution
    from dotenv import load_dotenv
    load_dotenv()
    
    news = fetch_trending_news(category='technology', country='in') # Defaulting to India for testing
    for n in news[:3]:
        print(f"Title: {n['title']}\nURL: {n['url']}\n")
