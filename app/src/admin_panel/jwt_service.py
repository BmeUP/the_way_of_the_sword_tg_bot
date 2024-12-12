from datetime import datetime, timedelta

import jwt

from config.settings import settings


class JWTService:
    def __init__(self, username: str | None = None):
        self.__username = username

    def __create_token(self, token_type: str):
        exp = datetime.now() + timedelta(minutes=5 if token_type == "access" else 20)
        payload = {"token_type": token_type, "username": self.__username,
                   "exp": exp}
        return jwt.encode(payload, settings.salt, algorithm="HS256")

    def validate_token(self, token: str): # noqa
        return jwt.decode(token, settings.salt, algorithms=["HS256"])

    def get_tokens(self):
        return {"access": self.__create_token(token_type="access"),
                "refresh": self.__create_token(token_type="refresh")}

    def refresh_tokens(self, refresh_token: str):
        decoded_data = self.validate_token(refresh_token)

        if decoded_data["token_type"] == "refresh":
            return self.get_tokens()