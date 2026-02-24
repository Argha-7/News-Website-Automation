import requests
import os
from dotenv import load_dotenv

load_dotenv()

# The token the user just gave us (User Token with Page permissions)
user_token = "EAALip7CxUHsBQ2yf4Rdmtu3uh6rfaLpiDT078z5AxIrftyYgsH5Du0yXChZAhJZAXdkyc6KJttFrgjbNf5yVLuXh2cUoFWTWnv7ucHUMnPmBqpeDdul75IiMOKdeX0iqYrgCJBbucrmSaIIqCo19SA02RrVqsqHQgpRx08YT8QZCSf7ieKWUeqSLQxZCaXiUq2IXPdsvDKQRIvpnHCY2Adc6BAlQwc9J37Y1EJXyOWu7YeSqq1L7qs3c1kW3ZBg1PRYch7b4RAq2D6mQZD"
page_id = "342919928915666"

# Exchange User Token for Page Token
url = f"https://graph.facebook.com/v20.0/{page_id}?fields=access_token&access_token={user_token}"
res = requests.get(url)

print(f"Status: {res.status_code}")
print(f"Response: {res.text}")

if res.status_code == 200:
    page_access_token = res.json().get('access_token')
    print("\n--- NEW PAGE TOKEN ---")
    print(page_access_token)
    
    # Test posting with it
    post_url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
    payload = {
        "message": "📰 Automation Test: This is a news update from our AI system! \n\n#NewslyViral #AI",
        "link": "https://ainews.blogspot.com/",
        "access_token": page_access_token
    }
    post_res = requests.post(post_url, data=payload)
    print(f"\nPost Status: {post_res.status_code}")
    print(f"Post Response: {post_res.text}")
