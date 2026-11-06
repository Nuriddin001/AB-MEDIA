# 🎬 Abror Baxtiyarovich · AB Media — Telegram bot

Landing page'ning Telegram'dagi davomi. Bot "tungi suratga olish" uslubida qurilgan:
har bir bo'lim — kino kadri, navigatsiya bitta xabar ichida kadrma-kadr almashadi
(chat xabarlar lentasiga aylanmaydi).

## Ichida nima bor

| Bo'lim | Nima qiladi |
|---|---|
| 🌐 Til tanlash | O'zbekcha / Русский / English — kinoxlopushka kadrida |
| 👤 Abror haqida | Kim, nima bilan shug'ullanadi, fokus, mijozlar + ijtimoiy tarmoq tugmalari |
| 🎞 Ishlar | 5 ta keys karuseli (◀ SC 02/05 ▶): vazifa, konsepsiya, Abror qismi, titrlar. Har bir keys uchun alohida "titr-kadr" |
| 🛠 Xizmatlar | A — to'liq sikl, B — prodyuserlik nazorati; har biridan to'g'ridan-to'g'ri arizaga |
| 🧭 Mijoz yo'li | Obyektiv fokus-shkalasi: 5 bosqichni "burab" ko'rasiz, Tanilish va Ishonch — Abrorning fokusi |
| 🎬 Ish jarayoni | Montaj taymlayni: playhead 5 bosqich bo'ylab yuradi |
| 🧪 Brend diagnostikasi | 6 savollik test ("TAKE 01…06") → Tanilish % va Ishonch % kartasi + tavsiya → ariza |
| 📝 Ariza | Ism → telefon (bitta tugma bilan) → email (ixtiyoriy). Yakunda "Snyat!" kadri, adminga to'liq ma'lumot |
| 🌍 Sayt | `SITE_URL` berilsa, landing page Telegram ichida Mini App bo'lib ochiladi |

Adminga ariza bilan birga keladi: qaysi formatni tanlagani, qaysi keysdan kelgani,
diagnostika natijasi, tili va **manbasi** (deep-link orqali).

## Ishga tushirish (5 daqiqa)

1. **Bot yarating:** Telegram'da [@BotFather](https://t.me/BotFather) → `/newbot` → token oling.
   Bot rasmi uchun `/setuserpic` ga `assets/portrait.jpg` ni yuboring.
2. **ID'ingizni bilib oling:** [@userinfobot](https://t.me/userinfobot) ga yozing.
3. **Sozlang:**
   ```bash
   cp .env.example .env
   # .env ichida BOT_TOKEN va ADMIN_IDS ni to'ldiring
   ```
4. **Ishga tushiring** (Python 3.10+):
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```
   Bot birinchi ishga tushganda buyruqlar menyusi va bot tavsifini 3 tilda o'zi o'rnatadi.

### Serverda doimiy ishlashi uchun

**Docker:**
```bash
docker build -t ab-bot .
docker run -d --restart=always --env-file .env -v $(pwd)/data:/app/data --name ab-bot ab-bot
```

**systemd** (`/etc/systemd/system/ab-bot.service`):
```ini
[Unit]
Description=AB Media bot
After=network.target

[Service]
WorkingDirectory=/opt/ab_media_bot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```
`sudo systemctl enable --now ab-bot`

Railway / Render kabi xizmatlarda ham ishlaydi: start buyrug'i `python bot.py`, o'zgaruvchilar `.env.example` dagidek.

## Landing page bilan bog'lash (deep-link)

Saytdagi tugmalarga shu havolalarni qo'ying (`BOT` o'rniga bot username'i):

| Havola | Nima ochiladi |
|---|---|
| `https://t.me/BOT?start=lead` | Darhol ariza formasi |
| `https://t.me/BOT?start=quiz` | Darhol brend diagnostikasi |
| `https://t.me/BOT?start=works` | Ishlar karuseli |
| `https://t.me/BOT?start=instagram` | Bosh menyu, manba = instagram |

`start=` dan keyingi har qanday so'z "manba" bo'lib yoziladi — `/stats` da qaysi
kanal qancha odam olib kelganini ko'rasiz (masalan `start=reels_nov`, `start=site`).

## Admin buyruqlari

Faqat `ADMIN_IDS` dagi foydalanuvchilar uchun:

- `/admin` — yordam va deep-link'lar
- `/stats` — foydalanuvchilar, arizalar, diagnostika o'rtachasi, tillar, manbalar
- `/leads` — barcha arizalar CSV faylda (Excel'da ochiladi)
- `/broadcast` — istalgan xabarga (matn, rasm, video) **reply** qilib yozing → barcha foydalanuvchilarga ketadi

## Kontentni o'zgartirish

- **Matnlar** — hammasi `texts.py` da, 3 tilda. Keys qo'shish uchun `CASES` ro'yxatiga yangi element qo'shing.
- **Rasmlar** — `assets/portrait.jpg` (bosh ekran) va `assets/stage.jpg` ("Abror haqida"). Shu nomlar bilan almashtiring.
- **Kartochkalar dizayni** — `render.py`. Biror narsani o'zgartirsangiz, fayl boshidagi `RENDER_VERSION` ni bittaga oshiring — bot yangi rasmlarni qayta yuklaydi.
- **Yangi til** (masalan ispan yoki arab) — `texts.py` da `T["es"]`, har bir keysga `"es"` matni va `LANGS` ga `"es"`.

## Texnik tuzilma

```
bot.py            ishga tushirish, buyruqlar menyusi, bot tavsifi
config.py         .env sozlamalari
texts.py          barcha matnlar (uz/ru/en) va keyslar
render.py         kadr-kartochkalarni chizish (Pillow, 1280×720)
ui.py             ekranlar va "bitta xabarda navigatsiya"
db.py             SQLite: foydalanuvchilar, arizalar, test natijalari, rasm keshi
middlewares.py    foydalanuvchi tilini aniqlash
handlers/         menu · quiz · lead · admin
assets/           fotolar va shriftlar (Sofia Sans Extra Condensed, Golos Text, JetBrains Mono — OFL)
```

Kartochkalar birinchi marta ko'rsatilganda chiziladi (~0,1 s) va Telegram `file_id`
si bazaga yoziladi — keyingi safar rasm qayta yuklanmaydi, ekranlar bir zumda almashadi.
Faqat diagnostika natijasi har safar yangidan chiziladi (unda shaxsiy foizlar bor).
