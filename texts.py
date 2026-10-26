# Bot matnlari. Matnni o'zgartirish uchun faqat shu faylni tahrirlang.
# HTML formatlash ishlaydi: <b>qalin</b>, <i>kursiv</i>.

ASK_NAME = (
    "Assalomu alaykum! 👋\n\n"
    "Sizga mos xonadonni tanlashda yordam beramiz.\n"
    "Iltimos, <b>ismingizni</b> yozing:"
)
BAD_NAME = "Iltimos, ismingizni matn ko'rinishida yozing (2–50 belgi)."

ASK_ROOMS = "Tanishganimdan xursandman, <b>{name}</b>! 😊\n\nNecha xonalik xonadon olmoqchisiz?"
BAD_ROOMS = "Iltimos, quyidagi tugmalardan birini tanlang 👇"
# Tugmalar: qiymat -> "{qiymat} xonali"
ROOM_OPTIONS = ["1", "2", "3", "4+"]
ROOM_LABEL = "{} xonali"

ASK_PHONE = (
    "Ajoyib! Endi <b>telefon raqamingizni</b> yuboring 👇\n\n"
    "Pastdagi «📱 Raqamni yuborish» tugmasini bosing "
    "yoki raqamni <code>+998 90 123 45 67</code> ko'rinishida yozing."
)
CONTACT_BUTTON = "📱 Raqamni yuborish"
PHONE_PLACEHOLDER = "+998 90 123 45 67"
BAD_PHONE = (
    "Raqam noto'g'ri ko'rinishda. Tugmani bosing yoki "
    "<code>+998 90 123 45 67</code> ko'rinishida yozing."
)
NOT_OWN_CONTACT = "Iltimos, o'zingizning raqamingizni yuboring — pastdagi tugmani bosing 👇"

DONE = (
    "✅ Rahmat, <b>{name}</b>! Arizangiz qabul qilindi.\n"
    "Mutaxassisimiz tez orada siz bilan bog'lanadi."
)
CHANNEL_INVITE = (
    "Hozircha kanalimizga obuna bo'ling — u yerda yangi loyihalar, "
    "narxlar va faqat obunachilar uchun maxsus takliflar 👇"
)
CHANNEL_BUTTON = "📢 Kanalga o'tish"

ALREADY_DONE = (
    "Arizangiz allaqachon qabul qilingan ✅\n"
    "Ma'lumotlarni yangilash uchun /start bosing.\n\n"
    "Kanalimizni kuzatib boring 👇"
)
STALE_BUTTON = "Qaytadan boshlash uchun /start bosing"

# Adminlarga boradigan xabar
LEAD_CARD = (
    "🆕 <b>Yangi ariza</b>\n\n"
    "👤 Ism: <b>{name}</b>\n"
    "🏠 Xonadon: <b>{rooms}</b>\n"
    "📞 Telefon: <code>{phone}</code>\n"
    "💬 Telegram: {telegram}\n"
    "📣 Manba: <code>{source}</code>"
)
