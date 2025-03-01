from fastapi import Depends, HTTPException
from src.db.model.account.account import Account
from src.db.engine import get_async_session
from src.core.service.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class AccountService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Account)

    async def before_add(self, instance, *args, **kwargs):
        instance.set_pwd(kwargs.get('password'))

    async def get_by_email(self, email: str):
        async def _get_by_email(in_email: str):
            query = select(self.model).where(self.model.email == in_email)
            return await self.session.execute(query)

        return await self._exec(_get_by_email, in_email=email, fetch_one=True)

    async def authenticate(self, email: str, password: str):
        user = await self.get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Wrong Email or Password"
            )
        if user.ver_pwd(password):
            return {
                "email": user.email,
                'id': user.id
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="Wrong Email or Password"
            )



def get_account_service(session=Depends(get_async_session)) -> AccountService:
    return AccountService(session)
