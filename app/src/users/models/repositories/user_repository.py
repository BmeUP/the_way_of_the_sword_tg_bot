from common.repository import BaseRepository
from users.models.orm.user import User


class UserRepository(BaseRepository):
    def set_entity(self):
        self.entity = User
