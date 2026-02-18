import pickle
import os
import json

try:
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
        with open('refresh_token.txt', 'w') as f:
            f.write(creds.refresh_token)
            
        print("REFRESH_TOKEN saved to refresh_token.txt")
    else:
        print("token.pickle not found.")
except Exception as e:
    print(f"Error: {e}")
