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

def save_article(article_data):
    """
    Saves an article dictionary to the 'articles' collection in Firestore.
    """
    db = init_db()
    if not db:
        return # Skip if DB not available
        
    try:
        # Prepare data record
        record = {
            'title': article_data.get('title', 'Untitled'),
            'content': article_data.get('content', ''),
            'url': article_data.get('url', ''), # Original URL
            'image_url': article_data.get('image_url', ''), # Our generated/fetched image
            'created_at': datetime.now(),
            'keywords': article_data.get('keywords', []),
            'language': 'en'
        }
        
        # Add to collection
        # timestamp as ID is simple, or let auto-ID
        db.collection('articles').add(record)
        logging.info(f"Article '{record['title']}' saved to Firebase.")
        
    except Exception as e:
        logging.error(f"Error saving to Firebase: {e}")
