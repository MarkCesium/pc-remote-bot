from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from config import TOKEN_BOT
from keyboards import start_kb

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Приветус!", reply_markup=start_kb())


@dp.message_handler(Text(equals="Сфоткай📸"))
async def take_screenshot(message):
    pass


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
