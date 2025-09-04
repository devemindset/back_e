from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ["http", "https"], parsed.netloc])
    except Exception:
        return False


import random

def generate_verification_code():
    return str(random.randint(100000, 999999))

