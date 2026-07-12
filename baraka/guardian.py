"""Bekçi — güvenlik ve düzen kontrolleri.

Amacı:   Repoların güvenlik hijyenini kontrol etmek.
Yetkisi: Yalnızca okuma. Bulgu üretir.
Sınırı:  Hiçbir şeyi değiştiremez, durduramaz (v0.1).
Sorumlu: Bulgularını BEY'e (scan.py) teslim eder.

Şiddet politikası (v0.1.1): Güvenlikle doğrudan ilgili bulgular (sızıntı izi)
kritiklikten bağımsız 🔴'dur. Hijyen bulguları (lisans, SECURITY.md) yalnızca
high repolarda 🟡, diğerlerinde ℹ️'dir.
"""

from __future__ import annotations

from .checks import Finding, by_crit
from .github_client import GitHubClient

# Kök dizinde bulunması sızıntı şüphesi doğuran dosya adları
SUSPICIOUS_FILES = {".env", ".env.local", ".env.production", "id_rsa", "id_ed25519",
                    "credentials.json", "service-account.json", "secrets.yaml", "secrets.yml"}


def run(gh: GitHubClient, owner: str, name: str, repo_data: dict,
        criticality: str = "normal") -> list[Finding]:
    findings: list[Finding] = []

    # 1. Arşiv / devre dışı durumu
    if repo_data.get("archived"):
        findings.append(Finding("Bekçi", "Arşiv durumu", "warn",
                                "Repo arşivlenmiş; registry'de hâlâ aktif görünüyor."))
    if repo_data.get("disabled"):
        findings.append(Finding("Bekçi", "Erişim", "fail", "Repo devre dışı bırakılmış."))

    # 2. Lisans
    if repo_data.get("license"):
        findings.append(Finding("Bekçi", "Lisans", "ok",
                                f"Lisans: {repo_data['license'].get('spdx_id', '?')}"))
    else:
        findings.append(Finding("Bekçi", "Lisans",
                                by_crit(criticality, high="warn", normal="info", low="info"),
                                "Lisans dosyası yok (public repo 'tüm hakları saklı' sayılır)."))

    # 3. SECURITY.md — yalnızca high repolarda uyarı
    if gh.has_path(owner, name, "SECURITY.md"):
        findings.append(Finding("Bekçi", "SECURITY.md", "ok", "Güvenlik politikası mevcut."))
    else:
        findings.append(Finding("Bekçi", "SECURITY.md",
                                by_crit(criticality, high="warn", normal="info", low="info"),
                                "SECURITY.md yok."))

    # 4. Kök dizinde sızıntı izi — kritiklikten bağımsız 🔴
    root = gh.root_contents(owner, name)
    leaked = sorted({item.get("name", "") for item in root} & SUSPICIOUS_FILES)
    if leaked:
        findings.append(Finding("Bekçi", "Sızıntı izi", "fail",
                                f"Şüpheli dosya(lar) commit edilmiş: {', '.join(leaked)}"))
    else:
        findings.append(Finding("Bekçi", "Sızıntı izi", "ok",
                                "Kök dizinde şüpheli dosya yok."))

    # 5. Dependabot uyarıları (yetkili token gerekir)
    status, count = gh.dependabot_alerts(owner, name)
    if status == "unavailable":
        findings.append(Finding("Bekçi", "Dependabot", "unknown",
                                "Kontrol edilemedi (token yetkisi gerekli)."))
    elif count == 0:
        findings.append(Finding("Bekçi", "Dependabot", "ok", "Açık güvenlik uyarısı yok."))
    else:
        if criticality == "high":
            level = "fail" if count >= 5 else "warn"
        else:
            level = "warn" if count >= 5 else "info"
        findings.append(Finding("Bekçi", "Dependabot", level,
                                f"{count} açık bağımlılık güvenlik uyarısı var."))

    return findings
