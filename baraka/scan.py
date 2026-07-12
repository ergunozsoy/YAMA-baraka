"""BEY — orkestratör.

Registry'yi okur, her repo için Bekçi ve Müfettiş kontrollerini çalıştırır,
sağlık durumunu türetir, Kedi'ye söz hakkı verir ve sonucu Yazmanlara teslim eder.

Kullanım:
    python -m baraka.scan [--registry registry.yaml] [--offline tests/fixtures.json]
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone

import yaml

from . import cat, guardian, inspector, scribe
from .checks import overall_health
from .github_client import GitHubClient


def load_registry(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        reg = yaml.safe_load(f)
    if not reg or "owner" not in reg or ("repos" not in reg and not reg.get("discover")):
        raise SystemExit("registry.yaml geçersiz: 'owner' ve ('repos' veya 'discover: true') zorunlu.")
    if reg["owner"] == "DEGISTIR-BENI":
        print("UYARI: registry.yaml içindeki owner alanı henüz doldurulmamış.", file=sys.stderr)
    return reg


def resolve_repos(reg: dict, gh: GitHubClient) -> list[dict]:
    """Elle listelenen repoları otomatik keşifle birleştirir.

    discover: true ise owner'ın tüm public repoları çekilir,
    include_pattern'e uyanlar defaults değerleriyle envantere eklenir.
    Elle yazılan girdiler her zaman önceliklidir; exclude listesi atlanır.
    """
    explicit = {e["name"]: dict(e) for e in (reg.get("repos") or [])}
    merged = dict(explicit)

    if reg.get("discover"):
        defaults = reg.get("defaults") or {}
        pattern = reg.get("include_pattern")
        exclude = set(reg.get("exclude") or [])
        discovered = gh.user_repos(reg["owner"])
        if not discovered:
            print("UYARI: Otomatik keşif sonuç döndürmedi (API erişimi kısıtlı olabilir); "
                  "yalnızca elle listelenen repolar taranacak.", file=sys.stderr)
        for r in discovered:
            name = r.get("name", "")
            if not name or name in merged or name in exclude:
                continue
            if r.get("fork"):
                continue
            if pattern and not re.search(pattern, name):
                continue
            merged[name] = {
                "name": name,
                "criticality": defaults.get("criticality", "normal"),
                "stale_after_days": defaults.get("stale_after_days", 120),
                "notes": (r.get("description") or "").strip() or "(otomatik keşif)",
            }

    return sorted(merged.values(), key=lambda e: e["name"].lower())


def scan(registry_path: str, offline_fixture: str | None = None, base_dir: str = ".") -> int:
    reg = load_registry(registry_path)
    owner = reg["owner"]
    gh = GitHubClient(offline_fixture=offline_fixture)

    results: list[dict] = []
    for entry in resolve_repos(reg, gh):
        name = entry["name"]
        criticality = entry.get("criticality", "normal")
        stale = int(entry.get("stale_after_days", 90))
        notes = entry.get("notes", "")
        print(f"⏳ Taranıyor: {owner}/{name}")

        status, repo_data = gh.repo(owner, name)
        if status != 200 or not isinstance(repo_data, dict):
            results.append({
                "name": name, "criticality": criticality, "notes": notes,
                "health": "⚪ Kontrol edilemedi", "findings": [],
                "error": f"HTTP {status}", "repo_data": None, "days_since_push": None,
            })
            continue

        findings = guardian.run(gh, owner, name, repo_data, criticality=criticality)
        findings += inspector.run(gh, owner, name, repo_data,
                                  stale_after_days=stale, criticality=criticality)

        days_since_push = None
        if repo_data.get("pushed_at"):
            pushed = datetime.fromisoformat(repo_data["pushed_at"].replace("Z", "+00:00"))
            days_since_push = (datetime.now(timezone.utc) - pushed).days

        results.append({
            "name": name, "criticality": criticality, "notes": notes,
            "health": overall_health(findings), "findings": findings,
            "error": None, "repo_data": repo_data, "days_since_push": days_since_push,
        })

    cat_note = cat.wander([r for r in results if r["repo_data"]])
    report = scribe.render_report(results, cat_note, owner)
    current, archived = scribe.write_and_archive(report, base_dir=base_dir)

    print(f"✅ Rapor yazıldı: {current}")
    print(f"📚 Arşivlendi:   {archived}")

    critical = [r["name"] for r in results if r["health"].startswith("🔴")]
    if critical:
        print(f"🔴 Kritik repo(lar): {', '.join(critical)}", file=sys.stderr)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Baraka sağlık taraması (BEY)")
    p.add_argument("--registry", default="registry.yaml")
    p.add_argument("--offline", default=None, help="Fixture JSON ile canlı API'siz çalıştır")
    p.add_argument("--base-dir", default=".", help="reports/ ve archive/ için kök dizin")
    args = p.parse_args()
    return scan(args.registry, offline_fixture=args.offline, base_dir=args.base_dir)


if __name__ == "__main__":
    raise SystemExit(main())
