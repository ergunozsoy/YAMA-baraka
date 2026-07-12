"""Müfettiş — kalite ve bakım kontrolleri.

Amacı:   Repoların bakım durumunu ölçmek.
Yetkisi: Yalnızca okuma. Bulgu üretir.
Sınırı:  Uygulama yapamaz, düzeltemez.
Sorumlu: Bulgularını BEY'e (scan.py) teslim eder.
"""

from __future__ import annotations

from datetime import datetime, timezone

from .checks import Finding
from .github_client import GitHubClient


def _days_since(iso_ts: str) -> int:
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def run(gh: GitHubClient, owner: str, name: str, repo_data: dict,
        stale_after_days: int = 90) -> list[Finding]:
    findings: list[Finding] = []

    # 1. Aktiflik
    pushed_at = repo_data.get("pushed_at")
    if pushed_at:
        days = _days_since(pushed_at)
        if days > stale_after_days * 2:
            findings.append(Finding("Müfettiş", "Aktiflik", "fail",
                                    f"Son push {days} gün önce (eşik: {stale_after_days})."))
        elif days > stale_after_days:
            findings.append(Finding("Müfettiş", "Aktiflik", "warn",
                                    f"Son push {days} gün önce (eşik: {stale_after_days})."))
        else:
            findings.append(Finding("Müfettiş", "Aktiflik", "ok",
                                    f"Son push {days} gün önce."))
    else:
        findings.append(Finding("Müfettiş", "Aktiflik", "unknown", "Push tarihi okunamadı."))

    # 2. README
    if gh.has_path(owner, name, "README.md"):
        findings.append(Finding("Müfettiş", "README", "ok", "README.md mevcut."))
    else:
        findings.append(Finding("Müfettiş", "README", "warn", "README.md yok."))

    # 3. Açıklama
    if repo_data.get("description"):
        findings.append(Finding("Müfettiş", "Açıklama", "ok", "Repo açıklaması girilmiş."))
    else:
        findings.append(Finding("Müfettiş", "Açıklama", "warn", "Repo açıklaması boş."))

    # 4. CI
    if gh.has_path(owner, name, ".github/workflows"):
        findings.append(Finding("Müfettiş", "CI", "ok", "GitHub Actions workflow tanımlı."))
    else:
        findings.append(Finding("Müfettiş", "CI", "warn", "CI workflow tanımlı değil."))

    # 5. Açık issue sayısı (bilgilendirici)
    open_issues = repo_data.get("open_issues_count", 0)
    level = "warn" if open_issues >= 20 else "ok"
    findings.append(Finding("Müfettiş", "Açık issue", level, f"{open_issues} açık issue."))

    # 6. Release
    release = gh.latest_release(owner, name)
    if release:
        findings.append(Finding("Müfettiş", "Sürüm", "ok",
                                f"Son sürüm: {release.get('tag_name', '?')}"))
    else:
        findings.append(Finding("Müfettiş", "Sürüm", "warn", "Hiç release yayınlanmamış."))

    return findings
