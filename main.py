from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import os
import pyautogui
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import TOKEN_BOT
from keyboards import start_kb, chrome_kb

storage = MemoryStorage()
bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)


class Remote(StatesGroup):
    chrome = State()
    spotify = State()
    steam = State()
    pc = State()


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message):
    await message.reply("Приветус!", reply_markup=start_kb())


@dp.message_handler(Text(equals="Сфоткай📸"))
async def take_screenshot(message):
    await message.answer(text='Не шевелись...')
    pyautogui.screenshot('img/screenshot.png')
    screenshot = open("img/screenshot.png", 'rb')
    await bot.send_photo(message.chat.id, photo=screenshot, caption="Принимай🌅")


# CHROME BLOCK >>>>>>>>>>>

@dp.message_handler(Text(equals="Chrome🌍"))
async def open_chrome(message: types.Message):
    await message.answer("Что открывать будем?", reply_markup=chrome_kb())
    os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")
    await Remote.chrome.set()


@dp.message_handler(Text(equals="YouTube📺"), state=Remote.chrome)
async def open_yt(message: types.Message):
    pass


@dp.message_handler(Text(equals="Telegram💬"), state=Remote.chrome)
async def open_yt(message: types.Message):
    pass


@dp.message_handler(Text(equals="Найти...🔍"), state=Remote.chrome)
async def open_yt(message: types.Message):
    pass


@dp.message_handler(Text(equals=("Назад❌")), state=Remote.chrome)
async def all_chrome(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Chrome закрыт", reply_markup=start_kb())


# CHROME BLOCK <<<<<<<<<<


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
