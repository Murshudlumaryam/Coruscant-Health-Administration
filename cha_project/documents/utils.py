import os
import hashlib
from cryptography.fernet import Fernet
from django.conf import settings

def get_fernet():
    key = settings.ENCRYPTION_KEY
    if key and isinstance(key, str):
        key = key.encode()
    if not key:
        key = Fernet.generate_key()
        settings.ENCRYPTION_KEY = key.decode()
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)

def encrypt_file(file_data: bytes) -> bytes:
    f = get_fernet()
    return f.encrypt(file_data)

def decrypt_file(encrypted_data: bytes) -> bytes:
    f = get_fernet()
    return f.decrypt(encrypted_data)

def compute_checksum(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
