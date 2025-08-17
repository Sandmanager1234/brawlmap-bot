import os
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from brawlapi.models import Event


class Base(DeclarativeBase):
    pass


class Maps(Base):
    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    image_path: Mapped[str] = mapped_column(nullable=True)
    start_time: Mapped[int] = mapped_column(nullable=True)
    end_time: Mapped[int] = mapped_column(nullable=True)
    game_modes: Mapped[list["GameModes"]] = relationship()

    def update_info(self, event: Event):
        self.start_time = event.start_time
        self.end_time = event.end_time
        self.is_current = True

    @classmethod
    def from_event(cls, event: Event) -> "Maps":
        self: Maps = cls()
        self.id = event.map_id
        self.title = event.map_name
        self.start_time = event.start_time
        self.end_time = event.end_time
        return self
        
    
class GameModes(Base):
    __tablename__ = "game_modes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    api_name: Mapped[str] = mapped_column(unique=True, index=True)
    map: Mapped[list["Maps"]] = mapped_column(ForeignKey(Maps.id), nullable=True)


class TelegramUsers(Base):
    __tablename__ = 'telegram_users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)


    @classmethod
    def from_telegram(cls, user) -> "TelegramUsers":
        self: TelegramUsers = cls()
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name

    def update_info(self, user):
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name

# class Brawlers(Base):
#     ...



