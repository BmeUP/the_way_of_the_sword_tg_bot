import string
import random

import qrcode

from users.models.repositories.user_repository import UserRepository
from users.models.orm.user import User


class UserQR:
    def __init__(self, user_repository: UserRepository,
                 telegram_user_id: int):
        self.__user_repo = user_repository
        self.__user = None
        self.__telegram_user_id = telegram_user_id

    async def __get_user(self):
        self.__user: User = await self.__user_repo.get_one_or_none_by_params(telegram_user_id=self.__telegram_user_id)

    def __generate_qr(self):
        random_str = random.choices(string.ascii_uppercase, k=5)
        qr_data = self.__user.telegram_user_id + "".join(random_str)
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10,
                           border=4)
        qr.add_data()
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")




    async def get_qr(self):
        await self.__get_user()