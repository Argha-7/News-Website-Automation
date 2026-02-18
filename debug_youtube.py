import requests
import re
import json

def get_youtube_video_id(query):
    """
    Searches YouTube for a video ID using requests and regex.
    This avoids the broken youtube-search-python library.
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
            print(f"Failed to fetch YouTube page: {response.status_code}")
            return None
            
        # Regex to find video IDs
        # Look for "videoId":"..." pattern
        video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)
        
        if video_ids:
            # Filter out duplicates and return the first valid one
            # (sometimes the first one is an ad or playlist, but usually okay)
            unique_ids = []
            for vid in video_ids:
                if vid not in unique_ids:
                    unique_ids.append(vid)
            
            if unique_ids:
                return unique_ids[0]
                
        return None

    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return None

def test_youtube(query):
    print(f"Searching for: {query}")
    vid = get_youtube_video_id(query)
    if vid:
        print(f"Found Video ID: {vid}")
        print(f"Embed: https://www.youtube.com/embed/{vid}")
    else:
        print("No video found.")

if __name__ == "__main__":
    test_youtube("West Bengal News trailer")
    test_youtube("Technology news trailer")
