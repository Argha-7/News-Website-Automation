import os
import requests
from requests_oauthlib import OAuth1
import logging

def post_to_x(title, article_url):
    """
    Posts a tweet to X (Twitter) using the requests_oauthlib library.
    """
    try:
        api_key = os.getenv('X_API_KEY')
        api_secret = os.getenv('X_API_SECRET')
        access_token = os.getenv('X_ACCESS_TOKEN')
        access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')

        if not all([api_key, api_secret, access_token, access_token_secret]):
            logging.warning("X (Twitter) API keys are missing. Skipping X post.")
            return False

        # Authenticate with X API v2 using OAuth 1.0a
        auth = OAuth1(api_key, api_secret, access_token, access_token_secret)

        # Create the tweet content
        # Keep it under 280 characters and engaging
        hashtags = "#News #Trending #BreakingNews"
        tweet_text = f"📰 {title}\n\nRead more here: {article_url}\n\n{hashtags}"

        # API endpoint for creating a tweet (v2)
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": tweet_text}

        # Post the tweet
        response = requests.post(url, json=payload, auth=auth)
        
        if response.status_code in (200, 201):
            logging.info(f"Successfully posted to X: {response.json()}")
            return True
        else:
            logging.error(f"Failed to post to X. Status Code: {response.status_code}, Response: {response.text}")
            return False

    except Exception as e:
        logging.error(f"Failed to post to X: {e}")
        return False

def post_to_facebook(title, article_url, image_url=None):
    """
    Posts a link and message to a Facebook Page using the Graph API.
    """
    try:
        page_id = os.getenv('FB_PAGE_ID')
        access_token = os.getenv('FB_PAGE_ACCESS_TOKEN')

        if not all([page_id, access_token]):
            logging.warning("Facebook API keys (Page ID or Access Token) are missing. Skipping Facebook post.")
            return False

        # Facebook Graph API endpoint for publishing feed posts
        url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
        
        message = f"📰 {title}\n\nRead more here: {article_url}\n\n#News #Trending #NewslyViral"
        
        payload = {
            "message": message,
            "link": article_url,
            "access_token": access_token
        }

        # Send POST request
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            logging.info(f"Successfully posted to Facebook: {response.json().get('id')}")
            return True
        else:
            logging.error(f"Failed to post to Facebook. Status Code: {response.status_code}, Response: {response.text}")
            return False

    except Exception as e:
        logging.error(f"Failed to post to Facebook: {e}")
        return False

# For testing locally
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Configure basic logging for the test
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_title = "The Fox Newspaper introduces AI-driven reporting capabilities"
    test_url = "https://ainews.blogspot.com/"
    
    print("Testing Facebook Post...")
    success = post_to_facebook(test_title, test_url)
    if success:
        print("Facebook Test post successful!")
    else:
        print("Facebook Test post failed. Check logs.")
