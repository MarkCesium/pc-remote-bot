from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
