# GOLDKAISER — Premium Wetten (Landing Page)

Lüks siyah-altın temalı, Almanca tek sayfalık tanıtım (landing) sitesi.
Tamamen statik: `index.html` (HTML + CSS + JS, dış bağımlılık sadece Google Fonts).

## Yerelde açma
`index.html` dosyasına çift tıkla — tarayıcıda açılır.

## Render'da yayınlama (Static Site — önerilen)

1. Bu klasörü GitHub'a at (aşağıda).
2. https://render.com → **New +** → **Static Site** → bu GitHub reposunu seç.
3. Ayarlar:
   - **Build Command:** *(boş bırak)*
   - **Publish Directory:** `.`
4. **Create Static Site** → sana `https://goldkaiser-bet.onrender.com` gibi bir adres verir.

> Statik site olduğu için uykuya dalma/sunucu derdi yok, anında açılır.

## GitHub'a atma
```bash
cd C:\Users\AZURANY\Desktop\goldkaiser-bet
git init
git add .
git commit -m "GOLDKAISER landing page"
git branch -M main
git remote add origin https://github.com/KULLANICI/goldkaiser-bet.git
git push -u origin main
```

---
18+ · Demo amaçlıdır, gerçek bahis/ödeme yoktur.
