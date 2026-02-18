import os
import pickle
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

# Configure logging
logging.basicConfig(level=logging.INFO)

# Scopes required for Blogger API
SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_blogger_service():
    """
    Authenticates the user and returns the Blogger API service object.
    Handles the OAuth2 flow and token storage.
    """
    creds = None
    # 1. Try Legacy Pickle Token (Local Dev)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # 2. Try JSON Token (CI/CD Environment)
    elif os.path.exists('token.json'):
         creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secret.json'):
                logging.error("client_secret.json not found. Please download it from Google Cloud Console.")
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run (Local only)
        # Avoid saving pickle in CI if we started with JSON
        if not os.path.exists('token.json'):
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    try:
        service = build('blogger', 'v3', credentials=creds)
        return service
    except Exception as e:
        logging.error(f"Error building Blogger service: {e}")
        return None

def post_to_blogger(blog_id, title, content, labels=None):
    """
    Posts a new article to the specified Blogger blog.
    
    Args:
        blog_id (str): The ID of the Blogger blog.
        title (str): The title of the post.
        content (str): The HTML content of the post.
        labels (list): A list of tags/labels for the post.
        
    Returns:
        dict: The response from the Blogger API containing post details.
    """
    service = get_blogger_service()
    if not service:
        logging.error("Failed to get Blogger service.")
        return None
        
    body = {
        'kind': 'blogger#post',
        'title': title,
        'content': content,
    }
    
    if labels:
        body['labels'] = labels
        
    try:
        posts = service.posts()
        result = posts.insert(blogId=blog_id, body=body).execute()
        logging.info(f"Successfully posted: {result.get('url')}")
        return result
    except Exception as e:
        logging.error(f"Error posting to Blogger: {e}")
        return None

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test execution
    # Ideally, you need a valid BLOG_ID and client_secret.json to run this.
    blog_id = os.getenv('BLOGGER_BLOG_ID')
    if blog_id:
        post_to_blogger(blog_id, "Test Post from Automated Script", "<p>This is a test post.</p>", ["Test", "Automation"])
    else:
        print("Please set BLOGGER_BLOG_ID in .env to test posting.")
