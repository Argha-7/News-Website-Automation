import os
import requests
from dotenv import load_dotenv

load_dotenv()
page_id = os.getenv('FB_PAGE_ID')
# This is the USER token you provided
user_token = "EAALip7CxUHsBQzO2YDwYsPTOy9AEN38r2UmR7fccR4nLUksuX5tN89E5zvjVLKRh4lpnsG9qdE8HTjX3Xa08xYU2ZBn0Gqwn5738PAP2bWcDrRZBs1d9YjrMvhnK1oWz0hKdq1OlkLYG60mG4nST791jud11VltihmYbKHMk6qefe8wJBacJ5TjvxDGhSriP3PNrYb52Lxj7WHTviYVmHY4EVhjYyo02q9jamLZC8yESK3ibepDaGgPH5LG3YFQW7VVlk47WdcBNUSs4TBkZBDDE"

# Step 1: Use User Token to fetch the Page Access Token
url = f"https://graph.facebook.com/v20.0/{page_id}?fields=access_token&access_token={user_token}"
response = requests.get(url)

print("--- FETCHING PAGE TOKEN ---")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    page_token = response.json().get('access_token')
    print(f"\nSUCCESS! Here is your real PAGE ACCESS TOKEN:\n\n{page_token}\n")
    
    # Step 2: Let's test it immediately!
    print("--- TESTING POST WITH PAGE TOKEN ---")
    post_url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
    payload = {
        "message": "📰 The Fox Newspaper introduces AI-driven reporting capabilities\n\nRead more here: https://ainews.blogspot.com/\n\n#News #Trending #NewslyViral",
        "link": "https://ainews.blogspot.com/",
        "access_token": page_token
    }
    post_res = requests.post(post_url, data=payload)
    print(f"Post Status: {post_res.status_code}")
    print(f"Post Response: {post_res.text}")
    print("\nIf you see a Post ID above, the code is PERFECT. Please copy the Page Token shown above and save it.")
else:
    print(f"Response: {response.text}")
