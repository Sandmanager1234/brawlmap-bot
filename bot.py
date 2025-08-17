from aiogram import Bot
from dispatcher import get_dispatcher


async def start_bot(token: str) -> None:
    dp = get_dispatcher()
    bot = Bot(
        token=token
    )
    await dp.start_polling(bot)