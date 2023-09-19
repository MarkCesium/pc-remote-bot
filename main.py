import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import os
import pyautogui
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import TOKEN_BOT
from keyboards import *
import webbrowser as wb

storage = MemoryStorage()
bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)


class Chrome(StatesGroup):
    base = State()


class Steam(StatesGroup):
    base = State()
    # TODO: Обдумать, как сделать состояния разных игр.


class Remote(StatesGroup):
    base = State()
    spotify = State()
    pc = State()


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    await message.reply("Приветус!", reply_markup=start_kb())
    await state.set_data({
        'chrome': False
    })


@dp.message_handler(Text(equals="Сфоткай📸"))
async def take_screenshot(message):
    await message.answer(text='Не шевелись...')
    pyautogui.screenshot('img/screenshot.png')
    screenshot = open("img/screenshot.png", 'rb')
    await bot.send_photo(message.chat.id, photo=screenshot, caption="Принимай🌅")


# CHROME BLOCK >>>>>>>>>>>

@dp.message_handler(Text(equals="Chrome🌍"), state='*')
async def open_chrome(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await Chrome.base.set()
    if data['chrome']:
        await message.answer("Уже открыт!", reply_markup=chrome_kb())
        wb.open_new_tab('https://www.google.com')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'w')
    else:
        await message.answer(
            '''Chrome открыт!
<b>/yt</b> [запрос] - открыть YouTube
<b>/tg</b> - открыть Telegram
<b>/search</b> [запрос] - воспользоваться поисковиком
<b>/ds</b> - открыть Discord''',
            parse_mode='HTML',
            reply_markup=chrome_kb()
        )
        await state.update_data({
            'chrome': True
        })
        wb.open_new('https://')


@dp.message_handler(commands=['tg'], state=Chrome.base)
async def open_yt(message: types.Message):
    wb.open_new_tab('https://web.telegram.org/a/')


@dp.message_handler(commands=['search'], state=Chrome.base)
async def open_yt(message: types.Message):
    query = message.text.replace(' ', '+')
    wb.open_new_tab(f'https://www.google.com/search?q={query[8:]}')
    await message.answer('Готово!', reply_markup=chrome_kb())
    await Chrome.base.set()


@dp.message_handler(commands=['ds'], state=Chrome.base)
async def open_ds(message: types.Message):
    wb.open_new_tab('https://discord.com/channels/@me')


@dp.message_handler(commands=['yt'], state=Chrome.base)
async def open_ds(message: types.Message):
    if len(message.text) > 3:
        query = message.text.replace(' ', '+')
        wb.open_new_tab(f'https://www.youtube.com/results?search_query={query[4:]}')
    else:
        wb.open_new_tab('https://www.youtube.com/')


@dp.message_handler(Text(equals=("Закрыть❌")), state=Chrome.base)
async def close_chrome(message: types.Message, state: FSMContext):
    await state.reset_state()
    await state.update_data({
        'chrome': False
    })
    pyautogui.hotkey('alt', 'f4')
    await message.answer("Chrome закрыт", reply_markup=start_kb())


@dp.message_handler(Text(equals='Назад↩'), state=Chrome.base)
async def back_from_chrome(message: types.Message, state: FSMContext):
    await state.set_state('*')
    await message.answer("Вы вышли из Chrome", reply_markup=start_kb())


# CHROME BLOCK <<<<<<<<<<

# SPOTIFY BLOCK >>>>>>>>>>

@dp.message_handler(Text(equals="Spotify🎧"))
async def open_spotify(message):
    pass


# SPOTIFY BLOCK <<<<<<<<<<

# STEAM BLOCK >>>>>>>>>>
@dp.message_handler(Text(equals="Steam🎮"))
async def open_steam(message):
    wb.open_new('steam://rungameid/444200')


# STEAM BLOCK <<<<<<<<<<

# PC BLOCK >>>>>>>>>>

@dp.message_handler(Text(equals="Гаси ебало💤"))
async def os_shutdown(message: types.Message):
    await Remote.pc.set()
    await message.answer('Точно?', reply_markup=pc_inline_kb())


@dp.callback_query_handler(lambda c: c.data == 'yes', state=Remote.pc)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await callback_query.answer()
    await callback_query.message.delete()
    os.system("shutdown -s -t 0")


@dp.callback_query_handler(lambda c: c.data == 'no', state=Remote.pc)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await callback_query.answer()
    await callback_query.message.delete()


# PC BLOCK <<<<<<<<<<

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
