"""Har bir update'ga foydalanuvchi tilini (`lang`) qo'shadi."""
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from config import cfg
from db import db
from texts import LANGS


class LangMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: dict[str, Any]) -> Any:
        user: User | None = data.get("event_from_user")
        lang = None
        if user:
            lang = await db.get_lang(user.id)
        data["has_lang"] = lang in LANGS
        if lang not in LANGS:
            code = (user.language_code or "")[:2] if user else ""
            lang = code if code in LANGS else cfg.default_lang
        data["lang"] = lang
        return await handler(event, data)
