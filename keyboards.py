from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import texts


def rooms() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for value in texts.ROOM_OPTIONS:
        builder.button(text=texts.ROOM_LABEL.format(value), callback_data=f"rooms:{value}")
    builder.adjust(2)
    return builder.as_markup()


def contact() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=texts.CONTACT_BUTTON, request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=texts.PHONE_PLACEHOLDER,
    )


def channel() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.CHANNEL_BUTTON, url=config.CHANNEL_URL)
    return builder.as_markup()
