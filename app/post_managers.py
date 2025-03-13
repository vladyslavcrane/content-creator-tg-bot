from abc import ABC, abstractmethod
import json
import logging
from typing import List

from aiogram import Bot
from aiogram.types import URLInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from app.ui.templates import get_rendered_template
from app.api.client import ContentClient
from app.db.mongo.documents import Moovie
from app.api.parser import parse_imdb_pictures_urls


log = logging.getLogger(__name__)


class PostManager(ABC):

    @abstractmethod
    def make_post(self, prompt: str, bot: Bot, chat_id: int) -> None:
        pass


class MooviePostManager(PostManager):
    model = Moovie
    template = "post_random_movie.html"

    def __init__(self, content_client: ContentClient) -> None:
        self.content_client = content_client

    def get_content(self, prompt: str) -> None:
        content = self.content_client.get_content(prompt)
        content = json.loads(content)
        return content

    async def _search_pictures_in_web(self, content: dict) -> List[str]:
        imdb_moovie_url = content["imdb_link"]
        media_urls = await parse_imdb_pictures_urls(imdb_moovie_url)
        return media_urls

    async def _create_media_group(self, content):
        album_builder = MediaGroupBuilder()
        media_urls = await self._search_pictures_in_web(content)
        for media_url in media_urls:
            try:
                media_file = URLInputFile(media_url)
                album_builder.add_photo(media_file)
            except:
                log.info(f"failed to add photo `{media_url}`")
                pass

        caption = get_rendered_template(self.template, {"obj": content})
        album_builder.caption = caption
        return album_builder.build()

    async def make_post(self, prompt: str, bot: Bot, chat_id: int) -> None:
        # get content for a post
        content = self.get_content(prompt)

        # create and save model with content data
        obj = self.model(**content)
        await obj.insert()

        # create tg post
        media_group = await self._create_media_group(content)

        # post
        log.info(f"Posting with data:\n{content}")
        await bot.send_media_group(chat_id=chat_id, media=media_group)
