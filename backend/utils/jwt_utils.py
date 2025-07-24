import jwt
import os
from datetime import datetime, timedelta

KEY_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'keys')
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, 'private.pem')
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, 'public.pem')

with open(PRIVATE_KEY_PATH, 'rb') as f:
    PRIVATE_KEY = f.read()
with open(PUBLIC_KEY_PATH, 'rb') as f:
    PUBLIC_KEY = f.read()

def issue_token(payload):
    payload['iss'] = 'AltID'
    payload['iat'] = int(datetime.utcnow().timestamp())
    payload['exp'] = int((datetime.utcnow() + timedelta(minutes=15)).timestamp())
    return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')

def verify_token(token):
    try:
        return jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'], issuer='AltID')
    except Exception as e:
        print(f"JWT verification error: {e}")
        return None 