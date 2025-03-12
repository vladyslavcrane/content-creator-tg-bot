from abc import ABC
import json
import logging

from aiogram import Bot
from aiogram.types import Message, URLInputFile, User
from aiogram.utils.media_group import MediaGroupBuilder

from app.ui.templates import get_rendered_template
from app.api.client import ContentClient
from app.db.mongo.documents import Moovie
from app.api.parser import parse_imdb_urls
from app.prompts.loaders import FilePromptLoader
from app.ui.keyboards import admin_inline


log = logging.getLogger(__name__)

class PostManager(ABC):
    
    def make_post(self, bot: Bot, chat_id: int):
        pass


class MooviePostManager(PostManager):
    model = Moovie
    template = "post_random_movie.html"

    def __init__(self, content_client: ContentClient):
        self.content_client = content_client

    def get_content(self, prompt):
        content = self.content_client.get_content(prompt)
        content = json.loads(content)
        # self.format_content(content)
        return content

    async def _get_extra_content(self, content):
        media_urls = await parse_imdb_urls(content["imdb_link"])
        return {'media_urls': media_urls}

    async def _create_media_group(self, content):
        album_builder = MediaGroupBuilder()
        extra_content = await self._get_extra_content(content)
        for media_url in extra_content["media_urls"]:
            try:
                media_file = URLInputFile(media_url)
                album_builder.add_photo(media_file)
            except:
                log.info(f'failed to add photo `{media_url}`')
                pass
        
        caption = get_rendered_template(self.template, {'obj': content})
        album_builder.caption = caption
        return album_builder.build()


    async def make_post(self, prompt: str, bot: Bot, chat_id: int):
        # get content for a post
        content = self.get_content(prompt)

        # create and save model with content data
        obj = self.model(**content)
        await obj.insert()

        # create tg post
        media_group = await self._create_media_group(content)

        # post
        log.info(f'Posting with data:\n{content}')
        await bot.send_media_group(chat_id=chat_id, media=media_group)
