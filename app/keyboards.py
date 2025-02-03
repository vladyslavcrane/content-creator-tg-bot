from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

admin_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        # [InlineKeyboardButton(text="Go to post", callback_data="go_to_post")],
        [InlineKeyboardButton(text="Edit", callback_data="edit_post")],
        # [InlineKeyboardButton(text="Delete", callback_data="remove_post")],
    ]
)
