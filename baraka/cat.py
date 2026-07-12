"""Kedi — görevsiz gözlemci.

Kedi'nin görevi yoktur. Kontrol listesi yoktur. Puan vermez.
Her taramada, hafta numarasıyla tohumlanmış rastgelelikle tek bir repoya
uğrar ve gördüklerinden tek bir gözlem seçer. Gözlem bilgilendiricidir;
hiçbir kararın zorunlu girdisi değildir. (BARAKA_PRINCIPLES, İlke 7)
"""

from __future__ import annotations

import random
from datetime import date
from typing import Optional


def wander(scan_results: list[dict], today: Optional[date] = None) -> Optional[str]:
    """scan_results: scan.py'nin repo başına topladığı sözlükler.

    Dönen değer: "🐈 ..." biçiminde tek paragraflık not, veya None
    (Kedi bazen hiçbir şey söylemez — bu da normaldir).
    """
    if not scan_results:
        return None

    today = today or date.today()
    year, week, _ = today.isocalendar()
    rng = random.Random(year * 100 + week)  # aynı hafta → aynı repo
    visit = rng.choice(scan_results)
    name = visit["name"]
    repo = visit.get("repo_data") or {}

    observations: list[str] = []

    days = visit.get("days_since_push")
    if days is not None and days > 180:
        observations.append(
            f"{name} reposuna uğradım. {days} gündür kimse dokunmamış; "
            f"pencere kenarında tozlanan bir kitap gibi duruyor.")

    if not repo.get("description"):
        observations.append(
            f"{name} reposunun kapısında isim tabelası yok (description boş). "
            f"İçeride ne olduğunu sadece bilenler biliyor.")

    stars = repo.get("stargazers_count", 0)
    if stars > 0:
        observations.append(
            f"{name} reposunda {stars} yıldız gördüm. Birileri burayı beğenmiş.")

    issues = repo.get("open_issues_count", 0)
    if issues > 0:
        observations.append(
            f"{name} reposunda {issues} açık issue duruyor. En eskisi kim bilir "
            f"ne zamandır cevap bekliyor.")

    if not observations:
        observations.append(
            f"Bugün {name} reposunda gezindim. Her şey olağan görünüyordu; "
            f"biraz uyudum, sonra gittim.")

    return "🐈 " + rng.choice(observations)
