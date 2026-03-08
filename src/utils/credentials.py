import json
import uuid
import secrets
import base64


def _b64encode_json(obj: dict) -> str:
    return base64.b64encode(json.dumps(obj).encode()).decode()


def create_credential(user_id: int) -> str:
    """Create a fake JWT-like credential string for a user."""
    header = _b64encode_json({"typ": "JWT", "alg": "HS256"})
    payload = _b64encode_json({"credential": str(uuid.uuid4()), "userId": str(user_id)})
    signature = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
    return f"{header}.{payload}.{signature}"


def create_signature(user_id: int) -> str:
    """Create a fake JWT-like signature string for a user."""
    header = _b64encode_json({"typ": "JWT", "alg": "HS256"})
    payload = _b64encode_json({"userId": str(user_id)})
    signature = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
    return f"{header}.{payload}.{signature}"
