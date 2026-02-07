from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from loguru import logger

from src.bot.config import settings


class WhitelistMiddleware(BaseMiddleware):
    """Reject updates from users not in the ALLOWED_USERS whitelist."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not settings.allowed_users:
            return await handler(event, data)

        if isinstance(event, Update):
            user = None
            if event.message:
                user = event.message.from_user
            elif event.callback_query:
                user = event.callback_query.from_user

            if user and user.id not in settings.allowed_users:
                logger.warning(f"Blocked update from non-whitelisted user {user.id} ({user.username})")
                return None

        return await handler(event, data)
