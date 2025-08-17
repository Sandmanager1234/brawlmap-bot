from brawlapi.models import Event
from brawlapi.brawlapi import BrawlClient
from database.database import Database


class Updater:
    def __init__(
            self,
            db: Database,
            client: BrawlClient
    ):
        self.db = db
        self.client = client

    async def update_maps(self):
        self.client.start_session()
        try:
            response = self.client.get_events()
            for obj in response:
                event = Event.from_json(obj)
                await self.db.update_map_mode_info(event)
        except Exception as ex:
            pass
        finally:
            await self.client.close_session()
            