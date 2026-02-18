import os
import json

def setup_token():
    """
    Reconstructs token.json from environment variables for CI/CD.
    """
    token_data = {
        "token": os.environ.get("BLOGGER_ACCESS_TOKEN"),
        "refresh_token": os.environ.get("BLOGGER_REFRESH_TOKEN"),
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": os.environ.get("BLOGGER_CLIENT_ID"),
        "client_secret": os.environ.get("BLOGGER_CLIENT_SECRET"),
        "scopes": ["https://www.googleapis.com/auth/blogger"],
        "expiry": "2024-01-01T00:00:00.000000Z" # Dummy expiry to force refresh
    }
    
    with open('token.json', 'w') as f:
        json.dump(token_data, f)
        
    print("token.json created from secrets.")

if __name__ == "__main__":
    setup_token()
