import os
import json
import logging

def setup_token():
    """
    Reconstructs token.json from environment variables for CI/CD.
    """
    # Use .strip() to remove accidental spaces from copy-pasting
    refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN", "").strip()
    client_id = os.environ.get("BLOGGER_CLIENT_ID", "").strip()
    client_secret = os.environ.get("BLOGGER_CLIENT_SECRET", "").strip()
    
    if not all([refresh_token, client_id, client_secret]):
        print("CRITICAL: Missing required Blogger OAuth secrets in environment.")
        print(f"DEBUG: Refresh Token Length: {len(refresh_token)}")
        print(f"DEBUG: Client ID Length: {len(client_id)}")
        print(f"DEBUG: Client Secret Length: {len(client_secret)}")
        return False

    print(f"DEBUG: Using Client ID starting with: {client_id[:10]}...")

    token_data = {
        "token": "", # Will be refreshed on first use
        "refresh_token": refresh_token,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": ["https://www.googleapis.com/auth/blogger"],
        "expiry": "2020-01-01T00:00:00Z" # Force refresh
    }
    
    try:
        with open('token.json', 'w') as f:
            json.dump(token_data, f, indent=4)
        print("SUCCESS: token.json created for GitHub Actions.")
        return True
    except Exception as e:
        print(f"ERROR creating token.json: {e}")
        return False

if __name__ == "__main__":
    setup_token()
