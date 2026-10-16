"""Shared HTTP path for both tools.

Standard library only — the plugin ships no dependency beyond the Dify SDK, so
there is nothing to pin and nothing that can drift out from under a workflow.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
import uuid

BASE = "https://veida.ai"

# Read out of the running service on 2026-10-16. A signed-out caller is granted
# 4 credits, and one run on Veida AI Image v1 costs 4 whether it draws from a
# prompt or edits a photo, so the grant is ONE run per caller. A fresh caller id
# per call keeps a loop from stopping after the first image; a ceiling of 30
# credits per IP per day (about 7 runs) sits on top.
ANON_GRANT = 4
COST_PER_RUN = 4
IP_DAILY_CEILING = 30
MODEL = "veida-image-v1"


class VeidaError(RuntimeError):
    pass


def _headers(anon: str) -> dict:
    return {
        "Content-Type": "application/json",
        "x-anon-id": anon,
        "User-Agent": "veida-dify-plugin/0.0.1",
    }


def run(prompt: str, aspect_ratio: str = "1:1", image_url: str | None = None,
        timeout: float = 240.0) -> str:
    """Submit one job, poll it, return the CDN url of the finished image."""
    anon = f"dify-{uuid.uuid4()}"
    options: dict = {"aspect_ratio": aspect_ratio}
    if image_url:
        options["image_input"] = [image_url]
    payload = {
        "provider": "kie",
        "mediaType": "image",
        "model": MODEL,
        "scene": "image-to-image" if image_url else "text-to-image",
        "prompt": prompt,
        "options": options,
    }

    req = urllib.request.Request(
        BASE + "/api/ai/generate",
        data=json.dumps(payload).encode(),
        headers=_headers(anon),
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            submitted = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise VeidaError(f"submit failed with HTTP {e.code}") from e

    data = submitted.get("data") or {}
    # The quota wall answers HTTP 200, not an error. Without this branch it
    # surfaces as the misleading "no task id".
    if data.get("wall"):
        if data.get("reason") == "ip_daily":
            raise VeidaError(
                f"the per-IP daily ceiling ({IP_DAILY_CEILING} credits, about 7 runs) "
                "is spent; try tomorrow or sign in at https://veida.ai/pricing"
            )
        raise VeidaError(
            "the free allowance for this caller is spent; sign in at https://veida.ai/pricing"
        )
    if submitted.get("code") not in (0, None):
        raise VeidaError(str(submitted.get("message") or "request refused"))

    task_id = data.get("id")
    if not task_id:
        raise VeidaError("the API returned no task id")

    deadline = time.monotonic() + timeout
    query = f"{BASE}/api/ai/anon-query?taskId={task_id}&provider=kie&mediaType=image"
    while time.monotonic() < deadline:
        time.sleep(4)
        with urllib.request.urlopen(
            urllib.request.Request(query, headers=_headers(anon)), timeout=60
        ) as r:
            polled = json.loads(r.read()).get("data") or {}
        images = polled.get("images") or []
        if images:
            return images[0]
        # Status is not monotonic (pending and processing alternate), so only a
        # terminal failure ends the loop early.
        if str(polled.get("status") or "").lower() in {"failed", "error"}:
            raise VeidaError(
                "the prompt was refused by the content filter; rewrite it "
                "rather than retrying the same text"
            )
    raise VeidaError(f"still queued after {timeout:g}s")
