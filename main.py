import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import os
import pyautogui
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import *
from keyboards import *
import webbrowser as wb
from volume import set_volume
from close_apps import close_app

storage = MemoryStorage()
bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)


class Chrome(StatesGroup):
    base = State()


class Steam(StatesGroup):
    base = State()


class Remote(StatesGroup):
    base = State()
    pc = State()


class Spotify(StatesGroup):
    base = State()


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message):
    if message.from_user.id not in ADMIN_ID:
        await message.answer('Вы не мой хозяин!')
    else:
        await message.reply("Приветус!", reply_markup=start_kb())
        await Remote.base.set()


# VOLUME BLOCK >>>>>>>>>>>
@dp.message_handler(Text(equals="Громкость🔊"), state=Remote.base)
async def volume(message):
    await message.answer(text='dj арбуз к вашим услугам', reply_markup=volume_inline_kb())


@dp.callback_query_handler(lambda c: c.data in ('0', '0.25', '0.5', '0.75', '1'))
async def volume_callback(c: types.CallbackQuery):
    set_volume(float(c.data))
    await c.answer()

# VOLUME BLOCK <<<<<<<<<<<

# CHROME BLOCK >>>>>>>>>>>

@dp.message_handler(Text(equals="Chrome🌍"), state=Remote.base)
async def open_chrome(message: types.Message):
    await Chrome.base.set()
    if data['chrome']['run']:
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
        data['chrome']['run'] = True
        wb.open_new('https://')


@dp.message_handler(commands=['tg'], state=Chrome.base)
async def open_tg(message: types.Message):
    wb.open_new_tab('https://web.telegram.org/a/')


@dp.message_handler(commands=['search'], state=Chrome.base)
async def search(message: types.Message):
    query = message.text.replace(' ', '+')
    wb.open_new_tab(f'https://www.google.com/search?q={query[8:]}')
    await message.answer('Готово!', reply_markup=chrome_kb())
    await Chrome.base.set()


@dp.message_handler(commands=['ds'], state=Chrome.base)
async def open_ds(message: types.Message):
    wb.open_new_tab('https://discord.com/channels/@me')


@dp.message_handler(commands=['yt'], state=Chrome.base)
async def open_yt(message: types.Message):
    if len(message.text) > 3:
        query = message.text.replace(' ', '+')
        wb.open_new_tab(f'https://www.youtube.com/results?search_query={query[4:]}')
    else:
        wb.open_new_tab('https://www.youtube.com/')


@dp.message_handler(Text(equals=("Закрыть❌")), state=Chrome.base)
async def close_chrome(message: types.Message):
    await Remote.base.set()
    data['chrome']['run'] = False
    pyautogui.hotkey('alt', 'f4')
    await message.answer("Chrome закрыт", reply_markup=start_kb())


@dp.message_handler(Text(equals='Назад↩'), state=Chrome.base)
async def back_from_chrome(message: types.Message, state: FSMContext):
    await Remote.base.set()
    await message.answer("Вы вышли из Chrome", reply_markup=start_kb())


# CHROME BLOCK <<<<<<<<<<

# SPOTIFY BLOCK >>>>>>>>>>

@dp.message_handler(Text(equals="Spotify🎧"), state=Remote.base)
async def open_chrome(message: types.Message):
    await Spotify.base.set()
    if data['spotify']['run']:
        await message.answer('Spotify уже запущен!', reply_markup=spotify_kb())
    else:
        print(3)
        await message.answer('Запускаю Spotify!', reply_markup=spotify_kb())
        wb.open_new('spotify:/')
        data['spotify']['run'] = True


@dp.message_handler(Text(equals=("Закрыть❌")), state=Spotify.base)
async def close_spotify(message: types.Message, state: FSMContext):
    await Remote.base.set()
    close_app('spotify')
    data['spotify']['run'] = False
    await message.answer("Spotify закрыт", reply_markup=start_kb())


@dp.message_handler(Text(equals='Назад↩'), state=Spotify.base)
async def back_from_spotify(message: types.Message, state: FSMContext):
    await Remote.base.set()
    await message.answer("Вы вышли из Spotify", reply_markup=start_kb())


# SPOTIFY BLOCK <<<<<<<<<<

# STEAM BLOCK >>>>>>>>>>

@dp.message_handler(Text(equals="Steam🎮"), state=Remote.base)
async def open_steam(message):
    await Steam.base.set()
    print(1)
    if data['steam']['run']:
        print(2)
        await message.answer('Steam уже запущен!', reply_markup=steam_kb(data['steam']['games']))
    else:
        print(3)
        await message.answer('Запускаю Steam!', reply_markup=steam_kb(data['steam']['games']))
        wb.open_new('steam:/')
        data['steam']['run'] = True


@dp.message_handler(commands=['play'], state=Steam.base)
async def open_game(message: types.Message):
    game_name: str = message.get_args()
    count = 0
    for game in data['steam']['games']:
        if game['name'] == game_name:
            wb.open_new(f'steam://rungameid/{game["id"]}')
            break
        count += 1
    data['steam']['games'][count]['run'] = True
    await message.answer(f'{game_name} Запускается!', reply_markup=steam_kb(data['steam']['games']))


@dp.message_handler(commands=['close'], state=Steam.base)
async def open_game(message: types.Message):
    game_name: str = message.get_args()
    count = 0
    for game in data['steam']['games']:
        if game['name'] == game_name:
            close_app(game['proc'])
            break
        count += 1
    data['steam']['games'][count]['run'] = False
    await message.answer(f'{game_name} Закрыватся!', reply_markup=steam_kb(data['steam']['games']))


@dp.message_handler(Text(equals=("Закрыть❌")), state=Steam.base)
async def close_chrome(message: types.Message, state: FSMContext):
    await Remote.base.set()
    close_app('steam')
    data['steam']['run'] = False
    await message.answer("Steam закрыт", reply_markup=start_kb())


@dp.message_handler(Text(equals='Назад↩'), state=Steam.base)
async def back_from_chrome(message: types.Message, state: FSMContext):
    await Remote.base.set()
    await message.answer("Вы вышли из Steam", reply_markup=start_kb())


# STEAM BLOCK <<<<<<<<<<

# PC BLOCK >>>>>>>>>>


@dp.message_handler(Text(equals="Сфоткай📸"), state=Remote.base)
async def take_screenshot(message):
    await message.answer(text='Не шевелись...')
    pyautogui.screenshot('img/screenshot.png')
    screenshot = open("img/screenshot.png", 'rb')
    await bot.send_photo(message.chat.id, photo=screenshot, caption="Принимай🌅")


@dp.message_handler(Text(equals="Спим💤"), state=Remote.base)
async def os_shutdown(message: types.Message):
    await Remote.pc.set()
    await message.answer('Точно?', reply_markup=pc_inline_kb())


@dp.callback_query_handler(lambda c: c.data == 'yes', state=Remote.pc)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await Remote.base.set()
    await callback_query.answer()
    await callback_query.message.delete()
    os.system("shutdown -s -t 0")


@dp.callback_query_handler(lambda c: c.data == 'no', state=Remote.pc)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await Remote.base.set()
    await callback_query.answer()
    await callback_query.message.delete()


# PC BLOCK <<<<<<<<<<

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
