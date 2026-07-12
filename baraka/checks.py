"""Ortak bulgu (Finding) modeli.

Her kontrol bir Finding üretir. Rapor dili BARAKA_PRINCIPLES.md'deki sözlüğü kullanır:
  ok        🟢  sorun yok
  info      ℹ️  bilgi notu (sağlığı etkilemez; iyileştirme fırsatı)
  warn      🟡  bakım gerektiren bulgu
  fail      🔴  güvenlik/işlerlik sorunu
  unknown   ⚪  kontrol edilemedi (yetki/erişim eksik)

v0.1.1: Kontrol şiddeti repo kritikliğine göre ayarlanır. Aynı eksik,
high bir repoda uyarıyken low bir repoda bilgi notudur. Böylece rapor
"her şey sarı" olmaz; gerçekten dikkat gerektiren repolar öne çıkar.
"""

from __future__ import annotations

from dataclasses import dataclass

LEVELS = ("ok", "info", "warn", "fail", "unknown")
ICONS = {"ok": "🟢", "info": "ℹ️", "warn": "🟡", "fail": "🔴", "unknown": "⚪"}


@dataclass
class Finding:
    source: str      # "Bekçi" | "Müfettiş"
    check: str       # kontrolün adı
    level: str       # ok | info | warn | fail | unknown
    detail: str      # tek cümlelik açıklama

    def __post_init__(self):
        if self.level not in LEVELS:
            raise ValueError(f"Geçersiz seviye: {self.level}")

    @property
    def icon(self) -> str:
        return ICONS[self.level]


def by_crit(criticality: str, high: str = "warn", normal: str = "info",
            low: str = "info") -> str:
    """Kritikliğe göre bulgu seviyesi seçer."""
    return {"high": high, "normal": normal, "low": low}.get(criticality, normal)


def overall_health(findings: list[Finding]) -> str:
    """Bulgulardan repo sağlık durumu türetir (BEY'in basit karar kuralı).

    info ve unknown sağlığı düşürmez (İlke 6: kontrol edilemeyen şey
    'kötü' de sayılmaz, 'iyi' de gösterilmez — ⚪ olarak görünür).
    """
    levels = [f.level for f in findings]
    if "fail" in levels:
        return "🔴 Kritik"
    if "warn" in levels:
        return "🟡 Dikkat"
    return "🟢 Sağlıklı"
