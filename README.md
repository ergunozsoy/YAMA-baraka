# Baraka

**Baraka, YAMA Hub'daki repo ve uygulamaların bakımını, güvenliğini, gelişimini ve
kurumsal hafızasını yöneten yönetim katmanıdır.**

YAMA Ana Gemisi'nin köprüsüdür. YAMA'nın modülleri (Museum, Flight, Health, Nota,
Time Traveling, Heritage, ...) gövdeyi oluşturur; Baraka bu gövdenin sağlıklı
yaşamasını sağlar.

## Ne yapar? (v0.1)

- `registry.yaml` içindeki tüm YAMA repolarını haftada bir tarar
- Her repo için **güvenlik** (Bekçi) ve **kalite** (Müfettiş) kontrolleri çalıştırır
- Sonuçları tek bir **Sağlık Raporu**'nda toplar (`reports/HEALTH_REPORT.md`)
- Her raporu tarihli olarak arşivler (Yazmanlar, `archive/`)
- Haftada bir Kedi rastgele bir repoya bakar ve tek paragraflık bir gözlem bırakır

## Ne yapmaz? (v0.1)

- **Hiçbir repoyu değiştirmez.** Baraka v0.1 salt okunurdur: okur, ölçer, raporlar.
- Otomatik PR açmaz, dosya silmez, ayar değiştirmez.
- Yazma yetkisi (issue/PR açma) v0.2'de bilinçli bir kararla eklenecektir.

## Kurumlar ve yazılım karşılıkları

| Kurum | Yazılım karşılığı | Dosya |
|---|---|---|
| BEY | Orkestrasyon: taramayı başlatır, sonuçları toplar | `baraka/scan.py` |
| Bekçi | Güvenlik kontrolleri | `baraka/guardian.py` |
| Müfettiş | Kalite ve bakım kontrolleri | `baraka/inspector.py` |
| Yazmanlar | Rapor üretimi ve arşiv | `baraka/scribe.py` |
| Kedi | Rastgele, görevsiz gözlem | `baraka/cat.py` |
| Oyun Bahçesi | Fikir havuzu (Irmak & Deniz) | `ideas/` |
| Konsey, YerDede, GökDede | AI değerlendirme katmanı | v0.3 (bkz. ROADMAP) |

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Kullanım

```bash
# Gerçek tarama (GITHUB_TOKEN ortam değişkeni önerilir, public repolar için zorunlu değil)
export GITHUB_TOKEN=ghp_...
python -m baraka.scan

# Canlı API olmadan deneme (örnek verilerle)
python -m baraka.scan --offline tests/fixtures.json
```

Rapor: `reports/HEALTH_REPORT.md`

## Otomatik çalışma

`.github/workflows/health-scan.yml` her pazartesi 06:00 UTC'de taramayı çalıştırır
ve güncel raporu bu repoya commit eder. Elle tetiklemek için Actions sekmesinden
**Run workflow** kullanılabilir.

## Belgeler

- [`docs/BARAKA_ARCHITECTURE.md`](docs/BARAKA_ARCHITECTURE.md) — nasıl çalışır
- [`docs/BARAKA_ROADMAP.md`](docs/BARAKA_ROADMAP.md) — nasıl gelişecek
- [`docs/BARAKA_PRINCIPLES.md`](docs/BARAKA_PRINCIPLES.md) — hangi ilkelere göre karar verir

## Temel ilke

> Dil modelleri araçtır; akıl Baraka'dadır.
> Ve: her karakterin somut bir yazılım karşılığı olmak zorundadır.
