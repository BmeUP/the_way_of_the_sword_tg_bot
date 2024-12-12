from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from fastapi import HTTPException, status
import jwt

from config.db import AsyncSessionLocal
from users.models.repositories.user_repository import UserRepository
from admin_panel.utils import validate_password
from admin_panel.jwt_service import JWTService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_object_by_params(username=username)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if validate_password(password, user.password):
            jwt_service = JWTService(user.username)
            request.session.update(jwt_service.get_tokens())
            return True
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        access = request.session.get("access")

        if not access:
            return False

        jwt_service = JWTService()

        try:
            if jwt_service.validate_token(access):
                return True
        except jwt.exceptions.ExpiredSignatureError:
            refresh = request.session.get("refresh")
            request.session.update(jwt_service.refresh_tokens(refresh))
            return True