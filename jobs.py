from aiogram import Bot

from aiogram.types import Message, URLInputFile
from templates import get_rendered_template
from api import get_completion
from parser import parse_imdb_urls


async def post_movie(bot: Bot, user_id: int) -> None:
    # image = URLInputFile(openai_response["poster_image_url"])
    data = get_completion()
    
    data.update(**parse_imdb_urls(data["imdb_link"]))
    data["genres"] = ", ".join(g.lower() for g in data["genres"])
    data["director"] = (
        data["director"]
        if isinstance(data["director"], str)
        else ", ".join(data["director"])
    )
    data['actors'] = ', '.join(data['actors'])

    caption = get_rendered_template("post_movie.html", data)

    await bot.send_photo(chat_id=user_id, photo=data["poster_url"], caption=caption)
