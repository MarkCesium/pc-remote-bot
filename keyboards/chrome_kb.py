from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def chrome_kb() -> ReplyKeyboardMarkup:
    youtube_btn = KeyboardButton("/yt")
    tg_btn = KeyboardButton("/tg")
    ds_btn = KeyboardButton("/ds")
    back_btn = KeyboardButton("Назад↩")
    close_btn = KeyboardButton('Закрыть❌')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   input_field_placeholder="Открыть...",
                                   row_width=3).add(youtube_btn, tg_btn, ds_btn, back_btn, close_btn)

    return keyboard
