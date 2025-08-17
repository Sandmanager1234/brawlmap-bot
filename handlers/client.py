from aiogram import Router, types
from aiogram.filters import Command
from keyboards.gamemods import get_gm_kb

client_router = Router()


@client_router.message(Command('/map'))
async def get_gm_list(msg: types.Message):
    await msg.answer('Выбери режим: ', reply_markup=get_gm_kb())

@client_router.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    ...

