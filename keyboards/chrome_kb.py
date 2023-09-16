from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def chrome_kb() -> ReplyKeyboardMarkup:
    youtube_btn = KeyboardButton("YouTube📺")
    tg_btn = KeyboardButton("Telegram💬")
    query_btn = KeyboardButton("Найти...🔍")
    back_btn = KeyboardButton("Назад↩")
    close_btn = KeyboardButton('Закрыть❌')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   input_field_placeholder="Открыть...",
                                   row_width=2).add(youtube_btn, tg_btn, query_btn, back_btn)

    return keyboard
