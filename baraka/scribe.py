"""Yazmanlar — rapor üretimi ve kurumsal hafıza.

Amacı:   Her taramayı okunabilir rapora dönüştürmek ve arşivlemek.
Yetkisi: Yalnızca Baraka'nın kendi reposuna yazar (reports/, archive/).
Sınırı:  Başka repolara yazamaz; içerik üretmez, kayıt tutar.
Sorumlu: Rapor BEY adına yayınlanır.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from . import __version__
from .checks import ICONS, Finding


def render_report(results: list[dict], cat_note: Optional[str], owner: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# YAMA Hub Sağlık Raporu",
        "",
        f"Tarama: {now} · Sahip: `{owner}` · Baraka v{__version__}",
        "",
        "## Genel durum",
        "",
        "| Repo | Durum | Kritiklik | Bulgular | Not |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        counts = {"fail": 0, "warn": 0, "info": 0, "unknown": 0}
        for f in r.get("findings", []):
            if f.level in counts:
                counts[f.level] += 1
        parts = [f"{n} {ICONS[lvl]}" for lvl, n in counts.items() if n]
        summary = " · ".join(parts) if parts else "—"
        lines.append(f"| {r['name']} | {r['health']} | {r['criticality']} | {summary} | {r['notes']} |")

    if cat_note:
        lines += ["", "## Kedi'nin notu", "", f"> {cat_note}"]

    lines += ["", "## Ayrıntılar", ""]
    for r in results:
        lines.append(f"### {r['name']} — {r['health']}")
        lines.append("")
        if r.get("error"):
            lines.append(f"⚪ Repo okunamadı: {r['error']}")
            lines.append("")
            continue
        lines.append("| Kaynak | Kontrol | Durum | Ayrıntı |")
        lines.append("|---|---|---|---|")
        for f in r["findings"]:
            assert isinstance(f, Finding)
            lines.append(f"| {f.source} | {f.check} | {f.icon} | {f.detail} |")
        lines.append("")

    lines += [
        "---",
        "",
        "_Bu rapor Baraka tarafından otomatik üretilmiştir. Baraka v0.1 salt okunurdur:_",
        "_hiçbir repoyu değiştirmez, yalnızca okur, ölçer ve raporlar._",
        "",
    ]
    return "\n".join(lines)


def write_and_archive(report: str, base_dir: str = ".") -> tuple[Path, Path]:
    base = Path(base_dir)
    reports_dir = base / "reports"
    archive_dir = base / "archive"
    reports_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)

    current = reports_dir / "HEALTH_REPORT.md"
    current.write_text(report, encoding="utf-8")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    archived = archive_dir / f"{stamp}-health.md"
    archived.write_text(report, encoding="utf-8")

    return current, archived
