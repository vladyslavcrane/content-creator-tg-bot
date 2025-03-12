from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

admin_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Edit", callback_data="edit_post")],
    ]
)
