import csv
import io
from datetime import datetime

from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

import config
import db

# /id — sozlash paytida chat ID ni bilish uchun, hamma uchun ochiq
public_router = Router()

router = Router()
router.message.filter(F.from_user.id.in_(config.ADMIN_IDS))


@public_router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(
        f"Chat ID: <code>{message.chat.id}</code>\n"
        f"Sizning ID: <code>{message.from_user.id}</code>"
    )


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    total, completed, by_source = db.stats()
    conversion = round(completed * 100 / total, 1) if total else 0
    lines = [
        f"👥 Botga kirganlar: <b>{total}</b>",
        f"✅ Ariza qoldirganlar: <b>{completed}</b>",
        f"📈 Konversiya: <b>{conversion}%</b>",
    ]
    if by_source:
        lines += ["", "📣 Manbalar bo'yicha (kirgan → ariza):"]
        lines += [
            f"• <code>{html.quote(r['source'])}</code>: {r['started']} → {r['completed']}"
            for r in by_source
        ]
    await message.answer("\n".join(lines))


@router.message(Command("export"))
async def cmd_export(message: Message) -> None:
    rows = db.all_leads()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(
        ["user_id", "username", "telegram_ism", "manba", "ism", "xonadon", "telefon",
         "kirgan_vaqt", "ariza_vaqt"]
    )
    for r in rows:
        writer.writerow(
            [r["user_id"], r["username"] or "", r["tg_name"], r["source"], r["name"] or "",
             r["rooms"] or "", r["phone"] or "", r["started_at"], r["completed_at"] or ""]
        )
    # utf-8-sig: Excel o'zbekcha/ruscha harflarni to'g'ri ochishi uchun
    data = buf.getvalue().encode("utf-8-sig")
    filename = f"leads_{datetime.now(db.TZ):%Y-%m-%d}.csv"
    await message.answer_document(
        BufferedInputFile(data, filename=filename), caption=f"Jami: {len(rows)} ta"
    )
