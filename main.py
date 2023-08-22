from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import os
import pyautogui

from config import TOKEN_BOT
from keyboards import start_kb

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Приветус!", reply_markup=start_kb())


@dp.message_handler(Text(equals="Сфоткай📸"))
async def take_screenshot(message):
    await message.answer(text='Не шевелись...')
    pyautogui.screenshot('.img/screenshot.png')
    s = open(r".img/screenshot.png", 'rb')
    await bot.send_photo(message.chat.id, photo=s, caption="Принимай🌅")


@dp.message_handler(Text(equals="Chrome🌍"))
async def open_chrome(message):
    pass


@dp.message_handler(Text(equals="Spotify🎧"))
async def open_spotify(message):
    pass


@dp.message_handler(Text(equals="Steam🎮"))
async def open_steam(message):
    pass


@dp.message_handler(Text(equals="Гаси ебало💤"))
async def os_shutdown(message: types.Message):
    await message.answer(text='бб')
    os.system("shutdown -s -t 0")


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
