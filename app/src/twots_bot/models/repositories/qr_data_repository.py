from common.repository import BaseRepository
from twots_bot.models.orm.qr_data import QRData


class QRDataRepository(BaseRepository):
    def set_entity(self):
        self.entity = QRData
