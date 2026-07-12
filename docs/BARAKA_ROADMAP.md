# BARAKA_ROADMAP

Her faz, bir önceki faz **gerçekten çalışmadan** başlamaz.

## v0.1 — Sağlık Raporu (bu sürüm)

- [x] registry.yaml (repo envanteri)
- [x] Müfettiş: aktiflik, README, açıklama, CI, release, açık issue kontrolleri
- [x] Bekçi: lisans, SECURITY.md, sızıntı izi, Dependabot (token'lı), arşiv durumu
- [x] Yazmanlar: HEALTH_REPORT.md + tarihli arşiv
- [x] Kedi: haftalık tek gözlem
- [x] GitHub Actions: haftalık otomatik tarama
- [ ] Registry'nin gerçek YAMA repolarıyla doldurulması
- [ ] İlk gerçek taramanın çalıştırılması ve raporun gözden geçirilmesi

## v0.2 — Bulgu takibi

- Kritik (🔴) bulgular için Baraka reposunda otomatik issue açma
- Aynı bulgu için mükerrer issue engelleme
- Rapora trend bilgisi: geçen taramaya göre iyileşti/kötüleşti
- Basit HTML pano (HEALTH_REPORT'un görsel hâli, GitHub Pages)

## v0.3 — Konsey, YerDede, GökDede (AI katmanı)

- Tarama bulgularının LLM ile yorumlanması ve önceliklendirilmesi
- YerDede: uygulanabilirlik/risk perspektifi; GökDede: uzun vade/kullanıcı perspektifi
- Konsey çıktısı: her tarama için "bu hafta ilk 3 öncelik" bölümü
- Model bağımsız adapter (Claude/GPT/Gemini/yerel model takılabilir)

## v0.4 — İnşaatçılar (öneri üretimi)

- Seçili bulgular için otomatik PR taslağı (README güncelleme, lisans ekleme gibi
  düşük riskli işler) — merge her zaman insanda
- Görev şablonları: Mimar (plan) → Usta (uygulama adımları) → İşçi (değişiklik)

## v0.5 — Oyun Bahçesi

- `ideas/` klasörüne yapı: fikir şablonu (Irmak sorusu / Deniz oyunu / gelecek sinyali)
- Konsey'in ayda bir fikir havuzunu değerlendirmesi

## Bilinçli olarak yapılmayacaklar

- Baraka için ayrı sunucu/hosting (GitHub üzerinde kalır)
- Diğer repolarda otomatik merge veya silme
- Kedi'ye görev, kota veya kontrol listesi verilmesi
