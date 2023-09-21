from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def steam_kb(games) -> ReplyKeyboardMarkup:
    back_btn = KeyboardButton("Назад↩")
    close_btn = KeyboardButton('Закрыть❌')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   input_field_placeholder="Открыть...",
                                   row_width=3)
    for game in games:
        if game['run']:
            keyboard.add(KeyboardButton(f"/close {game['name']}"))
        else:
            keyboard.add(KeyboardButton(f"/play {game['name']}"))

    return keyboard.add(back_btn, close_btn)
