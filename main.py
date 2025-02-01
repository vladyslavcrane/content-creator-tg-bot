from datetime import datetime
import json
import asyncio
import logging
from logging.handlers import RotatingFileHandler
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, URLInputFile

from jobs import post_movie
from settings import BASE_DIR, MEDIA_DIR, CRON_SCHEDULE, MOOVIES_CHAT_USERNAME
from scheduler import setup_scheduler

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TG_BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# @dp.message(AutoPost())  # TODO: Implement AutoPost flag


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    user = message.from_user
    
    await message.answer(f"Hello, {html.bold(user.full_name)}!")


@dp.message(Command('postmovie'))
async def post_movie_handler(message: Message, bot) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """

    await post_movie(bot, MOOVIES_CHAT_USERNAME)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    jobs = [
        (post_movie, CRON_SCHEDULE['POST_MOVIE']),
    ]

    setup_scheduler(bot, jobs)

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = BASE_DIR / 'logfile.log'

    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
    asyncio.run(main())
