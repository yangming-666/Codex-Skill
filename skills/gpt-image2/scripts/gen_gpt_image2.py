import argparse
import base64
import json
import os
import time
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError


RETRYABLE_HTTP_CODES = {408, 409, 429, 500, 502, 503, 504, 524}


def post_json(url: str, headers: dict, payload: dict, retries: int = 3, retry_delay: float = 8.0) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last_error = None

    for attempt in range(1, retries + 1):
        req = request.Request(url, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"HTTP {e.code}: {detail}")
            if e.code in RETRYABLE_HTTP_CODES and attempt < retries:
                print(f"retrying_after_http={e.code} attempt={attempt}/{retries}")
                time.sleep(retry_delay)
                continue
            raise last_error from e
        except URLError as e:
            last_error = RuntimeError(f"Request failed: {e}")
            if attempt < retries:
                print(f"retrying_after_network_error attempt={attempt}/{retries}")
                time.sleep(retry_delay)
                continue
            raise last_error from e

    if last_error:
        raise last_error
    raise RuntimeError("Request failed for unknown reason")


def download_file(url: str) -> bytes:
    with request.urlopen(url, timeout=180) as resp:
        return resp.read()


def main():
    parser = argparse.ArgumentParser(description="Generate an image with gpt-image-2 via OpenAI-compatible API.")
    parser.add_argument("prompt", help="Image prompt, supports Chinese safely.")
    parser.add_argument("--api-key", default=os.environ.get("TOKENX24_API_KEY"), help="API key for the provider. Defaults to TOKENX24_API_KEY environment variable.")
    parser.add_argument("--base-url", default="https://tokenx24.com/v1", help="Provider base URL")
    parser.add_argument("--model", default="gpt-image-2", help="Model id")
    parser.add_argument("--size", default="1024x1024", help="Image size, e.g. 1024x1024")
    parser.add_argument("--out", default="output.png", help="Output PNG path")
    parser.add_argument("--retries", type=int, default=3, help="Total attempts for retryable failures")
    parser.add_argument("--retry-delay", type=float, default=8.0, help="Seconds to wait between retries")
    args = parser.parse_args()

    if not args.api_key:
        raise RuntimeError("Missing API key. Set TOKENX24_API_KEY or pass --api-key.")

    url = args.base_url.rstrip("/") + "/images/generations"
    headers = {
        "Authorization": f"Bearer {args.api_key}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
    }

    data = post_json(url, headers, payload, retries=args.retries, retry_delay=args.retry_delay)
    if not data.get("data"):
        raise RuntimeError(f"No image data returned: {json.dumps(data, ensure_ascii=False)}")

    item = data["data"][0]
    out_path = Path(args.out)

    if item.get("b64_json"):
        out_path.write_bytes(base64.b64decode(item["b64_json"]))
        print(f"saved_png={out_path.resolve()}")
        return

    if item.get("url"):
        out_path.write_bytes(download_file(item["url"]))
        print(f"saved_png={out_path.resolve()}")
        return

    raise RuntimeError(f"Unsupported response format: {json.dumps(data, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
