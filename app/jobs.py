import logging
from typing import Dict, Optional
from aiogram import Bot

from aiogram.types import Message, URLInputFile, User
from app.templates import get_rendered_template
from app.api import fetch_post_movie_data
from app.parser import parse_imdb_urls

log = logging.getLogger(__name__)


async def post_movie(bot: Bot, chat_id: int, user: Optional[User] = None) -> Dict:
    # image = URLInputFile(openai_response["poster_image_url"])
    data = fetch_post_movie_data()

    try:
        data.update(**parse_imdb_urls(data["imdb_link"]))
        data["genres"] = ", ".join(g.lower() for g in data["genres"])
        data["director"] = (
            data["director"]
            if isinstance(data["director"], str)
            else ", ".join(data["director"])
        )
        data["actors"] = ", ".join(data["actors"])

        caption = get_rendered_template("post_movie.html", data)
    
        message = await bot.send_photo(chat_id=chat_id, photo=data["poster_url"], caption=caption)
        
        if user:
            return await message.forward(user.id)
    except Exception as e:
        await bot.send_message(text='Post failed', chat_id=user.id)
        log.exception(f"Error posting movie: {e}")
