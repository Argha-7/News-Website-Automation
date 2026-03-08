import os
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import json

# Scopes required for Blogger API
SCOPES = ['https://www.googleapis.com/auth/blogger']

def main():
    print("--- Blogger Authentication Setup ---")
    if not os.path.exists('client_secret.json'):
        print("ERROR: client_secret.json not found in the current directory.")
        print("Please download it from Google Cloud Console and rename it to client_secret.json.")
        return

    # Delete old tokens to ensure a fresh start
    for f in ['token.pickle', 'token.json']:
        if os.path.exists(f):
            os.remove(f)
            print(f"Removed old {f}")

    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the credentials
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    
    # Also save as JSON for easy inspection if needed
    token_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }
    with open('token.json', 'w') as f:
        json.dump(token_data, f, indent=4)

    print("\nSUCCESS! New authentication tokens generated.")
    print("You can now run main.py or your automated schedule.")
    print("\nIMPORTANT: If your token expires every 7 days, go to Google Cloud Console > APIs & Services > OAuth consent screen and set 'Publishing status' to 'Production'.")

if __name__ == "__main__":
    main()
