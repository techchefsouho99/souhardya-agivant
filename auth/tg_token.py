import os
import requests
import config

_TG_TOKEN = None   # module-level cache

def get_tg_token() -> str:
    """
    Returns a cached TigerGraph token.
    Generates it once per process.
    """
    global _TG_TOKEN

    if _TG_TOKEN is not None:
        return _TG_TOKEN

    host = os.getenv("TG_HOST")
    secret = os.getenv("TG_SECRET")

    if not host or not secret:
        raise RuntimeError("TG_HOST and TG_SECRET must be set")

    url = f"{host}/gsql/v1/tokens"

    response = requests.post(
        url,
        json={"secret": secret},
        headers={"Content-Type": "application/json"}
    )

    response.raise_for_status()

    _TG_TOKEN = response.json()["token"]
    return _TG_TOKEN
