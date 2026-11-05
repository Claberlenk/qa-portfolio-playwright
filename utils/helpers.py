"""Shared helpers for UI and API test suites."""
from __future__ import annotations

import os
from typing import Any

import requests

BASE_UI_URL = "https://www.saucedemo.com"
BASE_API_URL = "https://reqres.in/api"

# ── Credentials ──────────────────────────────────────────────────────────────

STANDARD_USER = {"username": "standard_user", "password": "secret_sauce"}
LOCKED_USER = {"username": "locked_out_user", "password": "secret_sauce"}
PROBLEM_USER = {"username": "problem_user", "password": "secret_sauce"}


# ── API helpers ───────────────────────────────────────────────────────────────

def _request(method: str, path: str, **kwargs: Any) -> requests.Response:
    # Anonymous reqres.in traffic is limited to 40 requests/day per IP;
    # a free key from app.reqres.in raises the limit.
    headers = kwargs.pop("headers", {})
    api_key = os.environ.get("REQRES_API_KEY")
    if api_key:
        headers = {"x-api-key": api_key, **headers}
    return requests.request(method, f"{BASE_API_URL}{path}", timeout=10, headers=headers, **kwargs)


def api_get(path: str, **kwargs: Any) -> requests.Response:
    return _request("GET", path, **kwargs)


def api_post(path: str, payload: dict, **kwargs: Any) -> requests.Response:
    return _request("POST", path, json=payload, **kwargs)


def api_put(path: str, payload: dict, **kwargs: Any) -> requests.Response:
    return _request("PUT", path, json=payload, **kwargs)


def api_patch(path: str, payload: dict, **kwargs: Any) -> requests.Response:
    return _request("PATCH", path, json=payload, **kwargs)


def api_delete(path: str, **kwargs: Any) -> requests.Response:
    return _request("DELETE", path, **kwargs)
