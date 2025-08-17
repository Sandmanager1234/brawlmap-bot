from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from main import db

async def get_gm_buttons():
    gm_buttons = []
    gm_list = await db.get_game_modes()
    for gm in gm_list:
        gm_buttons.append(
            [
                InlineKeyboardButton(text=gm[1], callback_data=f"{gm[3]}")
            ]
        )
    return gm_buttons

async def get_gm_kb():
    return InlineKeyboardMarkup(inline_keyboard=await get_gm_buttons())