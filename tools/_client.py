"""Shared HTTP path for the tool.

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

# Measured against the live site on 2026-09-06. A signed-out caller is granted 4
# credits and one text-to-image run costs exactly 4, so the grant is ONE image
# per caller — hence a fresh anonymous id per call rather than one per session.
#
# Two things are deliberately absent from this plugin, both for the same reason
# (a tool that always fails is worse than a tool that is not there):
#   - editing an existing image: the editor model costs 30 credits, which no
#     anonymous wallet can pay;
#   - video: this site does not serve it at all.
ANON_GRANT = 4
COST_TEXT_TO_IMAGE = 4
IP_DAILY_CEILING = 30


class VeidaError(RuntimeError):
    pass


def _headers(anon: str) -> dict:
    return {
        "Content-Type": "application/json",
        "x-anon-id": anon,
        "User-Agent": "veida-dify-plugin/0.0.1",
    }


def run(prompt: str, aspect_ratio: str = "1:1", timeout: float = 240.0) -> str:
    """Submit one job, poll it, return the CDN url of the finished image."""
    anon = f"dify-{uuid.uuid4()}"
    payload = {
        "provider": "kie",
        "mediaType": "image",
        "model": "veida-image-v1",
        "scene": "text-to-image",
        "prompt": prompt,
        "options": {"aspect_ratio": aspect_ratio},
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
    # surfaces as the misleading "the API returned no task id".
    if data.get("wall"):
        if data.get("reason") == "ip_daily":
            raise VeidaError(
                f"the per-IP daily ceiling ({IP_DAILY_CEILING} credits, about 7 "
                "images) is spent; try tomorrow or sign in at "
                "https://veida.ai/pricing?utm_source=dify&utm_medium=plugin"
            )
        raise VeidaError(
            "the free allowance for this caller is spent; sign in at "
            "https://veida.ai/pricing?utm_source=dify&utm_medium=plugin"
        )

    task_id = data.get("id")
    if not task_id:
        raise VeidaError("the API returned no task id")

    deadline = time.monotonic() + timeout
    query = (
        f"{BASE}/api/ai/anon-query?taskId={task_id}"
        "&provider=kie&mediaType=image"
    )
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
