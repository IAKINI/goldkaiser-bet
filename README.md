# BETSPIN777 — Spin & Win

Neon mor-pembe temalı, Almanca bahis/casino sitesi + oynanabilir Aviator.
Masaüstü **tracker** ile çalışması için küçük bir Python **kanal sunucusu** içerir.

```
goldkaiser-bet/
├─ server.py          # kanal sunucusu (statik dosyaları servis eder + /api/state, /api/command)
├─ requirements.txt   # harici bağımlılık YOK (yalnızca Python standart kütüphanesi)
└─ web/
   ├─ index.html      # ana sayfa (kayıt/giriş, cüzdan, yatırma/çekme simülasyonu)
   └─ aviator.html    # Aviator oyunu (durumu sunucuya gönderir → tracker crash_at okur)
```

## Yerelde çalıştırma
```bash
cd goldkaiser-bet
python server.py 8000
```
- Ana sayfa:  http://localhost:8000/
- Aviator:    http://localhost:8000/aviator

## Render'da yayınlama (Web Service — tracker için gerekli)

> ⚠ Statik site DEĞİL. Tracker'ın çalışması için kalıcı süreç (Web Service) gerekir.

1. https://render.com → **New +** → **Web Service** → `goldkaiser-bet` reposunu seç.
2. Ayarlar:
   - **Language / Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
   - **Instance Type:** Free
3. Deploy → sana `https://goldkaiser-bet.onrender.com` gibi bir adres verir.
   (`PORT`'u Render otomatik verir; `server.py` onu okur.)

> Ücretsiz katman uykuya dalabilir (ilk açılış ~30 sn) ve yeniden başlarsa odalar sıfırlanır — demo için sorun değil.

## Tracker'ı bu siteye bağlama
Masaüstü `tracker.py` (ENTRY projesinde) HTTP modunda bu sunucuyu izler.
Bir başlatıcı `.bat` içindeki adresi yeni siteye çevir:
```
set CUPGAME_CHANNEL=http
set CUPGAME_SERVER=https://goldkaiser-bet.onrender.com
set CUPGAME_ROOM=MAIN
python tracker.py
```
Aviator'ı `…/aviator?room=MAIN` ile aç; tracker aynı oda kodunu (MAIN) kullansın.
Aviator her turda `crash_at` (kaç x'te düşeceği) bilgisini sunucuya yazar, tracker okur.

---
18+ · Demo amaçlıdır, gerçek bahis/ödeme yoktur.
