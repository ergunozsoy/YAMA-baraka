# BARAKA_ARCHITECTURE

## 1. Amaç

Baraka, YAMA Hub'daki repoların **bakımını, güvenliğini, gelişimini ve kurumsal
hafızasını** yöneten koordinasyon katmanıdır. YAMA gövdedir, Baraka köprüdür.

Baraka'nın amacı YAMA'yı yönetmek değil; YAMA Hub'daki projelerin **sağlıklı
yaşamasını** sağlamaktır.

## 2. Temel ilkeler

1. **Somutluk ilkesi:** Her karakterin somut bir yazılım karşılığı olmak zorundadır.
   Karşılığı tanımlanamayan kurum, o sürüme girmez.
2. **Model bağımsızlığı:** Dil modelleri değiştirilebilir araçlardır. Baraka'nın
   kimliği, karar protokolü ve hafızası model sağlayıcısından bağımsızdır.
3. **Salt okunur başlangıç:** v0.1 hiçbir repoyu değiştirmez. Yazma yetkisi
   kademeli ve bilinçli olarak açılır (bkz. §6).
4. **GitHub üzerinde yaşar:** Baraka ayrı bir sunucu değildir. Zamanlanmış
   GitHub Actions + Python betikleri olarak çalışır. Bakım yükünü azaltmak için
   kurulan sistemin kendisi bakım yükü olmamalıdır.

## 3. Bileşenler (v0.1)

### BEY — `baraka/scan.py`
Orkestratör. Registry'yi okur, her repo için Bekçi ve Müfettiş kontrollerini
çalıştırır, sonuçları toplar, Yazmanlara teslim eder. Karar mantığı basittir:
kontrol sonuçlarından repo sağlık durumu (🟢/🟡/🔴) türetilir.

### Bekçi — `baraka/guardian.py`
Güvenlik ve düzen kontrolleri:
- Lisans var mı?
- SECURITY.md var mı?
- Repoda commit edilmiş `.env` / anahtar dosyası izi var mı? (kök dizin taraması)
- Dependabot uyarıları (token yetkisi varsa; yoksa "kontrol edilemedi" olarak raporlanır)
- Repo arşivlenmiş/devre dışı mı?

### Müfettiş — `baraka/inspector.py`
Kalite ve bakım kontrolleri:
- Son push ne zaman? (aktiflik eşiği: registry'de repo başına tanımlanabilir)
- README var mı, açıklama (description) girilmiş mi?
- CI workflow tanımlı mı?
- Açık issue sayısı
- Son sürüm/release var mı?

### Yazmanlar — `baraka/scribe.py`
Kurumsal hafıza:
- Tüm sonuçları `reports/HEALTH_REPORT.md` olarak yazar
- Her taramayı `archive/YYYY-MM-DD-health.md` olarak saklar
- Böylece "geçen ay bu repo ne durumdaydı?" sorusu her zaman cevaplanabilir

### Kedi — `baraka/cat.py`
Görevsiz gözlemci. Her taramada (hafta numarasıyla tohumlanmış rastgelelikle)
tek bir repo seçer ve tarama verilerinden dikkat çekici tek bir gözlem üretir.
Gözlem rapora "🐈 Kedi'nin notu" olarak eklenir. Kedi hiçbir kontrol listesine
bağlı değildir, puan vermez, hiçbir şeyi değiştiremez.

### Oyun Bahçesi — `ideas/`
Irmak ve Deniz'in yaşadığı fikir havuzu. Sadece bir klasördür. Buradaki hiçbir
fikir otomatik olarak geliştirmeye dönüşmez; olgunlaşan fikirler elle
değerlendirilir.

### Konsey, YerDede, GökDede — v0.3
AI değerlendirme katmanı. Deterministik temel çalışmadan AI değerlendirmesi
anlam taşımaz; bu yüzden ertelenmiştir. Geldiklerinde görevleri: Müfettiş ve
Bekçi bulgularını yorumlamak, öncelik önermek ve büyük değişiklik taleplerinde
iki perspektifli (gerçeklik/vizyon) görüş üretmek olacaktır.

## 4. Veri akışı

```
registry.yaml
     │
     ▼
   BEY (scan.py)
     │  her repo için
     ├── Bekçi  → güvenlik bulguları
     ├── Müfettiş → kalite bulguları
     └── Kedi   → (haftalık tek gözlem)
     │
     ▼
  Yazmanlar (scribe.py)
     ├── reports/HEALTH_REPORT.md   (güncel durum)
     └── archive/YYYY-MM-DD-health.md (tarih damgalı kopya)
```

## 5. Registry

`registry.yaml` Baraka'nın envanteridir. İki kaynaktan beslenir:

```yaml
owner: ergunozsoy
discover: true              # owner'ın tüm public repolarını otomatik bul
include_pattern: "^YAMA-"   # keşif filtresi (fork'lar her zaman hariç)
exclude: []                 # keşiften hariç tutulacaklar
defaults:                   # keşfedilen repolar için varsayılanlar
  criticality: normal
  stale_after_days: 120
repos:                      # elle tanımlar; keşfin üzerine yazar
  - name: YAMA-Lokman
    criticality: high        # high | normal | low
    stale_after_days: 90     # bu süre push olmazsa "hareketsiz" uyarısı
    notes: "Sağlık modülü"
```

Böylece yeni bir YAMA reposu açıldığında elle liste güncellemeye gerek kalmaz;
bir sonraki taramada Baraka onu kendisi bulur. Elle girilen kayıtlar her zaman
önceliklidir.

## 6. Yetki sınırları

| Sürüm | Baraka'nın yetkisi |
|---|---|
| v0.1 | Salt okunur: okur, ölçer, raporlar. Yalnızca kendi reposuna yazar (rapor/arşiv). |
| v0.2 | Kendi reposunda bulgu başına issue açabilir. Diğer repolara dokunamaz. |
| v0.3+ | Hedef repolara PR önerebilir (asla doğrudan merge edemez). |

Değişmez kurallar:
- Kedi hiçbir şeyi değiştiremez.
- Irmak ve Deniz karar veremez.
- Müfettiş uygulama yapamaz.
- Baraka kendi işini kendisi onaylayamaz; merge her zaman insana aittir.
