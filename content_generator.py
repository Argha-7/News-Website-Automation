import os
import logging
from groq import Groq
import json
import requests
import re
import urllib.parse
from datetime import datetime


from bs4 import BeautifulSoup

def scrape_body_text(url):
    """
    Scrapes the main body text from a webpage to understand competitor content.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200: return ""
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Simple extraction: all paragraph text
        paragraphs = soup.find_all('p')
        text = " ".join([p.get_text() for p in paragraphs])
        
        # Limit to 3000 chars to avoid token overflow
        return text[:3000]
    except Exception as e:
        logging.error(f"Error scraping body: {e}")
        return ""

def analyze_keywords(topic, context_text=""):
    """
    Analyzes the topic AND competitor content using Groq to find high-potential SEO keywords.
    """
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key: return ""
    
    try:
        client = Groq(api_key=api_key)
        
        if context_text:
             prompt = f"Analyze this high-ranking article content about '{topic}':\\n\\n{context_text[:1000]}...\\n\\nExtract the Top 5 SEO keywords that are driving traffic to this article. Return ONLY the comma-separated list."
        else:
             prompt = f"Analyze the topic '{topic}'. Return top 5 SEO keywords with high search volume and low competition for a news blog. Return ONLY the comma-separated list of keywords, nothing else."
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=60,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error analyzing keywords: {e}")
        return ""

def get_youtube_video(query):
    """
    Searches YouTube for a relevant video (trailer/news clip) and returns the embed code.
    Uses direct requests + regex to avoid broken libraries.
    """
    try:
        # Prepare search URL
        query = query.replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={query}"
        
        # Headers to mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Failed to fetch YouTube page: {response.status_code}")
            return ""
            
        # Regex to find video IDs
        # Look for "videoId":"..." pattern
        video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)
        
        if video_ids:
            # Filter out duplicates and find valid ID
            unique_ids = []
            for vid in video_ids:
                if vid not in unique_ids:
                    unique_ids.append(vid)
            
            if unique_ids:
                video_id = unique_ids[0]
                embed_code = f'<div class="video-container" style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; max-width:100%; margin-top:30px; margin-bottom:20px;"><iframe src="https://www.youtube.com/embed/{video_id}" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allowfullscreen></iframe></div>'
                return embed_code
                
        logging.warning("No video ID found in YouTube search results.")
        return ""

    except Exception as e:
        logging.error(f"Error fetching YouTube video: {e}")
    return ""

def generate_blog_post(article_title, article_description, article_url, article_image_url=None):
    """
    Generates a blog post using Groq API (Llama-3) and adds a YouTube video.
    """
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        logging.error("GROQ_API_KEY environment variable not found.")
        return None

    client = Groq(api_key=api_key)

    # SEO COMPETITOR ANALYSIS
    competitor_text = scrape_body_text(article_url)
    seo_keywords = analyze_keywords(article_title, competitor_text)
    
    logging.info(f"Targeting Keywords (Based on Competitor): {seo_keywords}")
    
    # Save to SEO Log
    try:
        log_entry = {'date': str(datetime.now()), 'title': article_title, 'keywords': seo_keywords}
        with open('seo_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + "\\n")
    except: pass

    prompt = f"""
    You are an expert news reporter and SEO specialist. 
    Rewrite the following news article into a unique, engaging, and professional blog post.
    
    Source Article:
    Title: {article_title}
    Original URL: {article_url}
    
    Requirements:
    1. **Tone**: Professional yet engaging.
    2. **SEO Optimization**: 
       - MUST include these specific keywords naturally in the content: {seo_keywords}
       - Use the primary keyword in the H1 Title.
       - Use variations in H2 subheaders.
    3. **Structure**: 
       - Catchy SEO Title (English).
       - Engaging Intro (English).
       - Detailed Body (English).
       - Key Takeaways (English).
       - Conclusion (English).
       - "User Feedback" question (English).
    3. **Multi-Language Support**:
       - Provide a concise summary of the same news in **Hindi** (under a section called 'Hindi News').
       - Provide a concise summary of the same news in **Bengali** (under a section called 'Bengali News').
    4. **Output Format**: Valid JSON with keys: 
       - "title": SEO Title.
       - "content": Full English Blog Post (HTML).
       - "content_hindi": Full Hindi Summary (HTML).
       - "content_bengali": Full Bengali Summary (HTML).
       - "labels": Comma-separated tags.
    
    IMPORTANT: Return ONLY the raw JSON string. Do NOT use markdown code blocks.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that outputs strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000, # Increased for multi-language
            top_p=1,
            stream=False,
            stop=None,
        )

        text_response = completion.choices[0].message.content
        text_response = text_response.replace('```json', '').replace('```', '').strip()
        
        content_data = json.loads(text_response)
        
        # 1. Add YouTube Video at Top (Replaced Position)
        video_query = f"{article_title} trailer news"
        video_embed = get_youtube_video(video_query)
        if video_embed:
            content_data['content'] = f"<h3>Watch Related Video</h3>{video_embed}" + content_data['content']

        # 2. Add Image at Bottom (Replaced Position)
        if not article_image_url:
            # Fallback to AI generated image if no image found
            # Create a rich prompt for realistic news photography
            clean_title = article_title[:80].replace("'", "").replace('"', '')
            prompt = f"editorial news photography of {clean_title}, realistic, 4k, journalism style, highly detailed, dramatic lighting"
            safe_prompt = urllib.parse.quote(prompt)
            article_image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true&model=flux"
            
        img_tag = f'<img src="{article_image_url}" style="width:100%; border-radius:10px; margin-bottom:20px;">' # Move to TOP
        content_data['content'] = img_tag + content_data['content'] # Prepend

        # 3. Append Hindi & Bengali Content
        if 'content_hindi' in content_data and content_data['content_hindi']:
            content_data['content'] += f'<hr style="margin:40px 0;"><h2>🇮🇳 हिंदी में पढ़ें (News in Hindi)</h2>{content_data["content_hindi"]}'
            
        if 'content_bengali' in content_data and content_data['content_bengali']:
            content_data['content'] += f'<hr style="margin:40px 0;"><h2>🇧🇩 বাংলায় পড়ুন (News in Bengali)</h2>{content_data["content_bengali"]}'
            
        return content_data

    except Exception as e:
        logging.error(f"Error generating content with Groq: {e}")
        return None
