from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from src.bot.i18n import TEXTS, get_text
from src.bot.keyboards import language_keyboard, main_keyboard, parameter_keyboard
from src.bot.scheduler import (
    _broadcast_walk,
    cancel_walk_timer,
    schedule_walk_finalization,
)
from src.database import crud
from src.database.session import async_session

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command - show language selection."""
    logger.info(f"User {message.from_user.id} ({message.from_user.username}) started bot")
    await message.answer(
        text=get_text("welcome", "ru") + "\n" + get_text("welcome", "en"),
        reply_markup=language_keyboard(),
    )


@router.message(F.text == "🇷🇺 Русский")
async def set_russian(message: Message) -> None:
    """Set Russian language."""
    await _set_language(message, "ru")


@router.message(F.text == "🇬🇧 English")
async def set_english(message: Message) -> None:
    """Set English language."""
    await _set_language(message, "en")


async def _set_language(message: Message, lang: str) -> None:
    """Set user language and show main keyboard."""
    async with async_session() as session:
        user = await crud.get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
        )
        await crud.set_user_language(session, user.id, lang)
        logger.info(f"User {message.from_user.id} set language to {lang}")

    await message.answer(
        text=get_text("language_set", lang),
        reply_markup=main_keyboard(lang),
    )


@router.message(F.text.in_({TEXTS["ru"]["walk_button"], TEXTS["en"]["walk_button"]}))
async def start_walk(message: Message) -> None:
    """Handle walk button press - create walk and show parameter keyboard."""
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
        if user is None:
            logger.warning(f"Unregistered user {message.from_user.id} tried to start walk")
            await message.answer("Please /start first")
            return

        lang = user.language

        # Check for existing pending walk
        existing_walk = await crud.get_pending_walk(session, user.id)
        if existing_walk:
            logger.debug(f"User {user.telegram_id} has existing pending walk {existing_walk.id}")
            await message.answer(
                text=get_text("walk_started", lang),
                reply_markup=parameter_keyboard(lang),
            )
            return

        # Create new walk
        walk = await crud.create_walk(session, user.id)
        logger.info(f"User {user.telegram_id} ({user.username}) started walk {walk.id}")

        # Schedule auto-finalization
        await schedule_walk_finalization(user.id, walk.id)

        await message.answer(
            text=get_text("walk_started", lang),
            reply_markup=parameter_keyboard(lang),
        )


@router.message(F.text.in_({TEXTS["ru"]["didnt_poop"], TEXTS["en"]["didnt_poop"]}))
async def toggle_didnt_poop(message: Message) -> None:
    """Toggle 'didn't poop' parameter."""
    await _toggle_param(message, "didnt_poop")


@router.message(F.text.in_({TEXTS["ru"]["long_walk"], TEXTS["en"]["long_walk"]}))
async def toggle_long_walk(message: Message) -> None:
    """Toggle 'long walk' parameter."""
    await _toggle_param(message, "long_walk")


async def _toggle_param(message: Message, param: str) -> None:
    """Toggle a walk parameter."""
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
        if user is None:
            await message.answer("Please /start first")
            return

        lang = user.language
        walk = await crud.get_pending_walk(session, user.id)

        if walk is None:
            logger.debug(f"User {message.from_user.id} tried to toggle param without active walk")
            await message.answer(
                text=get_text("no_active_walk", lang),
                reply_markup=main_keyboard(lang),
            )
            return

        # Toggle the parameter
        if param == "didnt_poop":
            new_value = not walk.didnt_poop
            await crud.update_walk_params(session, walk.id, didnt_poop=new_value)
        elif param == "long_walk":
            new_value = not walk.long_walk
            await crud.update_walk_params(session, walk.id, long_walk=new_value)

        logger.debug(f"User {user.telegram_id} toggled {param}={new_value} for walk {walk.id}")

        await message.answer(
            text=get_text("param_toggled", lang),
            reply_markup=parameter_keyboard(lang),
        )


@router.message(F.text.in_({TEXTS["ru"]["send"], TEXTS["en"]["send"]}))
async def send_walk(message: Message, bot: Bot) -> None:
    """Finalize and send walk notification."""
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
        if user is None:
            await message.answer("Please /start first")
            return

        lang = user.language
        walk = await crud.get_pending_walk(session, user.id)

        if walk is None:
            logger.debug(f"User {message.from_user.id} tried to send without active walk")
            await message.answer(
                text=get_text("no_active_walk", lang),
                reply_markup=main_keyboard(lang),
            )
            return

        # Cancel the timer
        await cancel_walk_timer(user.id)

        # Finalize the walk
        walk = await crud.finalize_walk(session, walk.id)
        logger.info(
            f"User {user.telegram_id} ({user.username}) finalized walk {walk.id} "
            f"[didnt_poop={walk.didnt_poop}, long_walk={walk.long_walk}]"
        )

        # Send confirmation
        await message.answer(
            text=get_text("walk_sent", lang),
            reply_markup=main_keyboard(lang),
        )

        # Broadcast to all users
        await _broadcast_walk(session, walk, user)
