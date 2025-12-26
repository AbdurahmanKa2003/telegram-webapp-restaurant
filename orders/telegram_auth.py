import hmac, hashlib
from urllib.parse import parse_qsl
from django.conf import settings

def verify_init_data(init_data: str, bot_token: str) -> dict:
    if not init_data:
        if settings.DEBUG:
            return {}
        raise ValueError("init_data is empty")

    data = dict(parse_qsl(init_data, keep_blank_values=True))
    if "hash" not in data:
        if settings.DEBUG:
            return data
        raise ValueError("hash is missing")

    received_hash = data.pop("hash")
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if calculated_hash != received_hash:
        if settings.DEBUG:
            return data
        raise ValueError("init_data hash is invalid")

    return data