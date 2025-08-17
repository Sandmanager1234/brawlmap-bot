from aiogram import Router, types
from aiogram.filters import CommandStart

from keyboards.gamemods import get_gm_kb

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(msg: types.Message) -> None:
    await msg.answer('Выбери режим:', reply_markup=get_gm_kb())
