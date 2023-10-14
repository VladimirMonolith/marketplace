from fastapi import Depends
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from sqladmin.authentication import AuthenticationBackend

from app.users.manager import current_superuser
from app.users.models import User


class AdminAuth(AuthenticationBackend):
    """Класс для аутентификации пользователей с возможностью администрирования."""


    # async def login(self, request: Request) -> bool:
    #     """Позволяет ."""
    #     form = await request.form()
    #     username, password = form["username"], form["password"]

    #     # Validate username/password credentials
    #     # And update session
    #     request.session.update({"token": "..."})

    #     return True


    def login(
            self,
            request: Request,
            user: User = Depends(current_superuser)
        ) -> bool:
        """Предоставляет доступ пользователям с возможностью администрирования."""
        request.session.update({'token': str(user.id)})
        return True

    async def logout(self, request: Request) -> bool:
        """."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """."""
        token = request.session.get("token")

        if not token:
            return False
        return True


authentication_backend = AdminAuth(secret_key="...")
