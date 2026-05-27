import hashlib
import secrets


def generate_api_key():

    random_string = secrets.token_urlsafe(32)

    return f"sk_live_{random_string}"


def hash_api_key(api_key: str):

    return hashlib.sha256(
        api_key.encode()
    ).hexdigest()