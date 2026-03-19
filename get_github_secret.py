import os
import json
import pickle

def get_refresh_token():
    """
    Reads token.pickle or token.json and prints the refresh token and client info.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            print("Found credentials in token.pickle")
    elif os.path.exists('token.json'):
        with open('token.json', 'r') as f:
            data = json.load(f)
            # Handle both raw JSON and Credentials.from_authorized_user_file format
            refresh_token = data.get('refresh_token')
            client_id = data.get('client_id')
            client_secret = data.get('client_secret')
            print("Found credentials in token.json")
    else:
        print("ERROR: No token.pickle or token.json found. Please run blogger_setup.py first.")
        return

    if hasattr(creds, 'refresh_token') or 'refresh_token' in locals():
        rt = getattr(creds, 'refresh_token', None) or refresh_token
        cid = getattr(creds, 'client_id', None) or client_id
        cs = getattr(creds, 'client_secret', None) or client_secret
        
        print("\n" + "="*50)
        print("COPY THESE VALUES TO GITHUB SECRETS")
        print("="*50)
        print(f"\n1. BLOGGER_REFRESH_TOKEN:\n{rt}")
        print(f"\n2. BLOGGER_CLIENT_ID:\n{cid}")
        print(f"\n3. BLOGGER_CLIENT_SECRET:\n{cs}")
        print("\n" + "="*50)
    else:
        print("ERROR: Refresh token not found in the credentials.")

if __name__ == "__main__":
    get_refresh_token()
