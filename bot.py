"""Abror Baxtiyarovich · AB Media — Telegram bot.

Ishga tushirish:  python bot.py
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

import handlers
from config import cfg
from db import db
from middlewares import LangMiddleware
from texts import LANGS, T

log = logging.getLogger("ab_bot")


async def setup_profile(bot: Bot):
    """Buyruqlar menyusi va bot tavsifi — har bir til uchun alohida."""
    for lang in LANGS:
        code = None if lang == cfg.default_lang else lang
        cmds = [BotCommand(command=k, description=v) for k, v in T[lang]["cmd"].items()]
        try:
            await bot.set_my_commands(cmds, scope=BotCommandScopeDefault(), language_code=code)
            await bot.set_my_short_description(T[lang]["bot_short"][:120], language_code=code)
            await bot.set_my_description(T[lang]["bot_desc"][:512], language_code=code)
        except Exception as e:  # tavsif limiti / tarmoq — botni to'xtatmasin
            log.warning("Profil (%s) o'rnatilmadi: %s", lang, e)


async def main():
    if not cfg.token:
        sys.exit("BOT_TOKEN topilmadi. .env faylini to'ldiring (README'ga qarang).")
    await db.open()
    bot = Bot(cfg.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(LangMiddleware())
    dp.include_router(handlers.setup())
    await setup_profile(bot)
    me = await bot.get_me()
    log.info("Bot ishga tushdi: @%s", me.username)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(main())
