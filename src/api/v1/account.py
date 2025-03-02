from src.conf.loging import log
from fastapi import Depends, APIRouter, status, Form
from src.core.service.account.account import (
    get_account_service,
    AccountService
)
from src.core.service.auth.auth import (
    generate_token,
    get_current_user
)
from src.core.schema.responses import GlobalResponseSchema
from src.core.schema.account import (
    AccountCreateSchema,
    AccountResponseSchema,
)
from src.core.schema.token import TokenResponseSchema

account_api: APIRouter = APIRouter(prefix='/account', tags=['account'])


@account_api.post('/', status_code=status.HTTP_201_CREATED, response_model= AccountResponseSchema)
async def add_account(
        data: AccountCreateSchema,
        service:AccountService = Depends(get_account_service)
):
    return await service.add(**data.dict())


@account_api.get('/', status_code=status.HTTP_200_OK, response_model=GlobalResponseSchema)
async def get_account_list(
        offset: int = 0,
        limit: int = 10,
        service: AccountService = Depends(get_account_service)
):
    count = await service.get_count()
    result = await service.get_all()
    return GlobalResponseSchema[AccountResponseSchema](
        count=count[0],
        next=None,
        result=result
    )


@account_api.post('/login/')
async def login(
        username: str = Form(...),
        password: str = Form(),
        service: AccountService = Depends(get_account_service)
):

    user = await service.authenticate(username, password)
    token: str = ''
    if user:
        token = generate_token({
            'username': user.get('email'),
            'id': '{}'.format(user.get('id'))
        })
        return TokenResponseSchema(
            access_token=token,
            token_type='bearer'
        )


@account_api.get('/me/', status_code=200, response_model=AccountResponseSchema)
async def me(
    current_user=Depends(get_current_user)
):
    return current_user
