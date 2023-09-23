from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_kb() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton('Сфоткай📸')
    button_2 = KeyboardButton('Chrome🌍')
    button_3 = KeyboardButton('Spotify🎧')
    button_4 = KeyboardButton('Steam🎮')
    button_5 = KeyboardButton('Спим💤')
    button_6 = KeyboardButton('Громкость🔊')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).insert(button_1).insert(button_2).insert(button_3).insert(button_4).insert(button_5).insert(button_6)
    return keyboard
