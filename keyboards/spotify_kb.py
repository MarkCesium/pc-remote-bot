from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def spotify_kb() -> ReplyKeyboardMarkup:
    back_btn = KeyboardButton("Назад↩")
    close_btn = KeyboardButton('Закрыть❌')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(back_btn).add(close_btn)

    return keyboard