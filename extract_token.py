import pickle
import os
import json

try:
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
        print(f"REFRESH_TOKEN={creds.refresh_token}")
        print(f"CLIENT_ID={creds.client_id}")
        print(f"CLIENT_SECRET={creds.client_secret}")
    else:
        print("token.pickle not found.")
except Exception as e:
    print(f"Error: {e}")
