import os

env_path = '.env'
new_token = 'EAALip7CxUHsBQ2yf4Rdmtu3uh6rfaLpiDT078z5AxIrftyYgsH5Du0yXChZAhJZAXdkyc6KJttFrgjbNf5yVLuXh2cUoFWTWnv7ucHUMnPmBqpeDdul75IiMOKdeX0iqYrgCJBbucrmSaIIqCo19SA02RrVqsqHQgpRx08YT8QZCSf7ieKWUeqSLQxZCaXiUq2IXPdsvDKQRIvpnHCY2Adc6BAlQwc9J37Y1EJXyOWu7YeSqq1L7qs3c1kW3ZBg1PRYch7b4RAq2D6mQZD'
new_page_id = '342919928915666'

with open(env_path, 'r') as f:
    lines = f.readlines()

new_lines = []
found_token = False
found_id = False

for line in lines:
    if line.startswith('FB_PAGE_ACCESS_TOKEN='):
        new_lines.append(f'FB_PAGE_ACCESS_TOKEN={new_token}\n')
        found_token = True
    elif line.startswith('FB_PAGE_ID='):
        new_lines.append(f'FB_PAGE_ID={new_page_id}\n')
        found_id = True
    else:
        new_lines.append(line)

if not found_token:
    new_lines.append(f'FB_PAGE_ACCESS_TOKEN={new_token}\n')
if not found_id:
    new_lines.append(f'FB_PAGE_ID={new_page_id}\n')

with open(env_path, 'w') as f:
    f.writelines(new_lines)

print("Updated .env successfully")
