import sys
import requests

def test_facebook_token(token):
    url = f"https://graph.facebook.com/v20.0/me?access_token={token}&fields=id,name"
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            data = response.json()
            print(f"Page Name: {data.get('name')}")
            print(f"Page ID: {data.get('id')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_facebook_token("EAALip7CxUHsBQ20XlpRpIn63K1FA4BvwgZB2vECRMNS9UI2gIbXykY3g7VYpfoAI7ZCGArZCMRLRFYEgdi5Kahgn0qyDYOAsNu0fLwfuvvSEoR3vwPOKjvzrfNcvymQfEtNlVjJfYiyaNslR5uhQf5bNJStE44YL9QUXqihfdjPa1gWmk11OaLK3vakUdqmvPNVZCZAqHSZAnqpSTfRvG1OkqHrBLRXh9WnfYZCTlH9FixKMSppXzl9MZAdszZBnNTimVWted32vhOZCfNUsuLy52LwsvY")
