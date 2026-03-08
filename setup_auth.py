import os
import json
import logging

def setup_token():
    """
    Reconstructs token.json from environment variables for CI/CD.
    """
    refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")
    client_id = os.environ.get("BLOGGER_CLIENT_ID")
    client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
    
    if not all([refresh_token, client_id, client_secret]):
        print("CRITICAL: Missing required Blogger OAuth secrets in environment.")
        return False

    token_data = {
        "token": None, # Will be filled by refresh
        "refresh_token": refresh_token,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": ["https://www.googleapis.com/auth/blogger"],
        "universe_domain": "googleapis.com",
        "account": ""
    }
    
    try:
        with open('token.json', 'w') as f:
            json.dump(token_data, f, indent=4)
        print("token.json successfully created from environment variables.")
        return True
    except Exception as e:
        print(f"Error creating token.json: {e}")
        return False

if __name__ == "__main__":
    setup_token()
