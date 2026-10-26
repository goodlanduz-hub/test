import logging
import re

from aiogram import Bot, F, Router, html
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandObject, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, User

import config
import db
import keyboards as kb
import texts

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(F.chat.type == "private")


class Form(StatesGroup):
    name = State()
    rooms = State()
    phone = State()


def parse_source(args: str | None) -> str:
    # t.me/bot?start=ads_1 -> "ads_1"; havolasiz kirganlar -> "direct"
    if args and re.fullmatch(r"[A-Za-z0-9_-]{1,64}", args):
        return args
    return "direct"


def normalize_phone(raw: str) -> str | None:
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 9:
        digits = "998" + digits
    if len(digits) == 12 and digits.startswith("998"):
        return "+" + digits
    return None


async def begin(message: Message, state: FSMContext, source: str) -> None:
    user = message.from_user
    db.touch(user.id, user.username, user.full_name, source)
    await state.clear()
    await state.set_state(Form.name)
    await message.answer(texts.ASK_NAME, reply_markup=ReplyKeyboardRemove())


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext) -> None:
    await begin(message, state, parse_source(command.args))


# --- 1. Ism ---

@router.message(Form.name, F.text)
async def got_name(message: Message, state: FSMContext) -> None:
    name = " ".join(message.text.split())
    if name.startswith("/") or not 2 <= len(name) <= 50:
        await message.answer(texts.BAD_NAME)
        return
    await state.update_data(name=name)
    await state.set_state(Form.rooms)
    await message.answer(texts.ASK_ROOMS.format(name=html.quote(name)), reply_markup=kb.rooms())


@router.message(Form.name)
async def bad_name(message: Message) -> None:
    await message.answer(texts.BAD_NAME)


# --- 2. Necha xonali ---

@router.callback_query(Form.rooms, F.data.startswith("rooms:"))
async def got_rooms(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.split(":", 1)[1]
    if value not in texts.ROOM_OPTIONS:
        await callback.answer()
        return
    label = texts.ROOM_LABEL.format(value)
    await state.update_data(rooms=label)
    await state.set_state(Form.phone)
    await callback.answer()
    # Tanlovni xabarning o'zida ko'rsatib, tugmalarni olib tashlaymiz
    await callback.message.edit_text(f"{callback.message.html_text}\n\n✅ <b>{label}</b>")
    await callback.message.answer(texts.ASK_PHONE, reply_markup=kb.contact())


@router.callback_query(F.data.startswith("rooms:"))
async def stale_rooms(callback: CallbackQuery) -> None:
    await callback.answer(texts.STALE_BUTTON, show_alert=True)


@router.message(Form.rooms)
async def bad_rooms(message: Message) -> None:
    await message.answer(texts.BAD_ROOMS, reply_markup=kb.rooms())


# --- 3. Telefon ---

@router.message(Form.phone, F.contact)
async def got_contact(message: Message, state: FSMContext, bot: Bot) -> None:
    contact = message.contact
    if contact.user_id != message.from_user.id:
        await message.answer(texts.NOT_OWN_CONTACT, reply_markup=kb.contact())
        return
    phone = contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone
    await finish(message, state, bot, phone)


@router.message(Form.phone, F.text)
async def got_phone_text(message: Message, state: FSMContext, bot: Bot) -> None:
    phone = normalize_phone(message.text)
    if not phone:
        await message.answer(texts.BAD_PHONE, reply_markup=kb.contact())
        return
    await finish(message, state, bot, phone)


@router.message(Form.phone)
async def bad_phone(message: Message) -> None:
    await message.answer(texts.BAD_PHONE, reply_markup=kb.contact())


# --- 4. Yakun: kanalga progrev tugmasi ---

async def finish(message: Message, state: FSMContext, bot: Bot, phone: str) -> None:
    data = await state.get_data()
    await state.clear()
    user = message.from_user
    db.complete(user.id, data["name"], data["rooms"], phone)

    await message.answer(
        texts.DONE.format(name=html.quote(data["name"])), reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(texts.CHANNEL_INVITE, reply_markup=kb.channel())
    await notify_admins(bot, user, data["name"], data["rooms"], phone)


async def notify_admins(bot: Bot, user: User, name: str, rooms: str, phone: str) -> None:
    if not config.ADMIN_CHAT_ID:
        return
    telegram = user.mention_html()
    if user.username:
        telegram += f" (@{user.username})"
    row = db.get(user.id)
    text = texts.LEAD_CARD.format(
        name=html.quote(name),
        rooms=rooms,
        phone=phone,
        telegram=telegram,
        source=html.quote(row["source"] if row else "direct"),
    )
    try:
        await bot.send_message(config.ADMIN_CHAT_ID, text)
    except TelegramAPIError:
        logger.exception("Arizani ADMIN_CHAT_ID=%s ga yuborib bo'lmadi", config.ADMIN_CHAT_ID)


# --- /start bosmasdan yozganlar ---

@router.message(StateFilter(None))
async def no_state(message: Message, state: FSMContext) -> None:
    if db.is_completed(message.from_user.id):
        await message.answer(texts.ALREADY_DONE, reply_markup=kb.channel())
        return
    await begin(message, state, "direct")
