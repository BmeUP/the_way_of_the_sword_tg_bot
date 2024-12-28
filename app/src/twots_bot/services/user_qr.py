import string
import random
from io import BytesIO

import qrcode

from users.models.repositories.user_repository import UserRepository
from users.models.orm.user import User
from twots_bot.models.repositories.qr_data_repository import QRDataRepository
from twots_bot.models.orm.qr_data import QRData


class UserQR:
    def __init__(self, user_repository: UserRepository,
                 qr_data_repository: QRDataRepository,
                 telegram_user_id: int):
        self.__user_repo = user_repository
        self.__qr_data_repo = qr_data_repository
        self.__user = None
        self.__telegram_user_id = telegram_user_id
        self.__qr_data = None

    async def __get_user(self):
        self.__user: User = await self.__user_repo.get_one_or_none_by_params(telegram_user_id=self.__telegram_user_id)

    async def __generate_qr(self):
        random_str = random.choices(string.ascii_uppercase, k=5)
        self.__qr_data = str(self.__user.telegram_user_id) + "".join(random_str)
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10,
                           border=4)
        qr.add_data(self.__qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf)
        return buf.getvalue()

    async def __insert_qr_data(self):
        self.__qr_data_repo.add_to_the_session(data=QRData(qr_data=self.__qr_data, user=self.__user))
        await self.__qr_data_repo.persist()

    async def get_qr(self):
        await self.__get_user()
        _qr = await self.__generate_qr()
        await self.__insert_qr_data()
        return _qr
