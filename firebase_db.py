import firebase_admin
from firebase_admin import credentials, firestore
import logging
import os
from datetime import datetime

# Global flag to track if Firebase is initialized
_firebase_initialized = False

def init_db():
    """
    Initializes the Firebase connection using saved credentials.
    Returns the Firestore client or None if initialization fails.
    """
    global _firebase_initialized
    
    # Path to the key file the user needs to download
    key_path = "serviceAccountKey.json"
    
    if not os.path.exists(key_path):
        logging.warning(f"Firebase Key not found at {key_path}. Database saving skipped.")
        return None
        
    try:
        if not _firebase_initialized:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
            _firebase_initialized = True
            logging.info("Firebase initialized successfully.")
            
        return firestore.client()
    except Exception as e:
        logging.error(f"Failed to initialize Firebase: {e}")
        return None

def normalize_url(url):
    """
    Strips tracking parameters and trailing slashes for consistent comparison.
    """
    if not url: return ""
    try:
        # Strip query params
        clean_url = url.split('?')[0]
        # Strip trailing slash
        clean_url = clean_url.rstrip('/')
        return clean_url.lower()
    except:
        return url.lower()

def save_article(article_data):
    """
    Saves an article dictionary to the 'articles' collection in Firestore.
    """
    db = init_db()
    if not db:
        return # Skip if DB not available
        
    try:
        title = article_data.get('title', 'Untitled')
        url = article_data.get('url', '')
        
        # Prepare data record
        record = {
            'title': title,
            'title_lower': title.lower(), # For faster case-insensitive search
            'content': article_data.get('content', ''),
            'url': url, 
            'url_normalized': normalize_url(url),
            'image_url': article_data.get('image_url', ''), 
            'created_at': datetime.now(),
            'keywords': article_data.get('keywords', []),
            'language': 'en'
        }
        
        # Add to collection
        db.collection('articles').add(record)
        logging.info(f"Article '{title}' saved to Firebase.")
        
    except Exception as e:
        logging.error(f"Error saving to Firebase: {e}")

def is_article_posted(url, title=None):
    """
    Checks if an article with the given URL or Title exists in the Firebase database.
    """
    db = init_db()
    if not db:
        return False # Fallback to local if DB fails
        
    try:
        from google.cloud.firestore_v1.base_query import FieldFilter
        # 1. Check by Normalized URL
        norm_url = normalize_url(url)
        url_docs = db.collection('articles').where(filter=FieldFilter('url_normalized', '==', norm_url)).limit(1).get()
        if len(url_docs) > 0:
            return True
            
        # 2. Check by Title (Safety Fallback)
        if title:
            title_docs = db.collection('articles').where(filter=FieldFilter('title_lower', '==', title.lower())).limit(1).get()
            if len(title_docs) > 0:
                return True
                
        return False
    except Exception as e:
        logging.error(f"Error checking Firebase for duplicates: {e}")
        return False
