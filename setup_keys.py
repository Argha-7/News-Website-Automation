
import os

print("--- AI News Bot Setup ---")
print("We need to set up your API keys.")
print("You can copy-paste them when asked (Right-click to paste in CMD).")
print("-" * 30)

news_api_key = input("Enter your NewsAPI Key (from newsapi.org): ").strip()
groq_api_key = input("Enter your Groq API Key (from console.groq.com): ").strip()
blog_id = input("Enter your Blogger Blog ID (digits only): ").strip()

content = f"""NEWS_API_KEY={news_api_key}
GROQ_API_KEY={groq_api_key}
BLOGGER_BLOG_ID={blog_id}
"""

with open('.env', 'w') as f:
    f.write(content)

print("-" * 30)
print("✅ Configuration Saved to .env file!")
print("You can now run 'run.bat' again.")
print("Press Enter to exit...")
input()
