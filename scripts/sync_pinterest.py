#!/usr/bin/env python3
"""Sync the canonical Form & Flöde / Pius Pinterest reference board.

No Pinterest credentials or third-party binary assets are written to the repository.
The script requests a short-lived API token, resolves the configured board, paginates
all Pins, then writes raw API metadata plus normalized GraceY reference records.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_BASE = "https://api.pinterest.com/v5"
BOARD_NAME = os.getenv("PINTEREST_BOARD_NAME", "Form & Flöde / Pius - Reference board")
BOARD_ID_OVERRIDE = os.getenv("PINTEREST_BOARD_ID", "").strip()
APP_ID = os.getenv("PINTEREST_APP_ID", "").strip()
APP_SECRET = os.getenv("PINTEREST_APP_SECRET", "").strip()

OUT_DIR = Path("data/pinterest/form-flode-pius-reference-board")
RAW_PATH = OUT_DIR / "raw.json"
NORMALIZED_PATH = OUT_DIR / "normalized.json"
SOURCE_PATH = Path("sources/pinterest/form-flode-pius-reference-board.json")


def request_json(url: str, *, token: str | None = None, data: bytes | None = None, basic: str | None = None):
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if basic:
        headers["Authorization"] = f"Basic {basic}"
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, headers=headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Pinterest API HTTP {exc.code}: {body}") from exc


def get_access_token() -> str:
    if not APP_ID or not APP_SECRET:
        raise RuntimeError("PINTEREST_APP_ID and PINTEREST_APP_SECRET are required")
    basic = base64.b64encode(f"{APP_ID}:{APP_SECRET}".encode()).decode()
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "scope": "boards:read,pins:read",
    }).encode()
    payload = request_json(f"{API_BASE}/oauth/token", data=body, basic=basic)
    token = payload.get("access_token")
    if not token:
        raise RuntimeError(f"Pinterest token response did not contain access_token: {payload}")
    return token


def paginated(endpoint: str, token: str):
    items = []
    bookmark = None
    while True:
        params = {"page_size": "250"}
        if bookmark:
            params["bookmark"] = bookmark
        sep = "&" if "?" in endpoint else "?"
        payload = request_json(f"{API_BASE}{endpoint}{sep}{urllib.parse.urlencode(params)}", token=token)
        items.extend(payload.get("items") or [])
        bookmark = payload.get("bookmark")
        if not bookmark:
            return items


def resolve_board(token: str):
    if BOARD_ID_OVERRIDE:
        return {"id": BOARD_ID_OVERRIDE, "name": BOARD_NAME}
    boards = paginated("/boards", token)
    exact = [b for b in boards if b.get("name") == BOARD_NAME]
    if len(exact) != 1:
        found = [b.get("name") for b in boards]
        raise RuntimeError(
            f"Expected exactly one board named {BOARD_NAME!r}; found {len(exact)}. "
            f"Available board names: {found}"
        )
    return exact[0]


def choose_image(pin: dict):
    media = pin.get("media") or {}
    images = media.get("images") or {}
    candidates = []
    for spec in images.values():
        if isinstance(spec, dict) and spec.get("url"):
            width = spec.get("width") or 0
            height = spec.get("height") or 0
            candidates.append((width * height, spec["url"]))
    return max(candidates, default=(0, None))[1]


def normalize(pin: dict, board: dict, captured_at: str):
    pin_id = str(pin.get("id") or "")
    owner = pin.get("board_owner") or {}
    return {
        "reference_id": f"PIN-{pin_id}",
        "source_id": "SRC-PIN-001",
        "source_platform": "Pinterest",
        "source_object_id": pin_id,
        "source_board_id": str(board.get("id") or pin.get("board_id") or ""),
        "source_board_name": board.get("name") or BOARD_NAME,
        "source_url": f"https://www.pinterest.com/pin/{pin_id}/",
        "external_link": pin.get("link"),
        "title": pin.get("title"),
        "description": pin.get("description"),
        "alt_text": pin.get("alt_text"),
        "creator": owner.get("username"),
        "created_at": pin.get("created_at"),
        "captured_at": captured_at,
        "media": {
            "media_type": (pin.get("media") or {}).get("media_type"),
            "remote_image_url": choose_image(pin),
            "dominant_color": pin.get("dominant_color"),
        },
        "reference_status": "raw-unreviewed",
        "design_dna": {
            "typography": None,
            "grid_layout": None,
            "hierarchy": None,
            "color_logic": None,
            "geometry": None,
            "density": None,
            "imagery": None,
            "texture": None,
            "data_visualization": None,
            "motion_interaction": None,
            "visual_grammar": None,
            "reusable_principles": [],
            "anti_patterns": [],
        },
        "provenance": {
            "source_preserved": True,
            "binary_mirrored": False,
            "notes": "Metadata ingested from Pinterest API; third-party binary asset remains remote.",
        },
    }


def main():
    token = get_access_token()
    board = resolve_board(token)
    board_id = str(board["id"])
    pins = paginated(f"/boards/{urllib.parse.quote(board_id)}/pins", token)
    captured_at = datetime.now(timezone.utc).isoformat()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps({
        "source_id": "SRC-PIN-001",
        "captured_at": captured_at,
        "board": board,
        "pins": pins,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    normalized = [normalize(pin, board, captured_at) for pin in pins]
    NORMALIZED_PATH.write_text(json.dumps({
        "source_id": "SRC-PIN-001",
        "captured_at": captured_at,
        "count": len(normalized),
        "references": normalized,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    source["board_id"] = board_id
    source["ingestion_status"] = "active"
    source["last_sync"] = captured_at
    SOURCE_PATH.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Synced {len(normalized)} Pinterest references from board {BOARD_NAME!r} ({board_id}).")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
