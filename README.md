# Ko'chmas mulk lid-bot (Telegram Ads → bot → kanal)

Reklamadan kelgan odamdan ariza yig'ib, uni progrev kanalga yo'naltiradigan Telegram bot.

## Bot qanday ishlaydi

1. Odam Telegram Ads reklamasini bosadi → botga tushadi → **START** bosadi
2. Bot darhol ismini so'raydi
3. **Necha xonalik** xonadon olmoqchiligini so'raydi (tugmalar: 1 / 2 / 3 / 4+)
4. **Telefon raqamini** so'raydi («📱 Raqamni yuborish» tugmasi yoki qo'lda yozish)
5. Rahmat aytadi va **«📢 Kanalga o'tish»** tugmasini beradi (progrev kanal)
6. Ariza darhol admin guruhga yuboriladi: ism, xonadon, telefon, Telegram profil, qaysi reklamadan kelgani

> Telegram qoidasiga ko'ra bot odamga birinchi bo'lib yoza olmaydi — START tugmasini
> foydalanuvchi o'zi bosishi kerak. START bosilgandan keyin hammasi avtomatik.
> Agar odam START o'rniga biror narsa yozsa ham, bot so'rovnomani o'zi boshlaydi.

## O'rnatish

1. [@BotFather](https://t.me/BotFather) da bot yarating va tokenni oling.
2. Python 3.10+ o'rnating, so'ng:

   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. `.env` faylini to'ldiring:

   | O'zgaruvchi     | Nima                                                         |
   |-----------------|--------------------------------------------------------------|
   | `BOT_TOKEN`     | BotFather bergan token                                       |
   | `CHANNEL_URL`   | Progrev kanal havolasi, masalan `https://t.me/mening_kanalim` |
   | `ADMIN_CHAT_ID` | Arizalar tushadigan guruh ID si                              |
   | `ADMIN_IDS`     | `/stats` va `/export` ishlata oladiganlar ID si (vergul bilan) |

   **ID larni qanday bilish mumkin:** botni ishga tushiring, uni arizalar guruhiga qo'shing
   va guruhda `/id` yozing — bot guruh ID sini va sizning ID ingizni ko'rsatadi.

4. Ishga tushirish:

   ```bash
   python main.py
   ```

## Telegram Ads sozlash

Har bir reklama uchun alohida havola bering — shunda qaysi reklama ko'proq ariza
olib kelayotganini ko'rasiz:

```
https://t.me/SizningBot?start=ads_1
https://t.me/SizningBot?start=ads_2
https://t.me/SizningBot?start=story_oktabr
```

`start=` dan keyingi qism (lotin harflari, raqam, `_` va `-`, 64 belgigacha) arizada
«Manba» sifatida ko'rinadi. Havolasiz kirganlar `direct` deb yoziladi.

## Kanallardagi zakup va CRM teglari

Boshqa kanallardan sotib olingan reklama uchun havola `zakup_` bilan boshlanadi,
undan keyin kanal nomi (bo'sh joy o'rniga `_`):

```
https://t.me/SizningBot?start=zakup_Vodiy_Bozor
```

Har bir arizada CRM uchun teglar avtomatik chiqadi (admin xabarida va `/export` da):

| Havola                     | Teglar                                          |
|----------------------------|-------------------------------------------------|
| `zakup_Vodiy_Bozor`        | лид, ТГ, Vodiy Bozor, закупка рекламы           |
| boshqa hammasi (`ads_1`, havolasiz ham) | лид, лид с телеграм ads, telegram ads |

Teglarni o'zgartirish: `texts.py` dagi `TAGS_TG_ADS` va `TAGS_ZAKUP`.

## Admin buyruqlari

- `/stats` — nechta odam kirdi, nechtasi ariza qoldirdi, konversiya, har bir reklama bo'yicha
- `/export` — barcha arizalar CSV fayl ko'rinishida (Excel'da ochiladi)
- `/id` — chat ID ni ko'rsatadi (hamma uchun)

## Matnlarni o'zgartirish

Botning barcha matnlari va xonadon variantlari `texts.py` faylida. Masalan, «5+ xonali»
qo'shish uchun:

```python
ROOM_OPTIONS = ["1", "2", "3", "4", "5+"]
```

## Serverda doimiy ishlatish (Ubuntu, systemd)

`/etc/systemd/system/leadbot.service`:

```ini
[Unit]
Description=Lead bot
After=network-online.target

[Service]
WorkingDirectory=/opt/leadbot
ExecStart=/opt/leadbot/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now leadbot
sudo journalctl -u leadbot -f   # loglarni ko'rish
```

## Fayllar

| Fayl           | Vazifasi                                         |
|----------------|--------------------------------------------------|
| `main.py`      | Botni ishga tushiradi                            |
| `handlers.py`  | So'rovnoma: ism → xonadon → telefon → kanal      |
| `admin.py`     | `/stats`, `/export`, `/id`                       |
| `texts.py`     | Barcha matnlar                                   |
| `keyboards.py` | Tugmalar                                         |
| `db.py`        | Arizalarni SQLite bazada saqlash (`leads.db`)    |
| `config.py`    | `.env` sozlamalarini o'qish                      |
