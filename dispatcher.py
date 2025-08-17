from aiogram import Dispatcher


def get_dispatcher():
    from handlers.client import client_router
    from handlers.start import start_router
    dp = Dispatcher()
    dp.include_routers(
        client_router,
        start_router
    )
    return dp