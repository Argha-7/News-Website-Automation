import os
import requests
from dotenv import load_dotenv

load_dotenv()

def debug_facebook_post():
    page_id = os.getenv('FB_PAGE_ID')
    access_token = os.getenv('FB_PAGE_ACCESS_TOKEN')
    
    print(f"Page ID: {page_id}")
    print(f"Token (First 10 chars): {access_token[:10]}...")
    
    url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
    
    message = "📰 DEBUG TEST: AI-driven news reporting\n\nRead more here: https://ainews.blogspot.com/\n\n#News #Trending"
    
    payload = {
        "message": message,
        "link": "https://ainews.blogspot.com/",
        "access_token": access_token
    }

    print(f"Sending request to: {url}")
    response = requests.post(url, data=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("SUCCESS!")
    else:
        print("FAILED!")

if __name__ == "__main__":
    debug_facebook_post()
