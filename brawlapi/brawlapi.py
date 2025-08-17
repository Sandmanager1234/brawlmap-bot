import aiohttp
from typing import Optional, Dict


class BrawlClient:
    base_url = 'https://api.brawlstars.com'

    def __init__(
        self,
        access_token: str, 
    ):
        self.access_token = access_token
        self.session: Optional[aiohttp.ClientSession]

    
    def start_session(self) -> aiohttp.ClientSession:
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def __make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict],
        data: Optional[Dict]
    ):
        url = f'{self.base_url}{endpoint}'
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        try:
            async with self.session.request(
                method, url, headers=headers, params=params, data=data
            ) as response:
                if response.status in [401, 403]:
                    return {}
                elif response.status == 204:
                    return {}
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as ex:
            raise
        except aiohttp.ClientError as ex:
            raise

    async def get_events(
        self,
        params: Optional[Dict], 
        data: Optional[Dict]
    ):
        return await self.__make_request('GET', '/v1/events/rotation', params, data)
    
    async def get_player_info(
        self,
        tag: str,
        params: Optional[Dict], 
        data: Optional[Dict]
    ):
        return await self.__make_request('GET', f'/v1/players/{tag}', params, data)
    
    async def get_player_battlelog(
        self,
        tag: str,
        params: Optional[Dict], 
        data: Optional[Dict]
    ):
        return await self.__make_request('GET', f'/v1/players/{tag}/battlelog', params, data)
    
    async def get_club_info(
        self,
        tag: str,
        params: Optional[Dict], 
        data: Optional[Dict]
    ):
        return await self.__make_request('GET', f'/v1/clubs/{tag}', params, data)
    
    async def get_club_members(
        self,
        tag: str,
        params: Optional[Dict], 
        data: Optional[Dict]
    ):
        return await self.__make_request('GET', f'/v1/clubs/{tag}/members', params, data)

    async def get_rankings_players(
        self,
        country_code: str,
        params: Optional[Dict], 
        data: Optional[Dict]
    ):
        return await self.__make_request('GET', f'/v1/rankings/{country_code}/players', params, data)
    
    async def get_rankings_clubs(
        self,
        country_code: str,
        params: Optional[Dict], 
        data: Optional[Dict]
    ):
        return await self.__make_request('GET', f'/v1/rankings/{country_code}/clubs', params, data)

    async def get_brawlers(
        self,
        params: Optional[Dict], 
        data: Optional[Dict]
    ):
        return await self.__make_request('GET', '/v1/brawlers', params, data)
    
    async def get_brawler_info(
        self,
        brawler_id: str,
        params: Optional[Dict], 
        data: Optional[Dict]
    ):
        return await self.__make_request('GET', f'/v1/brawlers/{brawler_id}', params, data)
    
    