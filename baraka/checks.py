"""Ortak bulgu (Finding) modeli.

Her kontrol bir Finding üretir. Rapor dili BARAKA_PRINCIPLES.md'deki sözlüğü kullanır:
  ok        🟢  sorun yok
  warn      🟡  bakım gerektiren bulgu
  fail      🔴  güvenlik/işlerlik sorunu
  unknown   ⚪  kontrol edilemedi (yetki/erişim eksik)
"""

from __future__ import annotations

from dataclasses import dataclass

LEVELS = ("ok", "warn", "fail", "unknown")
ICONS = {"ok": "🟢", "warn": "🟡", "fail": "🔴", "unknown": "⚪"}


@dataclass
class Finding:
    source: str      # "Bekçi" | "Müfettiş"
    check: str       # kontrolün adı
    level: str       # ok | warn | fail | unknown
    detail: str      # tek cümlelik açıklama

    def __post_init__(self):
        if self.level not in LEVELS:
            raise ValueError(f"Geçersiz seviye: {self.level}")

    @property
    def icon(self) -> str:
        return ICONS[self.level]


def overall_health(findings: list[Finding]) -> str:
    """Bulgulardan repo sağlık durumu türetir (BEY'in basit karar kuralı)."""
    levels = [f.level for f in findings]
    if "fail" in levels:
        return "🔴 Kritik"
    if "warn" in levels:
        return "🟡 Dikkat"
    return "🟢 Sağlıklı"
