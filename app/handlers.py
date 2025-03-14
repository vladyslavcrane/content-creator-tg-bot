from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message, BotCommand

from app.api.client import OpenAIContentClient
from app.config import config
from app.post_managers import MooviePostManager
from app.prompts.loaders import FilePromptLoader

router = Router()


async def set_default_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(
                command="postrandommovie",
                description="Post random moovie",
            )
        ]
    )


@router.message(Command("postrandommovie"))
async def post_random_movie_handler(message: Message, bot) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    user = message.from_user

    if not user.username == config.OWNER_USERNAME:
        await message.answer(f"You can't perform this action.")
        return

    await message.answer(f"Posting...")

    post_manager = MooviePostManager(OpenAIContentClient())
    prompt = FilePromptLoader.get_prompt(
        f"{config.BASE_DIR}/prompts/random_moovie.txt"
    )
    await post_manager.make_post(prompt, bot, config.MOOVIES_CHAT_USERNAME)
