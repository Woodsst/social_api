import abc
from abc import ABC
from functools import lru_cache
from typing import Tuple, Union, Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import Repository
from db.get_session import get_session
from schemas.schemas import Users


class BaseLoginRepository(ABC):
    """Interface from login repository."""

    @abc.abstractmethod
    async def get_user_id_and_password(
        self, login: str
    ) -> Union[Tuple[None, None], Any]:
        """Request in db for get user id."""


class LoginRepository(BaseLoginRepository, Repository):
    """Repository for work with a database with user data."""

    async def get_user_id_and_password(
        self, login: str
    ) -> Union[Tuple[None, None], Any]:
        """Request in db for get user id."""
        stmt = select(Users.id, Users.password).where(Users.login == login)
        request = await self.session.execute(stmt)
        response = request.first()
        if response is None:
            return None, None
        return response


@lru_cache()
def get_login_repo(
    engine: AsyncSession = Depends(get_session),
) -> LoginRepository:
    return LoginRepository(engine)
