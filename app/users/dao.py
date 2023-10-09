from app.dao.base import BaseDAO

from .models import User


class UserDAO(BaseDAO):
    model = User
