# BARAKA_PRINCIPLES

Baraka'nın anayasası. Her yeni özellik bu sorulardan geçer.

## Dört soru

Her kurum (ve her yeni özellik) şu dört soruya net cevap vermelidir:

1. **Amacı nedir?** — Neden var?
2. **Yetkisi nedir?** — Neyi yapabilir?
3. **Sınırı nedir?** — Neyi yapamaz?
4. **Kime karşı sorumludur?** — Çıktısını kim denetler?

Cevap veremeyen özellik o sürüme girmez.

## İlkeler

1. **Somutluk** — Her karakterin somut bir yazılım karşılığı olmak zorundadır.
   Karakterler hikâye değil, servis isimleridir; hikâye tarafı rapor dilinde yaşar.

2. **Salt okunur varsayılan** — Baraka'nın varsayılan yetkisi okumaktır.
   Her yazma yetkisi ayrı bir sürüm kararıyla, kapsamı yazılı olarak açılır.

3. **İnsan onayı** — Baraka hiçbir zaman kendi değişikliğini kendisi onaylamaz.
   Merge, silme ve yayınlama her zaman insana aittir.

4. **Model bağımsızlığı** — Dil modelleri araçtır; akıl Baraka'dadır.
   Hiçbir kurum belirli bir LLM sağlayıcısına bağlanamaz.

5. **Hafıza** — Kaydedilmeyen tarama yapılmamış sayılır. Her çalışma
   Yazmanlar tarafından tarihli olarak arşivlenir.

6. **Şeffaf bulgu** — Rapor, kontrol edilemeyen şeyi "iyi" gibi göstermez.
   Token yetkisi olmayan kontroller "kontrol edilemedi" olarak işaretlenir.

7. **Kedi özgürdür** — Kedi'ye görev verilemez, çağrılamaz, puanlanamaz.
   Gözlemleri bilgilendiricidir; hiçbir kararın zorunlu girdisi değildir.

8. **Küçük ve geri alınabilir adımlar** — Her değişiklik önce en küçük
   çalışan hâliyle denenir; geri alınamayan adım atılmaz.

## Karar dili

Rapor ve gelecekteki karar çıktılarında durumlar şu sözlükle ifade edilir:

- 🟢 **Sağlıklı** — kritik bulgu yok
- ℹ️ **Bilgi notu** — iyileştirme fırsatı; sağlığı etkilemez
- 🟡 **Dikkat** — bakım gerektiren bulgu var
- 🔴 **Kritik** — güvenlik veya işlerlik sorunu var
- ⚪ **Kontrol edilemedi** — yetki/erişim eksik

**Kritikliğe duyarlı şiddet (v0.1.1):** Aynı eksik her repoda aynı ağırlıkta
değildir. SECURITY.md eksikliği `high` bir repoda 🟡, deneysel bir repoda ℹ️'dir.
Güvenlikle doğrudan ilgili bulgular (sızıntı izi) ise kritiklikten bağımsız 🔴'dur.
Amaç: rapor "her şey sarı" olmasın; gerçekten dikkat gerektiren repolar öne çıksın.
