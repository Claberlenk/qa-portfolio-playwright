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

def api_get(path: str, **kwargs: Any) -> requests.Response:
    return requests.get(f"{BASE_API_URL}{path}", timeout=10, **kwargs)


def api_post(path: str, payload: dict, **kwargs: Any) -> requests.Response:
    return requests.post(f"{BASE_API_URL}{path}", json=payload, timeout=10, **kwargs)


def api_put(path: str, payload: dict, **kwargs: Any) -> requests.Response:
    return requests.put(f"{BASE_API_URL}{path}", json=payload, timeout=10, **kwargs)


def api_patch(path: str, payload: dict, **kwargs: Any) -> requests.Response:
    return requests.patch(f"{BASE_API_URL}{path}", json=payload, timeout=10, **kwargs)


def api_delete(path: str, **kwargs: Any) -> requests.Response:
    return requests.delete(f"{BASE_API_URL}{path}", timeout=10, **kwargs)
