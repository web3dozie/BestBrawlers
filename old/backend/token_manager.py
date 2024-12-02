import base64
import json
import os
import requests
from datetime import datetime, timezone


class TokenManager:
    def __init__(self, cache_file='.token_cache.json'):
        self.cache_file = cache_file

    def decode_jwt(self, token):
        """Decode JWT payload without verification"""
        try:
            payload = token.split('.')[1]
            # Add padding if needed
            payload += '=' * (4 - len(payload) % 4)
            decoded = base64.b64decode(payload)
            return json.loads(decoded)
        except Exception:
            return None

    def is_token_valid(self, token):
        """Check if token is valid and not expired"""
        payload = self.decode_jwt(token)
        if not payload or 'exp' not in payload:
            return False
        expiry = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
        return datetime.now(timezone.utc) < expiry

    def save_token(self, token):
        """Save token with expiry to cache file"""
        payload = self.decode_jwt(token)
        if payload and 'exp' in payload:
            cache_data = {
                'token': token,
                'expiry': payload['exp']
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)

    def load_cached_token(self):
        """Load and validate cached token if available"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    token = cache_data['token']
                    if self.is_token_valid(token):
                        return token
        except Exception:
            pass
        return None

    def get_auth_token(self):
        """Fetch authentication token from brawltime.ninja"""
        auth_url = "https://brawltime.ninja/api/auth.getToken"
        headers = {
            'authority': 'brawltime.ninja',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9,ja;q=0.8,eo;q=0.7',
            'baggage': 'sentry-environment=production,sentry-release=brawltimeninja%40ae7c7ece0dda622a09ed36d59543b399101bf6b5,sentry-public_key=8f9daacd6ab7467788de9869803c41e8,sentry-trace_id=8e2752a3d58b4a3f97bd62b5a0a4ac7b,sentry-sample_rate=0.01,sentry-transaction=tier-list-mode-mode,sentry-sampled=false',
            'content-type': 'application/json',
            'origin': 'https://brawltime.ninja',
            'priority': 'u=1, i',
            'referer': 'https://brawltime.ninja/tier-list/mode/brawl-ball',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sentry-trace': '8e2752a3d58b4a3f97bd62b5a0a4ac7b-bb060a58120630f0-0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        try:
            response = requests.post(auth_url, headers=headers)
            response.raise_for_status()
            return response.json()['result']['data']['json']
        except requests.exceptions.RequestException as e:
            print(f"Failed to get auth token: {e}")
            return None

    def get_token(self):
        """Get valid token, using cache if possible"""
        token = self.load_cached_token()
        if token:
            return token

        token = self.get_auth_token()
        if token:
            self.save_token(token)
        return token