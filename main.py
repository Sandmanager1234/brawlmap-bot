import os
import sys
import logging
import asyncio

from dotenv import load_dotenv
from schedule import repeat, run_pending, every

from bot import start_bot
from updater import Updater
from database.database import Database
from brawlapi.brawlapi import BrawlClient

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_URL = os.getenv('DB_URL')
BRAWL_TOKEN = os.getenv('')

@repeat(every().hour)
def update():
    asyncio.run(updater.update_maps())


async def main() -> None:
    await start_bot(BOT_TOKEN)


if __name__ == '__main__':
    db = Database(
        db_url=DB_URL
    )
    brawl_client = BrawlClient(
        access_token=BRAWL_TOKEN
    )
    updater = Updater(
        db=db,
        client=brawl_client
    )
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())