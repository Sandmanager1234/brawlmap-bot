import os
import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from brawlapi.models import Event
from database.models import Base, GameModes, TelegramUsers, Maps

class Database:
    def __init__(self, db_url):
        self.engine = create_async_engine(db_url, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def dispose(self):
        await self.engine.dispose()

    async def check_tables(self):
        async with self.engine.connect() as conn:
            tables = await conn.run_sync(
                lambda sync_conn: sqlalchemy.inspect(sync_conn).get_table_names()
            )
        if set(tables) != {'maps', 'game_modes', 'telegram_users'}:
            await self.create_tables()
        else:
            Base.metadata.reflect

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_game_modes(self):
        async with self.async_session() as session:
            async with session.begin():
                gms = await session.execute(
                    sqlalchemy.select(GameModes)
                )
                return gms.fetchall()
    
    async def get_game_mode_map(self, mode_id: int):
        async with self.async_session() as session:
            async with session.begin():
                gm = await session.get(GameModes, mode_id)
                map_info = await session.get(Maps, gm.map)
                return map_info
    
    async def update_map_mode_info(self, event: Event):
         async with self.async_session() as session:
            async with session.begin():
                map_obj = await session.get(Maps, event.map_id)
                if map_obj:
                    map_obj.update_info(event)
                else:
                    map_obj = Maps.from_event(event)
                    await session.add(map_obj)
                await session.execute(
                    sqlalchemy.update(
                        GameModes
                    ).where(
                        GameModes.api_name == event.mode
                    ).values(
                        map=map_obj.id
                    )
                )
                await session.commit()

    async def add_user(self, user_info):
        async with self.async_session() as session:
            async with session.begin():
                user = TelegramUsers.from_telegram(user_info)
                await session.add(user)
                await session.commit()

    async def update_user(self, user_info):
        async with self.async_session() as session:
            async with session.begin():
                user = await session.get(TelegramUsers, user_info.id)
                user.update_info(user_info)
                await session.commit()
    
    async def get_user(self, user_id):
        async with self.async_session() as session:
            async with session.begin():
                user = await session.get(TelegramUsers, user_id)
                return user

    async def get_users_id(self):
        async with self.async_session() as session:
            async with session.begin():
                users_id = await session.execute(
                    sqlalchemy.select(
                        TelegramUsers.id
                    ).select_from(
                        TelegramUsers
                    )
                )
                return users_id.scalars().fetchall()
                


    