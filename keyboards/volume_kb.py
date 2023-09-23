from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def volume_kb() -> InlineKeyboardMarkup:
    v100_btn = InlineKeyboardButton('100%', callback_data='1')
    v75_btn = InlineKeyboardButton('75%', callback_data='0.75')
    v50_btn = InlineKeyboardButton('50%', callback_data='0.5')
    v25_btn = InlineKeyboardButton('25%', callback_data='0.25')
    v0_btn = InlineKeyboardButton('0%', callback_data='0')

    keyboard = InlineKeyboardMarkup(resize_keyboard=True).insert(v100_btn).insert(v75_btn).insert(v50_btn).insert(
        v25_btn).insert(v0_btn)

    return keyboard
