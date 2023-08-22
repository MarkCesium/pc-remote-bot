from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def pc_inline_kb() -> InlineKeyboardMarkup:
    y_btn = InlineKeyboardButton('yes', callback_data='yes')
    n_btn = InlineKeyboardButton('no', callback_data='no')
    keyboard = InlineKeyboardMarkup().add(y_btn).add(n_btn)
    return keyboard
