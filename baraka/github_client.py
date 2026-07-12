"""GitHub API istemcisi.

İki modda çalışır:
- canlı: api.github.com (GITHUB_TOKEN varsa yetkili, yoksa anonim)
- offline: bir JSON fixture dosyasından okur (test/demo için)

Baraka v0.1 salt okunurdur: bu istemci yalnızca GET yapar.
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional

import requests

API = "https://api.github.com"


class GitHubClient:
    def __init__(self, token: Optional[str] = None, offline_fixture: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self._fixture: Optional[dict] = None
        if offline_fixture:
            with open(offline_fixture, encoding="utf-8") as f:
                self._fixture = json.load(f)

    # ---- düşük seviye ----

    def _get(self, path: str) -> tuple[int, Any]:
        """(status_code, json) döndürür. Offline modda fixture'dan okur."""
        if self._fixture is not None:
            entry = self._fixture.get(path)
            if entry is None:
                return 404, {"message": "Not Found (fixture)"}
            return entry.get("status", 200), entry.get("body")

        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        resp = requests.get(f"{API}{path}", headers=headers, timeout=30)
        try:
            body = resp.json()
        except ValueError:
            body = None
        return resp.status_code, body

    # ---- yüksek seviye ----

    def repo(self, owner: str, name: str) -> tuple[int, Any]:
        return self._get(f"/repos/{owner}/{name}")

    def root_contents(self, owner: str, name: str) -> list[dict]:
        status, body = self._get(f"/repos/{owner}/{name}/contents/")
        return body if status == 200 and isinstance(body, list) else []

    def has_path(self, owner: str, name: str, path: str) -> bool:
        status, _ = self._get(f"/repos/{owner}/{name}/contents/{path}")
        return status == 200

    def latest_release(self, owner: str, name: str) -> Optional[dict]:
        status, body = self._get(f"/repos/{owner}/{name}/releases/latest")
        return body if status == 200 else None

    def user_repos(self, owner: str) -> list[dict]:
        """Owner'ın tüm public repolarını listeler (sayfalı).

        Otomatik keşif için kullanılır; yalnızca GitHub Actions gibi
        API erişimi tam olan ortamlarda çalışır.
        """
        repos: list[dict] = []
        page = 1
        while True:
            status, body = self._get(f"/users/{owner}/repos?per_page=100&page={page}&sort=full_name")
            if status != 200 or not isinstance(body, list) or not body:
                break
            repos.extend(body)
            if len(body) < 100:
                break
            page += 1
        return repos

    def dependabot_alerts(self, owner: str, name: str) -> tuple[str, int]:
        """('ok'|'unavailable', açık uyarı sayısı) döndürür.

        Dependabot uyarıları yetkili token ister; anonim/yetkisiz istekte
        'unavailable' döner ve rapor bunu ⚪ olarak gösterir (İlke 6).
        """
        status, body = self._get(f"/repos/{owner}/{name}/dependabot/alerts?state=open&per_page=100")
        if status == 200 and isinstance(body, list):
            return "ok", len(body)
        return "unavailable", 0
