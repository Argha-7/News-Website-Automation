import requests
import os
from dotenv import load_dotenv

load_dotenv()

user_token = "EAALip7CxUHsBQ2yf4Rdmtu3uh6rfaLpiDT078z5AxIrftyYgsH5Du0yXChZAhJZAXdkyc6KJttFrgjbNf5yVLuXh2cUoFWTWnv7ucHUMnPmBqpeDdul75IiMOKdeX0iqYrgCJBbucrmSaIIqCo19SA02RrVqsqHQgpRx08YT8QZCSf7ieKWUeqSLQxZCaXiUq2IXPdsvDKQRIvpnHCY2Adc6BAlQwc9J37Y1EJXyOWu7YeSqq1L7qs3c1kW3ZBg1PRYch7b4RAq2D6mQZD"
page_id = "342919928915666"

url = f"https://graph.facebook.com/v20.0/{page_id}?fields=access_token&access_token={user_token}"
res = requests.get(url)

if res.status_code == 200:
    page_access_token = res.json().get('access_token')
    
    env_path = '.env'
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.startswith('FB_PAGE_ACCESS_TOKEN='):
            new_lines.append(f'FB_PAGE_ACCESS_TOKEN={page_access_token}\n')
        elif line.startswith('FB_PAGE_ID='):
            new_lines.append(f'FB_PAGE_ID={page_id}\n')
        else:
            new_lines.append(line)
            
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    print("SUCCESS")
else:
    print("FAILED")
