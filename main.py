import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import admin
import config
import db
import handlers


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    if not config.BOT_TOKEN:
        raise SystemExit("BOT_TOKEN .env faylida ko'rsatilmagan")
    if not config.CHANNEL_URL:
        raise SystemExit("CHANNEL_URL .env faylida ko'rsatilmagan")

    db.init(config.DB_PATH)

    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    # Tartib muhim: admin buyruqlari foydalanuvchi oqimidan oldin tekshiriladi
    dp.include_routers(admin.public_router, admin.router, handlers.router)

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
