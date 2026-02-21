import json
import base64
import hashlib
import aiohttp
from app.config import CRYPTOMUS_API_KEY, CRYPTOMUS_MERCHANT_ID

API_BASE = "https://api.cryptomus.com/v1"

def _sign(payload: dict) -> str:
    # docs: md5( base64_encode(json(payload)) + api_key ) 2
    dumped = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    b64 = base64.b64encode(dumped.encode("utf-8"))
    raw = b64 + CRYPTOMUS_API_KEY.encode("utf-8")
    return hashlib.md5(raw).hexdigest()

async def create_invoice(amount_usd: float, order_id: str, callback_url: str, success_url: str = "", return_url: str = "") -> dict:
    url = f"{API_BASE}/payment"  # Creating an invoice 3
    payload = {
        "amount": f"{amount_usd:.2f}",
        "currency": "USD",
        "order_id": order_id,
        "url_callback": callback_url,
    }
    if success_url:
        payload["url_success"] = success_url
    if return_url:
        payload["url_return"] = return_url

    headers = {
        "merchant": CRYPTOMUS_MERCHANT_ID,
        "sign": _sign(payload),
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=payload, headers=headers, timeout=30) as r:
            return await r.json()

def verify_webhook(body_bytes: bytes, header_sign: str) -> bool:
    # Webhook signature is checked with same algorithm (docs Webhook) 4
    try:
        data = json.loads(body_bytes.decode("utf-8"))
    except Exception:
        return False
    expected = _sign(data)
    return expected == (header_sign or "")
