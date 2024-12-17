from common.repository import BaseRepository
from twots_bot.models.orm.message import Message


class MessageRepository(BaseRepository):
    def set_entity(self):
        self.entity = Message
