from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

KEY_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'keys')
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, 'private.pem')
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, 'public.pem')

os.makedirs(KEY_DIR, exist_ok=True)

if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    with open(PRIVATE_KEY_PATH, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    public_key = private_key.public_key()
    with open(PUBLIC_KEY_PATH, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print('Keys generated.')
else:
    print('Keys already exist.') 